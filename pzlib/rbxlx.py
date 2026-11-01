"""Escritor minimo de lugares Roblox en XML (.rbxlx, version 4)."""
from xml.sax.saxutils import escape

FACE_TOKEN = {'Right': 0, 'Top': 1, 'Back': 2, 'Left': 3, 'Bottom': 4, 'Front': 5}
MATERIAL = {'Plastic': 256, 'SmoothPlastic': 272, 'Wood': 512, 'Brick': 800, 'Concrete': 816,
            'Grass': 1280, 'Glass': 1568, 'Metal': 1088, 'Fabric': 1312, 'Slate': 800,
            'Asphalt': 1376, 'WoodPlanks': 528}


def _f(v):
    return ('%.4f' % v).rstrip('0').rstrip('.') if v != 0 else '0'


class Inst:
    __slots__ = ('cls', 'props', 'children')

    def __init__(self, cls, props=None, children=None):
        self.cls = cls
        self.props = props or []      # [(tipo, nombre, valor)]
        self.children = children or []

    def add(self, child):
        self.children.append(child)
        return child


def part(name, pos, R, size, color=(163, 162, 165), transparency=0.0, material='SmoothPlastic',
         collide=True, shape=None, cls='Part', cast_shadow=True):
    props = [
        ('string', 'Name', name),
        ('bool', 'Anchored', True),
        ('CFrame', 'CFrame', (pos, R)),
        ('Vector3', 'size', size),
        ('Color3uint8', 'Color3uint8', color),
        ('token', 'Material', MATERIAL.get(material, 272)),
        ('bool', 'CanCollide', collide),
        ('token', 'TopSurface', 0),
        ('token', 'BottomSurface', 0),
    ]
    if transparency:
        props.append(('float', 'Transparency', transparency))
    if not collide:
        props.append(('bool', 'CanTouch', False))
        props.append(('bool', 'CanQuery', transparency < 1))
    if not cast_shadow:
        props.append(('bool', 'CastShadow', False))
    if shape is not None:
        props.append(('token', 'shape', shape))
    return Inst(cls, props)


def decal(face, url, zindex=1, transparency=0.0):
    p = [('Content', 'Texture', url), ('token', 'Face', FACE_TOKEN[face]), ('int', 'ZIndex', zindex)]
    if transparency:
        p.append(('float', 'Transparency', transparency))
    return Inst('Decal', p)


def texture(face, url, studs_u, studs_v, zindex=1):
    return Inst('Texture', [('Content', 'Texture', url), ('token', 'Face', FACE_TOKEN[face]),
                            ('float', 'StudsPerTileU', studs_u), ('float', 'StudsPerTileV', studs_v),
                            ('int', 'ZIndex', zindex)])


def model(name):
    return Inst('Model', [('string', 'Name', name)])


def folder(name):
    return Inst('Folder', [('string', 'Name', name)])


def script(name, source, cls='Script'):
    return Inst(cls, [('string', 'Name', name), ('ProtectedString', 'Source', source)])


class Writer:
    def __init__(self, path):
        self.f = open(path, 'w', encoding='utf-8')
        self.ref = 0

    def _prop(self, t, n, v, ind):
        w = self.f.write
        if t == 'string':
            w('%s<string name="%s">%s</string>\n' % (ind, n, escape(v)))
        elif t == 'bool':
            w('%s<bool name="%s">%s</bool>\n' % (ind, n, 'true' if v else 'false'))
        elif t in ('float', 'int', 'token'):
            w('%s<%s name="%s">%s</%s>\n' % (ind, t, n, _f(v) if t == 'float' else int(v), t))
        elif t == 'Vector3':
            w('%s<Vector3 name="%s"><X>%s</X><Y>%s</Y><Z>%s</Z></Vector3>\n' % (ind, n, _f(v[0]), _f(v[1]), _f(v[2])))
        elif t == 'Color3uint8':
            r, g, b = v
            w('%s<Color3uint8 name="%s">%d</Color3uint8>\n' % (ind, n, 0xFF000000 | (r << 16) | (g << 8) | b))
        elif t == 'Color3':
            w('%s<Color3 name="%s"><R>%s</R><G>%s</G><B>%s</B></Color3>\n' % (ind, n, _f(v[0]), _f(v[1]), _f(v[2])))
        elif t == 'CFrame':
            p, R = v
            w('%s<CoordinateFrame name="%s"><X>%s</X><Y>%s</Y><Z>%s</Z>' % (ind, n, _f(p[0]), _f(p[1]), _f(p[2])))
            w('<R00>%s</R00><R01>%s</R01><R02>%s</R02><R10>%s</R10><R11>%s</R11><R12>%s</R12><R20>%s</R20><R21>%s</R21><R22>%s</R22></CoordinateFrame>\n' % tuple(
                _f(R[i][j]) for i in range(3) for j in range(3)))
        elif t == 'Content':
            w('%s<Content name="%s"><url>%s</url></Content>\n' % (ind, n, escape(v)))
        elif t == 'ProtectedString':
            w('%s<ProtectedString name="%s"><![CDATA[%s]]></ProtectedString>\n' % (ind, n, v))

    def write_inst(self, inst, depth=1):
        self.ref += 1
        ind = '\t' * depth
        self.f.write('%s<Item class="%s" referent="R%d">\n%s\t<Properties>\n' % (ind, inst.cls, self.ref, ind))
        for t, n, v in inst.props:
            self._prop(t, n, v, ind + '\t\t')
        self.f.write('%s\t</Properties>\n' % ind)
        for c in inst.children:
            self.write_inst(c, depth + 1)
        self.f.write('%s</Item>\n' % ind)

    def write_place(self, roots):
        self.f.write('<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" '
                     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                     'xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">\n')
        self.f.write('\t<External>null</External>\n\t<External>nil</External>\n')
        for r in roots:
            self.write_inst(r)
        self.f.write('</roblox>\n')
        self.f.close()
