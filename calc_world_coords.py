import math
import numpy as np

# In dense_10_2.83s.jpg, the bee avatar is at (x=964, y=661) on 1920x1080 screen
# Screen center is (960, 540)
# So the bee is slightly right (+4 px) and below center (+121 px).
# The camera looks at focusPos = rootPart.Position + aimCursorLookOffset
# Let's say focusPos is roughly the player position.
# Camera:
# Yaw = 45 deg, Pitch = -30 deg
# CFrame = CFrame.lookAt(camPos, focusPos)
# Distance = 115.0 studs
# FOV = 13.5 deg (vertical)

# Aspect ratio = 1920 / 1080 = 1.77778
# Vertical FOV = 13.5 deg = 0.2356 rad
# Horizontal FOV = 2 * atan(tan(13.5/2) * 16/9) = 23.77 deg

# Let's find the world position of the disappearing region!
# What parts in PZ_Rosewood.rbxlx match that region?
# Let's check the Z range of the parts in that area:
# In isometric PZ projection:
# Pitch = -30 deg looking towards (-X, -Z).
# Things further away from camera (upper on screen) have MORE NEGATIVE X and MORE NEGATIVE Z!
# Or depending on yaw:
# Yaw = 45 deg, Pitch = -30 deg:
# Camera LookVector:
# LookVector = Vector3(-sin(45)*cos(-30), sin(-30), -cos(45)*cos(-30))
# Let's verify exact LookVector in Roblox!
