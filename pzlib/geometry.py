"""Parser de media/tileGeometry.txt (TileGeometryFile.java, VERSION 2,
COORD_MULT = 10000). Ejes de escena: X = mundo +x, Y = arriba, Z = mundo +y.
Origen = centro del suelo del cuadro. 1 piso = sqrt(6) unidades."""
import os
import re

MEDIA = r'C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media'
STORY = 6 ** 0.5


def _vec(s, mult):
    return tuple(float(v) / mult for v in s.strip().strip(',').split('x'))


def _tokens(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return re.findall(r'[{}]|[^{}\n]+', text)


def load_tile_geometry(path=None):
    path = path or os.path.join(MEDIA, 'tileGeometry.txt')
    text = open(path, 'r', encoding='utf-8', errors='replace').read()
    toks = [t.strip() for t in _tokens(text) if t.strip()]
    mult = 10000.0
    out = {}
    i = 0
    stack = []
    tileset = None
    cur_tile = None
    cur_prim = None
    pending = None
    while i < len(toks):
        t = toks[i]
        if t == '{':
            stack.append(pending)
            if pending == 'tile':
                cur_tile = {'xy': None, 'shapes': [], 'props': {}}
            elif pending in ('box', 'cylinder', 'polygon'):
                cur_prim = {'type': pending}
            pending = None
        elif t == '}':
            kind = stack.pop() if stack else None
            if kind == 'tile' and cur_tile is not None and tileset:
                c, r = cur_tile['xy']
                out['%s_%d' % (tileset, c + r * 8)] = cur_tile
                cur_tile = None
            elif kind in ('box', 'cylinder', 'polygon') and cur_prim is not None:
                if cur_tile is not None:
                    cur_tile['shapes'].append(cur_prim)
                cur_prim = None
            elif kind == 'tileset':
                tileset = None
        elif '=' in t:
            k, v = [a.strip() for a in t.split('=', 1)]
            v = v.rstrip(',').strip()
            top = stack[-1] if stack else None
            if k == 'VERSION':
                mult = 10000.0 if int(v) >= 2 else 1000.0
            elif top == 'tileset' and k == 'name':
                tileset = v
            elif top == 'tile' and k == 'xy':
                a, b = v.split('x')
                cur_tile['xy'] = (int(a), int(b))
            elif top in ('box', 'cylinder', 'polygon') and cur_prim is not None:
                if k in ('translate', 'rotate', 'min', 'max'):
                    cur_prim[k] = _vec(v, mult)
                elif k in ('radius1', 'radius2', 'height'):
                    cur_prim[k] = float(v) / mult
                elif k == 'plane':
                    cur_prim[k] = v
                elif k == 'points':
                    pts = []
                    for p in v.split():
                        a, b = p.split('x')
                        pts.append((float(a) / mult, float(b) / mult))
                    cur_prim[k] = pts
            elif top == 'properties' and cur_tile is not None:
                cur_tile['props'][k] = v
        else:
            pending = t
        i += 1
    return out
