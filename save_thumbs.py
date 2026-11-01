import cv2

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'
for i in [0, 4, 10, 11, 14, 20]:
    img = cv2.imread(f"{p_dir}\\dense_{i:02d}_{i*0.283:.2f}s.jpg")
    if img is not None:
        # save a 640x360 thumbnail
        thumb = cv2.resize(img, (640, 360))
        cv2.imwrite(rf'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\thumb_{i:02d}.jpg', thumb)
        print(f"Saved thumb_{i:02d}.jpg, overall mean BGR = {img.mean(axis=(0,1))}")
