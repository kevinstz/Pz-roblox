import numpy as np
import re

# In crop_v4_lower_left_roof.jpg:
# Frame 6 (2.90s), Bee is at (1208.7, 880.5)
# Let's project from char_pos = (-30, 0, -55) and find the exact parts in the gutter and fins:
char_pos = np.array([-30.0, 0.0, -55.0])

ISO_PITCH_DEG = -30.0
ISO_YAW_DEG = 45.0
CAMERA_DISTANCE = 115.0
FOV = 13.5

yaw = np.radians(ISO_YAW_DEG)
pitch = np.radians(ISO_PITCH_DEG)

R_yaw = np.array([
    [np.cos(yaw), 0, np.sin(yaw)],
    [0, 1, 0],
    [-np.sin(yaw), 0, np.cos(yaw)]
])

R_pitch = np.array([
    [1, 0, 0],
    [0, np.cos(pitch), -np.sin(pitch)],
    [0, np.sin(pitch), np.cos(pitch)]
])

R_cam = R_yaw @ R_pitch
look_vec = -R_cam[:, 2]

cam_pos = char_pos - look_vec * CAMERA_DISTANCE

R_w2c = R_cam.T
t_w2c = -R_w2c @ cam_pos

W, H = 1920, 1080
tan_half_fov = np.tan(np.radians(FOV / 2.0))
focal_y = (H / 2.0) / tan_half_fov
focal_x = focal_y

def project(world_pt):
    p_cam = R_w2c @ world_pt + t_w2c
    if p_cam[2] >= 0:
        return None
    sx = (W / 2.0) + (p_cam[0] / -p_cam[2]) * focal_x
    sy = (H / 2.0) - (p_cam[1] / -p_cam[2]) * focal_y
    return sx, sy, -p_cam[2]

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search all parts in the corner X in [-52, -44], Z in [-75, -65], Y in [5, 12]
matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
roof_pts = []
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -52 <= x <= -44 and -76 <= z <= -65 and 5.0 <= y <= 12.0:
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            proj = project(np.array([x, y, z]))
            roof_pts.append({
                'ref': ref, 'cls': cls, 'name': m_name.group(1),
                'pos': (x, y, z), 'size': sz, 'col': m_col.group(1) if m_col else '',
                'tex': m_tex, 'proj': proj
            })

roof_pts.sort(key=lambda p: (p['pos'][1], p['pos'][2]))
for p in roof_pts:
    print(f"Ref={p['ref']:8s} | Name={p['name']:30s} | Pos=({p['pos'][0]:6.2f}, {p['pos'][1]:6.2f}, {p['pos'][2]:6.2f}) | Size={p['size']} | Col={p['col']:10s} | Screen={p['proj'][:2] if p['proj'] else None} | Tex={p['tex']}")
