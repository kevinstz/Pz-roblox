import numpy as np
import re

# Character position in v4 (parking lot):
char_pos = np.array([-21.0, 0.0, -45.0])

# Camera parameters from IsometricCamera script:
ISO_PITCH_DEG = -30.0
ISO_YAW_DEG = 45.0
CAMERA_DISTANCE = 115.0
FOV = 13.5  # degrees vertical FOV

# Rotation matrix:
yaw = np.radians(ISO_YAW_DEG)
pitch = np.radians(ISO_PITCH_DEG)

# CFrame.Angles(0, yaw, 0) * CFrame.Angles(pitch, 0, 0)
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
look_vec = -R_cam[:, 2] # in Roblox -Z is forward

cam_pos = char_pos - look_vec * CAMERA_DISTANCE

# World to Camera matrix:
R_w2c = R_cam.T
t_w2c = -R_w2c @ cam_pos

# Viewport: 1920x1080
W, H = 1920, 1080
tan_half_fov = np.tan(np.radians(FOV / 2.0))
focal_y = (H / 2.0) / tan_half_fov
focal_x = focal_y # square pixels

def project(world_pt):
    p_cam = R_w2c @ world_pt + t_w2c
    # In Roblox camera coords: p_cam[2] is negative for in front of camera
    if p_cam[2] >= 0:
        return None
    # x_screen = cx + x_cam / -z_cam * focal_x
    # y_screen = cy - y_cam / -z_cam * focal_y
    sx = (W / 2.0) + (p_cam[0] / -p_cam[2]) * focal_x
    sy = (H / 2.0) - (p_cam[1] / -p_cam[2]) * focal_y
    return sx, sy, -p_cam[2]

# Let's read all parts in out/PZ_Rosewood.rbxlx and project them
with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
screen_parts = []
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        proj = project(np.array([x, y, z]))
        if proj:
            sx, sy, dist = proj
            # Is it on screen?
            if 0 <= sx <= W and 0 <= sy <= H:
                screen_parts.append({
                    'ref': ref, 'cls': cls, 'name': m_name.group(1),
                    'pos': (x, y, z), 'screen': (sx, sy), 'dist': dist,
                    'col': m_col.group(1) if m_col else '',
                    'tex': m_tex
                })

print(f"Total parts on screen: {len(screen_parts)}")

# Filter parts in v4_tile_r1_c0 (sx: 0..640, sy: 360..720)
tile_r1_c0 = [p for p in screen_parts if 0 <= p['screen'][0] <= 640 and 360 <= p['screen'][1] <= 720]
print(f"\n=== Parts in v4_tile_r1_c0 (x: 0..640, y: 360..720) count={len(tile_r1_c0)} ===")
tile_r1_c0.sort(key=lambda p: (p['screen'][1], p['screen'][0]))
for p in tile_r1_c0:
    print(f"Ref={p['ref']:8s} | Name={p['name']:30s} | Screen=({p['screen'][0]:6.1f}, {p['screen'][1]:6.1f}) | Pos=({p['pos'][0]:6.1f}, {p['pos'][1]:6.1f}, {p['pos'][2]:6.1f}) | Col={p['col']:10s} | Tex={p['tex']}")

# Filter parts in v4_tile_r2_c0 (sx: 0..640, sy: 720..1080)
tile_r2_c0 = [p for p in screen_parts if 0 <= p['screen'][0] <= 640 and 720 <= p['screen'][1] <= 1080]
print(f"\n=== Parts in v4_tile_r2_c0 (x: 0..640, y: 720..1080) count={len(tile_r2_c0)} ===")
tile_r2_c0.sort(key=lambda p: (p['screen'][1], p['screen'][0]))
for p in tile_r2_c0:
    print(f"Ref={p['ref']:8s} | Name={p['name']:30s} | Screen=({p['screen'][0]:6.1f}, {p['screen'][1]:6.1f}) | Pos=({p['pos'][0]:6.1f}, {p['pos'][1]:6.1f}, {p['pos'][2]:6.1f}) | Col={p['col']:10s} | Tex={p['tex']}")
