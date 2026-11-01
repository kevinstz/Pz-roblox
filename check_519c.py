import cv2
import numpy as np

img = cv2.imread(r'.\out\textures\519c46ad323a93d7bdf1.png', cv2.IMREAD_UNCHANGED)
print("519c shape:", img.shape)
print("519c mean BGR:", np.mean(img[:,:,:3], axis=(0,1)))
