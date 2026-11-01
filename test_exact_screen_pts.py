import numpy as np

# Camera focus near the blue car and black car:
# Blue car at (69, -66), Black car at (90, -66)
# In frame 006, the character was at roughly (75, 0, -66)
focus_pos = np.array([75.0, 0.0, -66.0])

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

# Test candidate parts:
pts = [
    ("roofs_shallow_01_102", np.array([105.00, 11.64, -93.00])),
    ("roofs_accents_01_8", np.array([109.95, 9.52, -91.12])),
    ("roofs_accents_01_17", np.array([105.64, 8.71, -87.57])),
    ("roofs_accents_01_19", np.array([110.01, 8.38, -87.89])),
    ("trashcontainers_01_9", np.array([117.0, 2.2, -89.6])),
    ("second_floor_window", np.array([115.57, 11.02, -87.00])),
]

for name, pt in pts:
    u, v, z = project(pt)
    print(f"{name} at {pt} -> u={u:.1f}, v={v:.1f}")
