"""Lector exacto de .lotheader / .lotpack de Project Zomboid Build 42.

Basado en zombie/iso/IsoMetaGrid.java (loadCell, lineas 1992-2106) e
zombie/iso/IsoLot.java (load, lineas 118-179). Todo Little-Endian.
Celdas de 256x256 cuadros, 32x32 chunks de 8x8.
"""
import os
import struct

CELL = 256
CHUNKS = 32
CH = 8


class Reader:
    def __init__(self, data):
        self.d = data
        self.p = 0

    def i32(self):
        v = struct.unpack_from('<i', self.d, self.p)[0]
        self.p += 4
        return v

    def line(self):
        e = self.d.index(b'\n', self.p)
        s = self.d[self.p:e]
        self.p = e + 1
        if s.endswith(b'\r'):
            s = s[:-1]
        return s.decode('utf-8', 'replace')


class Room:
    __slots__ = ('index', 'name', 'level', 'rects', 'objects', 'building')

    def __init__(self, index, name, level, rects, objects):
        self.index = index
        self.name = name
        self.level = level
        self.rects = rects        # [(x, y, w, h)] en coordenadas de mundo
        self.objects = objects
        self.building = -1


class LotHeader:
    def __init__(self, path, cx, cy):
        self.cx, self.cy = cx, cy
        r = Reader(open(path, 'rb').read())
        version = 0
        if r.d[:4] == b'LOTH':
            r.p = 4
            version = r.i32()
        self.version = version
        n = r.i32()
        self.tiles = [r.line().strip() for _ in range(n)]
        if version == 0:
            r.p += 1
        w, h = r.i32(), r.i32()
        assert w == 8 and h == 8, 'chunk invalido %dx%d' % (w, h)
        if version == 0:
            self.minLevel, self.maxLevel = 0, r.i32() - 1
        else:
            self.minLevel, self.maxLevel = r.i32(), r.i32()
        ox, oy = cx * CELL, cy * CELL
        self.rooms = []
        for i in range(r.i32()):
            name = r.line()
            level = r.i32()
            rects = []
            for _ in range(r.i32()):
                x, y, rw, rh = r.i32(), r.i32(), r.i32(), r.i32()
                rects.append((x + ox, y + oy, rw, rh))
            objs = []
            for _ in range(r.i32()):
                t, x, y = r.i32(), r.i32(), r.i32()
                objs.append((t, x + ox, y + oy))
            self.rooms.append(Room(i, name, level, rects, objs))
        self.buildings = []
        for b in range(r.i32()):
            idx = [r.i32() for _ in range(r.i32())]
            for i in idx:
                self.rooms[i].building = b
            self.buildings.append(idx)
        raw = r.d[r.p:r.p + 1024]
        # en disco: lwx*32+lwy
        self.zombieIntensity = {(i // 32, i % 32): raw[i] for i in range(len(raw))}


def load_lotpack(path, hdr, chunk_filter=None):
    """Devuelve dict {(wx, wy, z): [nombres de sprite de abajo hacia arriba]}
    en coordenadas de mundo. chunk_filter(lwx, lwy) -> bool para limitar."""
    d = open(path, 'rb').read()
    base = 8 if d[:4] == b'LOTP' else 0
    out = {}
    ox, oy = hdr.cx * CELL, hdr.cy * CELL
    minZ = max(hdr.minLevel, -32)
    maxZ = min(hdr.maxLevel, 31)
    for lwx in range(CHUNKS):
        for lwy in range(CHUNKS):
            if chunk_filter and not chunk_filter(lwx, lwy):
                continue
            idx = lwx * 32 + lwy
            pos = struct.unpack_from('<q', d, base + 4 + idx * 8)[0]
            r = Reader(d)
            r.p = pos
            skip = 0
            for z in range(minZ, maxZ + 1):
                for x in range(8):
                    for y in range(8):
                        if skip > 0:
                            skip -= 1
                            continue
                        count = r.i32()
                        if count == -1:
                            skip = r.i32()
                            if skip > 0:
                                skip -= 1
                                continue
                        if count <= 1:
                            continue
                        r.i32()  # roomID legado (ignorado por IsoLot)
                        names = [hdr.tiles[r.i32()] for _ in range(count - 1)]
                        out[(ox + lwx * 8 + x, oy + lwy * 8 + y, z)] = names
    return out


def load_region(mapdir, x0, y0, x1, y1):
    """Carga todos los cuadros en [x0,x1) x [y0,y1) (coords de mundo)."""
    squares = {}
    rooms = []
    headers = {}
    for cx in range(x0 // CELL, (x1 - 1) // CELL + 1):
        for cy in range(y0 // CELL, (y1 - 1) // CELL + 1):
            hp = os.path.join(mapdir, '%d_%d.lotheader' % (cx, cy))
            pp = os.path.join(mapdir, 'world_%d_%d.lotpack' % (cx, cy))
            if not os.path.exists(hp):
                continue
            hdr = LotHeader(hp, cx, cy)
            headers[(cx, cy)] = hdr

            def flt(lwx, lwy, cx=cx, cy=cy):
                wx = cx * CELL + lwx * 8
                wy = cy * CELL + lwy * 8
                return wx + 8 > x0 and wx < x1 and wy + 8 > y0 and wy < y1

            sq = load_lotpack(pp, hdr, flt)
            for k, v in sq.items():
                if x0 <= k[0] < x1 and y0 <= k[1] < y1:
                    squares[k] = v
            for rm in hdr.rooms:
                for (rx, ry, rw, rh) in rm.rects:
                    if rx < x1 and rx + rw > x0 and ry < y1 and ry + rh > y0:
                        rooms.append(rm)
                        break
    return squares, rooms, headers
