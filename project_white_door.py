import numpy as np
import re

ISO_PITCH_DEG = -30.0
ISO_YAW_DEG = 45.0
CAMERA_DISTANCE = 115.0
BASE_FOV = 13.5

# Focus near the character
focus_pos = np.array([-16.65, 0.0, -50.0])
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

# Scan PZ_Rosewood.rbxlx and find parts whose projected (u, v) is in [0, 800], [500, 1080] (the lower left foreground!)
rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    hierarchy = []
    current_part = {}
    found_parts = []
    
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)"', line)
        if m_item:
            hierarchy.append(m_item.group(1))
            current_part = {'class': m_item.group(1), 'name': '', 'x': None, 'y': None, 'z': None}
            continue
        if '</Item>' in line:
            if current_part and current_part.get('x') is not None and current_part.get('z') is not None:
                x, y, z = current_part['x'], current_part['y'], current_part['z']
                u, v, depth = project(np.array([x, y, z]))
                # Check if in foreground bottom-left: u in [500, 800], v in [600, 950] (where white door is!)
                if 550 <= u <= 800 and 650 <= v <= 900:
                    found_parts.append((current_part['name'], current_part['class'], x, y, z, u, v, hierarchy[-3:]))
            if hierarchy:
                hierarchy.pop()
            current_part = {}
            continue
            
        if '<string name="Name">' in line:
            name = line.split('>')[1].split('<')[0]
            if hierarchy:
                hierarchy[-1] = name
            if current_part:
                current_part['name'] = name
        if current_part:
            if '<X>' in line and '</X>' in line and current_part['x'] is None:
                try: current_part['x'] = float(line.split('>')[1].split('<')[0])
                except: pass
            elif '<Y>' in line and '</Y>' in line and current_part['y'] is None:
                try: current_part['y'] = float(line.split('>')[1].split('<')[0])
                except: pass
            elif '<Z>' in line and '</Z>' in line and current_part['z'] is None:
                try: current_part['z'] = float(line.split('>')[1].split('<')[0])
                except: pass

print(f"Total parts projecting to white door area: {len(found_parts)}")
for p in found_parts[:20]:
    print(p)
