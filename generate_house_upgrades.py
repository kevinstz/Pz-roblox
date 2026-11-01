import uuid
import numpy as np

FACE_TOKEN = {'Right': 0, 'Top': 1, 'Back': 2, 'Left': 3, 'Bottom': 4, 'Front': 5}
MATERIAL = {'Plastic': 256, 'SmoothPlastic': 272, 'Wood': 512, 'Slate': 800, 'Concrete': 816,
            'CorrugatedMetal': 1088, 'Metal': 1088, 'WoodPlanks': 528}

def f_str(v):
    return ('%.4f' % v).rstrip('0').rstrip('.') if v != 0 else '0'

# Predefined Rotations
R_ID = np.eye(3)

# Wedge slope falling to +X (East): local +Z points to -X, local +X points to +Z
R_FALL_EAST = np.array([
    [0.0, 0.0, -1.0],
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 0.0]
])

# Wedge slope falling to -X (West): local +Z points to +X, local +X points to -Z
R_FALL_WEST = np.array([
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
    [-1.0, 0.0, 0.0]
])

# Gable triangle rising to +X: local +Z points to +X, local +X points to -Z
R_GABLE_RISE_EAST = np.array([
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
    [-1.0, 0.0, 0.0]
])

# Gable triangle rising to -X: local +Z points to -X, local +X points to +Z
R_GABLE_RISE_WEST = np.array([
    [0.0, 0.0, -1.0],
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 0.0]
])

# Textures
TEX_ROOF_DARK = "rbxasset://pz42/28f483ee7d0736992bde.png"
TEX_ROOF_TAN  = "rbxasset://pz42/334d48f51be74b5e9e1a.png"
TEX_SIDING    = "rbxasset://pz42/e6f1472b169f9a674721.png"
TEX_SKIRTING  = "rbxasset://pz42/f897bb35b4c9b00e4359.png"
TEX_WOOD_DECK = "rbxasset://pz42/109d70ae137a46eff0bd.png"
TEX_AC_GRILL  = "rbxasset://pz42/7557fa72aaf5e0e0799a.png"

class HouseUpgradeBuilder:
    def __init__(self, start_ref=200000):
        self.ref = start_ref

    def next_ref(self):
        self.ref += 1
        return f"R{self.ref}"

    def next_uid(self):
        return uuid.uuid4().hex

    def part(self, name, pos, R, size, color=(163, 162, 165), transparency=0.0,
             material='SmoothPlastic', cls='Part', collide=True, cast_shadow=True,
             textures=None, point_light=None, indent="\t\t\t\t"):
        ref = self.next_ref()
        uid = self.next_uid()
        mat_id = MATERIAL.get(material, 272)
        col_int = 0xFF000000 | (color[0] << 16) | (color[1] << 8) | color[2]
        
        xml = []
        xml.append(f'{indent}<Item class="{cls}" referent="{ref}">\n')
        xml.append(f'{indent}\t<Properties>\n')
        xml.append(f'{indent}\t\t<string name="Name">{name}</string>\n')
        xml.append(f'{indent}\t\t<bool name="Anchored">true</bool>\n')
        xml.append(f'{indent}\t\t<bool name="CanCollide">{"true" if collide else "false"}</bool>\n')
        xml.append(f'{indent}\t\t<bool name="CastShadow">{"true" if cast_shadow else "false"}</bool>\n')
        xml.append(f'{indent}\t\t<Color3uint8 name="Color3uint8">{col_int}</Color3uint8>\n')
        xml.append(f'{indent}\t\t<token name="Material">{mat_id}</token>\n')
        if transparency > 0:
            xml.append(f'{indent}\t\t<float name="Transparency">{f_str(transparency)}</float>\n')
        xml.append(f'{indent}\t\t<Vector3 name="size"><X>{f_str(size[0])}</X><Y>{f_str(size[1])}</Y><Z>{f_str(size[2])}</Z></Vector3>\n')
        xml.append(f'{indent}\t\t<CoordinateFrame name="CFrame"><X>{f_str(pos[0])}</X><Y>{f_str(pos[1])}</Y><Z>{f_str(pos[2])}</Z>')
        xml.append(f'<R00>{f_str(R[0][0])}</R00><R01>{f_str(R[0][1])}</R01><R02>{f_str(R[0][2])}</R02>')
        xml.append(f'<R10>{f_str(R[1][0])}</R10><R11>{f_str(R[1][1])}</R11><R12>{f_str(R[1][2])}</R12>')
        xml.append(f'<R20>{f_str(R[2][0])}</R20><R21>{f_str(R[2][1])}</R21><R22>{f_str(R[2][2])}</R22></CoordinateFrame>\n')
        xml.append(f'{indent}\t\t<token name="TopSurface">0</token>\n')
        xml.append(f'{indent}\t\t<token name="BottomSurface">0</token>\n')
        xml.append(f'{indent}\t\t<UniqueId name="UniqueId">{uid}</UniqueId>\n')
        xml.append(f'{indent}\t</Properties>\n')
        
        if textures:
            for face_name, tex_url, stu, stv in textures:
                t_ref = self.next_ref()
                t_uid = self.next_uid()
                f_tok = FACE_TOKEN.get(face_name, 1)
                xml.append(f'{indent}\t<Item class="Texture" referent="{t_ref}">\n')
                xml.append(f'{indent}\t\t<Properties>\n')
                xml.append(f'{indent}\t\t\t<string name="Name">Texture</string>\n')
                xml.append(f'{indent}\t\t\t<Content name="Texture"><url>{tex_url}</url></Content>\n')
                xml.append(f'{indent}\t\t\t<token name="Face">{f_tok}</token>\n')
                xml.append(f'{indent}\t\t\t<float name="StudsPerTileU">{f_str(stu)}</float>\n')
                xml.append(f'{indent}\t\t\t<float name="StudsPerTileV">{f_str(stv)}</float>\n')
                xml.append(f'{indent}\t\t\t<UniqueId name="UniqueId">{t_uid}</UniqueId>\n')
                xml.append(f'{indent}\t\t</Properties>\n')
                xml.append(f'{indent}\t</Item>\n')

        if point_light:
            l_ref = self.next_ref()
            l_uid = self.next_uid()
            b_val, r_val, col = point_light
            xml.append(f'{indent}\t<Item class="PointLight" referent="{l_ref}">\n')
            xml.append(f'{indent}\t\t<Properties>\n')
            xml.append(f'{indent}\t\t\t<string name="Name">PointLight</string>\n')
            xml.append(f'{indent}\t\t\t<float name="Brightness">{f_str(b_val)}</float>\n')
            xml.append(f'{indent}\t\t\t<float name="Range">{f_str(r_val)}</float>\n')
            xml.append(f'{indent}\t\t\t<Color3 name="Color"><R>{f_str(col[0])}</R><G>{f_str(col[1])}</G><B>{f_str(col[2])}</B></Color3>\n')
            xml.append(f'{indent}\t\t\t<bool name="Shadows">true</bool>\n')
            xml.append(f'{indent}\t\t\t<UniqueId name="UniqueId">{l_uid}</UniqueId>\n')
            xml.append(f'{indent}\t\t</Properties>\n')
            xml.append(f'{indent}\t</Item>\n')
            
        xml.append(f'{indent}</Item>\n')
        return "".join(xml)

    def model_open(self, name, indent="\t\t\t"):
        ref = self.next_ref()
        uid = self.next_uid()
        return (f'{indent}<Item class="Model" referent="{ref}">\n'
                f'{indent}\t<Properties>\n'
                f'{indent}\t\t<string name="Name">{name}</string>\n'
                f'{indent}\t\t<UniqueId name="UniqueId">{uid}</UniqueId>\n'
                f'{indent}\t</Properties>\n')

    def model_close(self, indent="\t\t\t"):
        return f'{indent}</Item>\n'

print("HouseUpgradeBuilder ready.")
