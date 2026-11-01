# In frame 6, character is at:
# Let's project pixels (200, 900) onto the ground plane Y = 0 or roof plane Y = 7.0:
import numpy as np

# In frame 6, Bee was at screen (1208.7, 880.5)
# In Roblox viewport 1920x1080:
# Bee world position: let's find the exact ground position hit by ray through (1208.7, 880.5)
# If bee was at world (-21, 0, -45):
# Let's verify:
ISO_PITCH_DEG = -30.0
ISO_YAW_DEG = 45.0
CAMERA_DISTANCE = 115.0
FOV = 13.5

yaw = np.radians(ISO_YAW_DEG)
pitch = np.radians(ISO_PITCH_DEG)

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
look_vec = -R_cam[:, 2]

# If focus is focus_pos:
# ray through screen point (sx, sy):
W, H = 1920, 1080
tan_half_fov = np.tan(np.radians(FOV / 2.0))
focal_y = (H / 2.0) / tan_half_fov
focal_x = focal_y

def screen_to_ground(focus_pos, sx, sy, target_y=0.0):
    cam_pos = focus_pos - look_vec * CAMERA_DISTANCE
    nx = (sx - W / 2.0) / focal_x
    ny = -(sy - H / 2.0) / focal_y
    ray_dir_cam = np.array([nx, ny, -1.0])
    ray_dir_cam /= np.linalg.norm(ray_dir_cam)
    ray_dir_world = R_cam @ ray_dir_cam
    
    # intersect with Y = target_y:
    t = (target_y - cam_pos[1]) / ray_dir_world[1]
    hit = cam_pos + ray_dir_world * t
    return hit

# In frame 6, character is at focus:
# If bee is at screen (1208.7, 880.5) and focus is at character:
# Wait, if focus is at character, bee is at center (960, 540)!
# But bee is at (1208.7, 880.5)!
# That means camera is NOT centered on bee!
# In frame 6, where is the camera centered?
# Let's find focus_pos such that char at (-21, 0, -45) projects to (1208.7, 880.5):
# Let's solve for focus_pos:
# cam_pos = focus_pos - look_vec * D
# delta = hit - char_pos
focus_0 = np.array([-21.0, 0.0, -45.0])
hit_bee = screen_to_ground(focus_0, 1208.7, 880.5, target_y=0.0)
# So if focus is shifted by (focus_0 - hit_bee):
focus_f6 = focus_0 + (focus_0 - hit_bee)
print("Focus in frame 6:", focus_f6)

# Now what world point is at screen (250, 750) (lower left roof) at Y = 7.0?
hit_roof = screen_to_ground(focus_f6, 250, 750, target_y=7.0)
print("World point at screen (250, 750) Y=7.0:", hit_roof)

hit_wall = screen_to_ground(focus_f6, 250, 450, target_y=4.0)
print("World point at screen (250, 450) Y=4.0:", hit_wall)
