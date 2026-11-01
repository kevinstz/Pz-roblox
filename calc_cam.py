import math

# Pitch = -30 deg, Distance = 115 studs to focusPos (Y=0)
# Height of camera: 115 * sin(30 deg) = 57.5 studs
# Ground distance along look ray:
# Ground is at Y=0. Ray starts at Y=57.5, points down at 30 deg.
# At focusPos, distance along ray = 115 studs.
# FOV = 13.5 deg (vertical FOV in Roblox!)
# Top of screen is at angle -30 + 13.5/2 = -23.25 deg from horizontal!
# Distance along top ray to ground (Y=0):
# 57.5 / sin(23.25 deg) = 57.5 / 0.3947 = 145.7 studs!
# Distance on ground from focusPos:
dist_top_ray = 57.5 / math.sin(math.radians(23.25))
ground_x_top = 57.5 / math.tan(math.radians(23.25))
ground_x_focus = 57.5 / math.tan(math.radians(30.0))
print(f"Distance to focusPos along ray: 115.0 studs")
print(f"Distance to ground at top ray: {dist_top_ray:.1f} studs")
print(f"Ground distance beyond player: {ground_x_top - ground_x_focus:.1f} studs")
