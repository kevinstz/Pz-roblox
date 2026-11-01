import math
import numpy as np

# Roblox IsometricCamera:
# focusPos = rootPart.Position (say car position: (-21, 0, -48))
# ISO_PITCH_DEG = -30.0
# ISO_YAW_DEG = 45.0
# CAMERA_DISTANCE = 115.0
# BASE_FOV = 13.5 (vertical FOV)

def project(pos, focus=(-21, 0, -48), viewport=(1920, 1080)):
    fx, fy, fz = focus
    pitch = math.radians(-30.0)
    yaw = math.radians(45.0)
    
    # CFrame rotation = Angles(0, yaw, 0) * Angles(pitch, 0, 0)
    # Rotation matrix:
    # R_yaw:
    # [cos(y)  0  sin(y)]
    # [0       1  0     ]
    # [-sin(y) 0  cos(y)]
    # R_pitch:
    # [1  0        0       ]
    # [0  cos(p)  -sin(p)  ]
    # [0  sin(p)   cos(p)  ]
    Cy, Sy = math.cos(yaw), math.sin(yaw)
    Cp, Sp = math.cos(pitch), math.sin(pitch)
    
    # R = R_yaw @ R_pitch:
    # col 0 (RightVector): [Cy, 0, -Sy]
    # col 1 (UpVector):    [Sy*Sp, Cp, Cy*Sp]
    # col 2 (-LookVector): [-Sy*Cp, Sp, -Cy*Cp]  Wait! In Roblox:
    # LookVector is -col 2: [Sy*Cp, -Sp, Cy*Cp] (pointing along look dir)
    # With pitch = -30: Sp = -0.5, Cp = 0.866.
    # LookVector = [0.7071 * 0.866, -(-0.5), 0.7071 * 0.866] = [0.6124, 0.5, 0.6124] ???
    # WAIT! In Roblox CFrame.Angles(p, y, r):
    # CFrame.Angles(0, math.rad(45), 0) * CFrame.Angles(math.rad(-30), 0, 0)
    pass

# Let us use Roblox matrix definition:
def get_cam_cframe(focus=(-21, 0, -48)):
    # In Roblox:
    # Angles(0, rad(45), 0):
    # R00=cos(45), R02=sin(45), R20=-sin(45), R22=cos(45)
    # Multiplied by Angles(rad(-30), 0, 0):
    # pitch around X axis: Y' = Y*cos(-30) - Z*sin(-30), Z' = Y*sin(-30) + Z*cos(-30)
    # Let us compute the 3x3 matrix:
    r_yaw = np.array([
        [math.cos(math.radians(45)), 0, math.sin(math.radians(45))],
        [0, 1, 0],
        [-math.sin(math.radians(45)), 0, math.cos(math.radians(45))]
    ])
    r_pitch = np.array([
        [1, 0, 0],
        [0, math.cos(math.radians(-30)), -math.sin(math.radians(-30))],
        [0, math.sin(math.radians(-30)), math.cos(math.radians(-30))]
    ])
    R = r_yaw @ r_pitch
    # LookVector in Roblox is -R[:, 2] (the negative Z column!)
    look = -R[:, 2]
    # camPos = focusPos - look * 115
    cam_pos = np.array(focus) - look * 115.0
    return cam_pos, R

cam_pos, R = get_cam_cframe((-21, 0, -48))
look = -R[:, 2]
right = R[:, 0]
up = R[:, 1]
print("Cam pos:", cam_pos)
print("LookVector:", look)
print("RightVector:", right)
print("UpVector:", up)

# Test project a point:
def to_screen(pt, focus=(-21, 0, -48), W=1920, H=1080, fov_deg=13.5):
    cam_pos, R = get_cam_cframe(focus)
    diff = np.array(pt) - cam_pos
    # Camera space coords:
    # X_cam = dot(diff, right)
    # Y_cam = dot(diff, up)
    # Z_cam = dot(diff, -look) (depth into screen is -Z_cam)
    depth = np.dot(diff, -R[:, 2]) # along look vector
    xc = np.dot(diff, R[:, 0])
    yc = np.dot(diff, R[:, 1])
    # Perspective projection:
    half_fov = math.radians(fov_deg / 2.0)
    # tan(half_fov) = (H/2) / focal_length
    focal = (H / 2.0) / math.tan(half_fov)
    screen_x = (W / 2.0) + (xc / depth) * focal
    screen_y = (H / 2.0) - (yc / depth) * focal
    return screen_x, screen_y, depth

print("Car Sedan (-21, 1.95, -60) -> screen:", to_screen((-21, 1.95, -60)))
print("Car Familiar (-21, 1.95, -36) -> screen:", to_screen((-21, 1.95, -36)))
print("Corner wall (-46.4, 3.7, -67.4) -> screen:", to_screen((-46.4, 3.7, -67.4)))
print("Building Knox Bank? (-10, 10, -80) -> screen:", to_screen((-10, 10, -80)))
