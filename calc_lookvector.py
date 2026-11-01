import math
import numpy as np

# In Roblox:
# CFrame.Angles(0, rad(45), 0) * CFrame.Angles(rad(-30), 0, 0)
# Let's compute rotation matrix R = Ry(45) * Rx(-30)
yaw = math.radians(45)
pitch = math.radians(-30)

Ry = np.array([
    [math.cos(yaw), 0, math.sin(yaw)],
    [0, 1, 0],
    [-math.sin(yaw), 0, math.cos(yaw)]
])

Rx = np.array([
    [1, 0, 0],
    [0, math.cos(pitch), -math.sin(pitch)],
    [0, math.sin(pitch), math.cos(pitch)]
])

R = Ry @ Rx
# LookVector is -Z column of R in Roblox!
# In Roblox CFrame, forward is -Z!
lookVector = -R[:, 2]
print("LookVector:", lookVector)

cam_dist = 115.0
focus = np.array([0, 3, 0])
camPos = focus - lookVector * cam_dist
print("camPos:", camPos)
