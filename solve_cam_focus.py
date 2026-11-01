import numpy as np

# Blue car is at (69, 1.5, -66) -> screen (1100, 380)
# Black car is at (90, 1.5, -66) -> screen (1360, 490)

ISO_PITCH_DEG = -30.0
ISO_YAW_DEG = 45.0
CAMERA_DISTANCE = 115.0
BASE_FOV = 13.5

yaw = np.radians(ISO_YAW_DEG)
pitch = np.radians(ISO_PITCH_DEG)

look = np.array([-np.sin(yaw) * np.cos(pitch), np.sin(pitch), -np.cos(yaw) * np.cos(pitch)])
look = look / np.linalg.norm(look)

up_world = np.array([0.0, 1.0, 0.0])
right = np.cross(look, up_world)
right = right / np.linalg.norm(right)
up = np.cross(right, look)
up = up / np.linalg.norm(up)

# In isometric/telephoto (FOV=13.5 deg, dist=115):
# u - 960 = dot(pt - focus, right) * factor_u
# v - 540 = - dot(pt - focus, up) * factor_v
factor_u = 960.0 / (CAMERA_DISTANCE * np.tan(np.radians(BASE_FOV / 2.0)) * (16.0 / 9.0))
factor_v = 540.0 / (CAMERA_DISTANCE * np.tan(np.radians(BASE_FOV / 2.0)))

# For Blue car: pt = (69, 1.5, -66), u = 1100, v = 380
# dot(pt - focus, right) = (1100 - 960) / factor_u = 140 / 39.673 = 3.5289
# dot(pt - focus, up) = -(380 - 540) / factor_v = 160 / 39.673 = 4.033

# Let pt = (69, 1.5, -66). Let focus = (Fx, 0, Fz):
# pt - focus = (69 - Fx, 1.5, -66 - Fz)
# dot with right: (69 - Fx - (-66 - Fz)) * sqrt(0.5) = (135 - Fx + Fz) * 0.7071 = 3.5289
# 135 - Fx + Fz = 4.9907 => Fx - Fz = 130.009

# dot with up: -0.35355*(69 - Fx) + 0.86603*(1.5) - 0.35355*(-66 - Fz) = 4.033
# -0.35355*(135 - Fx - Fz) + 1.299 = 4.033
# -0.35355*(135 - Fx - Fz) = 2.734 => 135 - Fx - Fz = -7.733 => Fx + Fz = 142.733

# From Fx - Fz = 130 and Fx + Fz = 142.7:
# 2*Fx = 272.7 => Fx = 136.35
# Fz = 6.35!

Fx = 136.35
Fz = 6.35
focus = np.array([Fx, 0.0, Fz])
print(f"Solved Camera Focus: Fx = {Fx:.2f}, Fz = {Fz:.2f}")

# Check spawn location from earlier:
# Spawn_Rosewood was at X = 129, Y = 0.1, Z = 168
# Wait, where was the character spawned?
