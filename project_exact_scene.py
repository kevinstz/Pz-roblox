import numpy as np
import re

focus_pos = np.array([75.0, 0.0, -60.0])

ISO_PITCH_DEG = -30.0
ISO_YAW_DEG = 45.0
CAMERA_DISTANCE = 115.0
BASE_FOV = 13.5

yaw = np.radians(ISO_YAW_DEG)
pitch = np.radians(ISO_PITCH_DEG)

look = np.array([-np.sin(yaw) * np.cos(pitch), np.sin(pitch), -np.cos(yaw) * np.cos(pitch)])
look = look / np.linalg.norm(look)
cam_pos = focus_pos - look * CAMERA_DISTANCE

up_world = np.array([0.0, 1.0, 0.0])
right = np.cross(look, up_world)
right = right / np.linalg.norm(right)
up = np.cross(right, look)
up = up / np.linalg.norm(up)

def project(pt):
    d = pt - cam_pos
    x_cam = np.dot(d, right)
    y_cam = np.dot(d, up)
    z_cam = np.dot(d, look)
    aspect = 1920.0 / 1080.0
    u = (x_cam / (z_cam * np.tan(np.radians(BASE_FOV / 2.0)) * aspect)) * 960 + 960
    v = 540 - (y_cam / (z_cam * np.tan(np.radians(BASE_FOV / 2.0)))) * 540
    return u, v, z_cam

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# We want to find:
# 1. The parts projecting to [200, 500], [600, 950] (lower left roof & white door!)
# 2. The parts projecting to [800, 1400], [150, 450] (windows across street with brown sticks!)

screen_parts = []

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    hierarchy = []
    cur_p = {}
    
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)"', line)
        if m_item:
            hierarchy.append(m_item.group(1))
            cur_p = {'class': m_item.group(1), 'name': '', 'x': None, 'y': None, 'z': None, 'lines': [line]}
            continue
        if '</Item>' in line:
            if cur_p and cur_p.get('x') is not None and cur_p.get('z') is not None:
                x, y, z = cur_p['x'], cur_p['y'], cur_p['z']
                # only consider points near the camera frustum:
                # distance to focus < 90
                if np.linalg.norm(np.array([x, y, z]) - focus_pos) < 90:
                    u, v, depth = project(np.array([x, y, z]))
                    if 0 <= u <= 1920 and 0 <= v <= 1080 and depth > 10:
                        screen_parts.append((cur_p['name'], cur_p['class'], x, y, z, u, v, list(hierarchy[-3:]), "".join(cur_p['lines'])))
            if hierarchy:
                hierarchy.pop()
            cur_p = {}
            continue
            
        if '<string name="Name">' in line:
            name = line.split('>')[1].split('<')[0]
            if hierarchy:
                hierarchy[-1] = name
            if cur_p:
                cur_p['name'] = name
        if cur_p:
            cur_p['lines'].append(line)
            if '<X>' in line and cur_p['x'] is None:
                try: cur_p['x'] = float(line.split('>')[1].split('<')[0])
                except: pass
            if '<Y>' in line and cur_p['y'] is None:
                try: cur_p['y'] = float(line.split('>')[1].split('<')[0])
                except: pass
            if '<Z>' in line and cur_p['z'] is None:
                try: cur_p['z'] = float(line.split('>')[1].split('<')[0])
                except: pass

print(f"Total parts in screen frustum: {len(screen_parts)}")

# Look for the white door / frame (u in 600..750, v in 650..850)
print("\n--- PARTS AT LOWER-LEFT WHITE DOOR / ROOF (u: 300..800, v: 600..950) ---")
for p in screen_parts:
    u, v = p[5], p[6]
    if 300 <= u <= 800 and 600 <= v <= 950:
        # filter to unique types or interesting names
        print(f"Name: {p[0]} ({p[1]}) at pos=({p[2]:.1f}, {p[3]:.1f}, {p[4]:.1f}) -> (u={u:.0f}, v={v:.0f}) | parent={p[7]}")

# Look for brown sticks / diagonal parts (u in 850..1300, v in 180..400)
print("\n--- PARTS AT ACROSS-STREET WINDOWS (u: 850..1300, v: 180..400) ---")
for p in screen_parts:
    u, v = p[5], p[6]
    if 850 <= u <= 1300 and 180 <= v <= 400:
        pname = p[0].lower()
        # look for stick, tree, wedge, branch, railing, pole, etc.
        print(f"Name: {p[0]} ({p[1]}) at pos=({p[2]:.1f}, {p[3]:.1f}, {p[4]:.1f}) -> (u={u:.0f}, v={v:.0f}) | parent={p[7]}")
