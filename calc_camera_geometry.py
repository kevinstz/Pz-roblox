import math

# Camera parameters
pitch = math.radians(-30.0) # 30 deg down
cam_dist = 115.0
cam_h = cam_dist * math.sin(math.radians(30.0)) # 57.5 studs above focus
fov_deg = 13.5
fov_rad = math.radians(fov_deg)

# In perspective camera, the vertical half-angle is fov/2 = 6.75 deg.
# The ray through the top of the viewport has pitch = -30 + 6.75 = -23.25 degrees!
# The ray through the bottom of the viewport has pitch = -30 - 6.75 = -36.75 degrees!

top_ray_pitch = math.radians(-30.0 + 6.75) # -23.25 deg
bot_ray_pitch = math.radians(-30.0 - 6.75) # -36.75 deg

# Distance along ground from camera's ground projection:
# ground_dist = cam_h / tan(pitch_angle)
dist_ground_center = 57.5 / math.tan(math.radians(30.0)) # 99.6 studs
dist_ground_bot    = 57.5 / math.tan(math.radians(36.75)) # 77.0 studs
dist_ground_top    = 57.5 / math.tan(math.radians(23.25)) # 133.8 studs

# Distance from CAMERA EYE to ground:
dist_eye_center = 57.5 / math.sin(math.radians(30.0)) # 115.0 studs
dist_eye_bot    = 57.5 / math.sin(math.radians(36.75)) # 96.1 studs
dist_eye_top    = 57.5 / math.sin(math.radians(23.25)) # 145.7 studs

print(f"Center eye-to-ground distance: {dist_eye_center:.1f} studs")
print(f"Bottom eye-to-ground distance: {dist_eye_bot:.1f} studs")
print(f"Top eye-to-ground distance:    {dist_eye_top:.1f} studs")
