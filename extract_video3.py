import cv2
import os

video_path = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\.user_uploaded\media_1793313980817_8ff44bf5.mp4"
out_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames"
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = total_frames / fps if fps > 0 else 0

print(f"Video info: {width}x{height}, FPS: {fps:.2f}, Frames: {total_frames}, Duration: {duration:.2f}s")

# Extract 1 frame per second or up to 20 frames
interval = max(1, int(fps))
frame_idx = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx % interval == 0 or frame_idx == total_frames - 1:
        sec = frame_idx / fps
        fn = os.path.join(out_dir, f"frame_{saved_count:03d}_{sec:.2f}s.jpg")
        cv2.imwrite(fn, frame)
        saved_count += 1
    frame_idx += 1

cap.release()
print(f"Saved {saved_count} frames to {out_dir}")
