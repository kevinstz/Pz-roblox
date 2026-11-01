"""Lector de definiciones binarias .tiles (IsoWorld.java 630-774) y de
archivos .pack (TexturePackDevice.java 84-146)."""
import io
import os
import struct

MEDIA = r'C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media'


def _line(d, p):
    e = d.index(b'\n', p)
    s = d[p:e]
    if s.endswith(b'\r'):
        s = s[:-1]
    return s.decode('utf-8', 'replace'), e + 1


def load_tiles_file(path, props):
    d = open(path, 'rb').read()
    p = 0
    if d[:4] == b'tdef':
        p = 8  # magic + version
    n = struct.unpack_from('<i', d, p)[0]
    p += 4
    for _ in range(n):
        name, p = _line(d, p)
        name = name.strip()
        _img, p = _line(d, p)
        w, h, tid, nt = struct.unpack_from('<4i', d, p)
        p += 16
        for i in range(nt):
            np_ = struct.unpack_from('<i', d, p)[0]
            p += 4
            pr = {}
            for _ in range(np_):
                k, p = _line(d, p)
                v, p = _line(d, p)
                pr[k.strip()] = v.strip()
            key = '%s_%d' % (name, i)
            if key in props and path.endswith('.patch.tiles'):
                props[key].update(pr)
            elif pr or key not in props:
                props[key] = pr
    return props


def load_all_tiles():
    props = {}
    for f in ['newtiledefinitions.tiles', 'tiledefinitions_erosion.tiles',
              'tiledefinitions_overlays.tiles',
              'tiledefinitions_b42chunkcaching.tiles',
              'tiledefinitions_noiseworks.patch.tiles',
              'jumbo_trees_big.tiles', 'jumbo_trees.tiles']:
        p = os.path.join(MEDIA, f)
        if os.path.exists(p):
            load_tiles_file(p, props)
    return props


class PackIndex:
    """Indexa todas las sub-texturas de varios .pack sin decodificar PNGs."""

    def __init__(self, packs):
        self.entries = {}   # name -> (packpath, pageid, x, y, w, h, ox, oy, fx, fy)
        self.pages = {}     # (packpath, pageid) -> (offset, length)
        self._cache = {}
        for pk in packs:
            path = os.path.join(MEDIA, 'texturepacks', pk)
            if os.path.exists(path):
                self._index(path)

    def _index(self, path):
        f = open(path, 'rb')
        size = os.path.getsize(path)
        magic = f.read(4)
        if magic == b'PZPK':
            version, npages = struct.unpack('<ii', f.read(8))
        else:
            version = 0
            f.seek(0)
            npages = struct.unpack('<i', f.read(4))[0]
        for pg in range(npages):
            ln = struct.unpack('<i', f.read(4))[0]
            f.read(ln)
            ne, _mask = struct.unpack('<ii', f.read(8))
            for _ in range(ne):
                ln = struct.unpack('<i', f.read(4))[0]
                nm = f.read(ln).decode('latin-1')
                vals = struct.unpack('<8i', f.read(32))
                if nm not in self.entries:
                    self.entries[nm] = (path, pg) + vals
            if version >= 1:
                plen = struct.unpack('<i', f.read(4))[0]
                off = f.tell()
                f.seek(plen, 1)
            else:
                # v0: PNG sin prefijo de longitud, seguido de 0xDEADBEEF (LE)
                off = f.tell()
                if not hasattr(self, '_whole') or self._whole[0] != path:
                    with open(path, 'rb') as g:
                        self._whole = (path, g.read())
                data = self._whole[1]
                k = data.find(b'IEND\xaeB`\x82\xef\xbe\xad\xde', off)
                if k < 0:
                    break
                plen = k + 8 - off
                f.seek(off + plen + 4)
            self.pages[(path, pg)] = (off, plen)
            if f.tell() >= size:
                break
        f.close()

    def page_image(self, path, pg):
        from PIL import Image
        key = (path, pg)
        if key not in self._cache:
            if len(self._cache) > 24:
                self._cache.pop(next(iter(self._cache)))
            off, ln = self.pages[key]
            with open(path, 'rb') as f:
                f.seek(off)
                data = f.read(ln)
            self._cache[key] = Image.open(io.BytesIO(data)).convert('RGBA')
        return self._cache[key]

    def sprite(self, name):
        """Devuelve la imagen RGBA sin recortar (fx x fy, p.ej. 128x256)."""
        from PIL import Image
        e = self.entries.get(name)
        if not e:
            return None
        path, pg, x, y, w, h, ox, oy, fx, fy = e
        page = self.page_image(path, pg)
        img = Image.new('RGBA', (fx, fy), (0, 0, 0, 0))
        img.paste(page.crop((x, y, x + w, y + h)), (ox, oy))
        return img
