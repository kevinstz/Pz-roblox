import cv2
import numpy as np

img = cv2.imread('tex_67cf.png', cv2.IMREAD_UNCHANGED)
print("tex_67cf shape:", img.shape)
if img.shape[2] == 4:
    alpha = img[:,:,3]
    print("Min alpha:", np.min(alpha), "Max alpha:", np.max(alpha), "Mean alpha:", np.mean(alpha))
    # Count transparent vs opaque pixels
    opaque = np.sum(alpha > 200)
    transp = np.sum(alpha < 50)
    print("Opaque pixels:", opaque, "Transparent pixels:", transp)
