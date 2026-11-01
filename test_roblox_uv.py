# Test orientation of Roblox Top Face Texture
# In Roblox, on a part with CFrame = CFrame.new(pos) (identity orientation):
# LookVector = (0, 0, -1) (pointing North in our PZ world!)
# RightVector = (1, 0, 0) (pointing East in our PZ world!)
# UpVector = (0, 1, 0) (pointing Up in our PZ world!)

# When Face = Top:
# In Roblox documentation for Texture:
# "For the Top face, the top edge of the texture points towards -Z, and the right edge points towards +X."
# Let's verify:
# Top edge of texture: V = 0
# Bottom edge of texture: V = 1
# Left edge of texture: U = 0
# Right edge of texture: U = 1

# Therefore:
# U=0 -> -X (West)
# U=1 -> +X (East)
# V=0 -> -Z (North)
# V=1 -> +Z (South)

print("Roblox Top face Texture mapping:")
print("  (U=0, V=0) [Top-Left of image]     -> (-X, -Z) [North-West corner]")
print("  (U=1, V=0) [Top-Right of image]    -> (+X, -Z) [North-East corner]")
print("  (U=0, V=1) [Bottom-Left of image]  -> (-X, +Z) [South-West corner]")
print("  (U=1, V=1) [Bottom-Right of image] -> (+X, +Z) [South-East corner]")
