# Test floor_image affine transform
# size = 128
size = 128
k = 128.0 / size # = 1.0
# x_src = 0.5 * k * x_out - 0.5 * k * y_out + 64.0
# y_src = 0.25 * k * x_out + 0.25 * k * y_out + 192.0

corners = [
    ("Top-Left (0, 0)", 0, 0),
    ("Top-Right (128, 0)", 128, 0),
    ("Bottom-Left (0, 128)", 0, 128),
    ("Bottom-Right (128, 128)", 128, 128),
]

for name, xo, yo in corners:
    xs = 0.5 * k * xo - 0.5 * k * yo + 64.0
    ys = 0.25 * k * xo + 0.25 * k * yo + 192.0
    print(f"{name:25} -> src: ({xs:6.1f}, {ys:6.1f})")
