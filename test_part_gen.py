import uuid

class IDGen:
    def __init__(self, start_ref=200000):
        self.ref = start_ref

    def next_ref(self):
        self.ref += 1
        return f"R{self.ref}"

    def next_uid(self):
        return uuid.uuid4().hex

FACE_TOKEN = {'Right': 0, 'Top': 1, 'Back': 2, 'Left': 3, 'Bottom': 4, 'Front': 5}
MATERIAL = {'Plastic': 256, 'SmoothPlastic': 272, 'Wood': 512, 'Slate': 800, 'Concrete': 816,
            'CorrugatedMetal': 1088, 'Metal': 1088, 'WoodPlanks': 528}

def f_str(v):
    return ('%.4f' % v).rstrip('0').rstrip('.') if v != 0 else '0'

def xml_part(id_gen, name, pos, R, size, color=(163, 162, 165), transparency=0.0,
             material='SmoothPlastic', cls='Part', collide=True, cast_shadow=True,
             textures=None, point_light=None, children_xml=""):
    ref = id_gen.next_ref()
    uid = id_gen.next_uid()
    mat_id = MATERIAL.get(material, 272)
    col_int = 0xFF000000 | (color[0] << 16) | (color[1] << 8) | color[2]
    
    xml = []
    xml.append(f'\t\t\t\t<Item class="{cls}" referent="{ref}">\n')
    xml.append('\t\t\t\t\t<Properties>\n')
    xml.append(f'\t\t\t\t\t\t<string name="Name">{name}</string>\n')
    xml.append('\t\t\t\t\t\t<bool name="Anchored">true</bool>\n')
    xml.append(f'\t\t\t\t\t\t<bool name="CanCollide">{"true" if collide else "false"}</bool>\n')
    xml.append(f'\t\t\t\t\t\t<bool name="CastShadow">{"true" if cast_shadow else "false"}</bool>\n')
    xml.append(f'\t\t\t\t\t\t<Color3uint8 name="Color3uint8">{col_int}</Color3uint8>\n')
    xml.append(f'\t\t\t\t\t\t<token name="Material">{mat_id}</token>\n')
    if transparency > 0:
        xml.append(f'\t\t\t\t\t\t<float name="Transparency">{f_str(transparency)}</float>\n')
    xml.append(f'\t\t\t\t\t\t<Vector3 name="size"><X>{f_str(size[0])}</X><Y>{f_str(size[1])}</Y><Z>{f_str(size[2])}</Z></Vector3>\n')
    xml.append(f'\t\t\t\t\t\t<CoordinateFrame name="CFrame"><X>{f_str(pos[0])}</X><Y>{f_str(pos[1])}</Y><Z>{f_str(pos[2])}</Z>')
    xml.append(f'<R00>{f_str(R[0][0])}</R00><R01>{f_str(R[0][1])}</R01><R02>{f_str(R[0][2])}</R02>')
    xml.append(f'<R10>{f_str(R[1][0])}</R10><R11>{f_str(R[1][1])}</R11><R12>{f_str(R[1][2])}</R12>')
    xml.append(f'<R20>{f_str(R[2][0])}</R20><R21>{f_str(R[2][1])}</R21><R22>{f_str(R[2][2])}</R22></CoordinateFrame>\n')
    xml.append(f'\t\t\t\t\t\t<token name="TopSurface">0</token>\n')
    xml.append(f'\t\t\t\t\t\t<token name="BottomSurface">0</token>\n')
    xml.append(f'\t\t\t\t\t\t<UniqueId name="UniqueId">{uid}</UniqueId>\n')
    xml.append('\t\t\t\t\t</Properties>\n')
    
    # Children
    if textures:
        for face_name, tex_url, stu, stv in textures:
            t_ref = id_gen.next_ref()
            t_uid = id_gen.next_uid()
            f_tok = FACE_TOKEN.get(face_name, 1)
            xml.append(f'\t\t\t\t\t<Item class="Texture" referent="{t_ref}">\n')
            xml.append('\t\t\t\t\t\t<Properties>\n')
            xml.append(f'\t\t\t\t\t\t\t<string name="Name">Texture</string>\n')
            xml.append(f'\t\t\t\t\t\t\t<Content name="Texture"><url>{tex_url}</url></Content>\n')
            xml.append(f'\t\t\t\t\t\t\t<token name="Face">{f_tok}</token>\n')
            xml.append(f'\t\t\t\t\t\t\t<float name="StudsPerTileU">{f_str(stu)}</float>\n')
            xml.append(f'\t\t\t\t\t\t\t<float name="StudsPerTileV">{f_str(stv)}</float>\n')
            xml.append(f'\t\t\t\t\t\t\t<UniqueId name="UniqueId">{t_uid}</UniqueId>\n')
            xml.append('\t\t\t\t\t\t</Properties>\n')
            xml.append('\t\t\t\t\t</Item>\n')

    if point_light:
        l_ref = id_gen.next_ref()
        l_uid = id_gen.next_uid()
        b_val, r_val, col = point_light
        xml.append(f'\t\t\t\t\t<Item class="PointLight" referent="{l_ref}">\n')
        xml.append('\t\t\t\t\t\t<Properties>\n')
        xml.append(f'\t\t\t\t\t\t\t<string name="Name">PointLight</string>\n')
        xml.append(f'\t\t\t\t\t\t\t<float name="Brightness">{f_str(b_val)}</float>\n')
        xml.append(f'\t\t\t\t\t\t\t<float name="Range">{f_str(r_val)}</float>\n')
        xml.append(f'\t\t\t\t\t\t\t<Color3 name="Color"><R>{f_str(col[0])}</R><G>{f_str(col[1])}</G><B>{f_str(col[2])}</B></Color3>\n')
        xml.append(f'\t\t\t\t\t\t\t<bool name="Shadows">true</bool>\n')
        xml.append(f'\t\t\t\t\t\t\t<UniqueId name="UniqueId">{l_uid}</UniqueId>\n')
        xml.append('\t\t\t\t\t\t</Properties>\n')
        xml.append('\t\t\t\t\t</Item>\n')
        
    if children_xml:
        xml.append(children_xml)
        
    xml.append('\t\t\t\t</Item>\n')
    return "".join(xml)

print("IDGen and xml_part defined successfully.")
