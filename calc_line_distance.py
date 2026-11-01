import math
import numpy as np

# Camera at camPos, looking along LookVector
# Let's compute ray for pixel (x=960, y=290) on 1920x1080 screen
# Screen center is (960, 540)
# dy = 540 - 290 = +250 pixels UP from center
# Screen height = 1080
# Vertical FOV = 13.5 deg = 0.235619 rad
# Angle per pixel = vertical_fov / 1080 rad = 0.235619 / 1080 = 0.000218166 rad
# Offset angle up = 250 * 0.000218166 = 0.05454 rad = 3.125 deg

# Since camera pitch is -30 deg, looking up by 3.125 deg gives pitch = -26.875 deg!
# Camera height above ground = 60.5 - (-1.5) = 62.0 studs!
h = 62.0
dist_ground = h / math.tan(math.radians(26.875))
dist_cam = h / math.sin(math.radians(26.875))

print(f"Ground distance from camera ground projection: {dist_ground:.1f} studs")
print(f"Distance from camera to line: {dist_cam:.1f} studs")

# Distance from PLAYER (who is at cam_dist=115 along LookVector, i.e. 115*cos(30) = 99.6 studs from camera projection):
player_dist_ground = 115.0 * math.cos(math.radians(30))
print(f"Ground distance from player to line: {dist_ground - player_dist_ground:.1f} studs")
