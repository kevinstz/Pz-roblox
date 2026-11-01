import cv2
import os

video_path = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\.user_uploaded\media_1793313980817_8ff44bf5.mp4"
out_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

interval = max(1, int(fps * 0.3)) # Every ~0.3s
frame_idx = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx % interval == 0 or frame_idx == total_frames - 1:
        sec = frame_idx / fps
        fn = os.path.join(out_dir, f"dense_{saved_count:02d}_{sec:.2f}s.jpg")
        cv2.imwrite(fn, frame)
        saved_count += 1
    frame_idx += 1

cap.release()
print(f"Saved {saved_count} dense frames to {out_dir}")
