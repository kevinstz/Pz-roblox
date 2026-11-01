import cv2
import os

video_path = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\.user_uploaded\media_1793313980817_8ff44bf5.mp4"
cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
duration = total_frames / fps
print(f"Total frames: {total_frames}, FPS: {fps:.2f}, Duration: {duration:.2f}s")

# Let's read every 10th frame:
frame_idx = 0
step = max(1, int(fps / 5)) # 5 frames per second

out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\video3_5fps"
os.makedirs(out_dir, exist_ok=True)

saved_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx % step == 0:
        t = frame_idx / fps
        cv2.imwrite(f"{out_dir}\\f_{saved_count:03d}_{t:.2f}s.jpg", frame)
        saved_count += 1
    frame_idx += 1

cap.release()
print(f"Extracted {saved_count} frames to {out_dir}")
