import numpy as np

# Let's project from the parking lot between Libreria and Office:
# Cars are at (69, -66) and (90, -66)
focus_pos = np.array([80.0, 0.0, -66.0])

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

# Blue car at (69, 1.5, -66)
# Black car at (90, 1.5, -66)
print("Blue car (69, 1.5, -66):", project(np.array([69.0, 1.5, -66.0])))
print("Black car (90, 1.5, -66):", project(np.array([90.0, 1.5, -66.0])))
