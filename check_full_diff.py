import cv2
import numpy as np

f10 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_10_raw.jpg")
f11 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_11_raw.jpg")

diff = np.abs(f10.astype(float) - f11.astype(float)).mean(axis=2)
mask = diff > 15

# Check regions of diff
print("Diff on entire screen:", mask.sum(), "pixels")

# Check if File Explorer changed (x: 500..1500, y: 100..700)
print("Diff in Explorer window area:", mask[100:700, 500:1500].sum())

# Check if Viewport changed (x: 0..1500, y: 150..890)
print("Diff in Viewport area:", mask[150:890, 0:1500].sum())

# Check if Studio UI (top bar, explorer pane, properties) changed
print("Diff in Studio Top Bar (y: 0..150):", mask[0:150, :].sum())
print("Diff in Studio Right Panes (x: 1500..1920):", mask[:, 1500:].sum())
