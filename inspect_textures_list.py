import os

tex_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"
files = [f for f in os.listdir(tex_dir) if f.endswith(".png")]
print(f"Total textures in out/textures: {len(files)}")

roof_tex = [f for f in files if "roof" in f.lower()]
wall_tex = [f for f in files if "wall" in f.lower()]
wood_tex = [f for f in files if "wood" in f.lower() or "carpentry" in f.lower()]
floor_tex = [f for f in files if "floor" in f.lower() or "tile" in f.lower()]

print(f"Roof textures ({len(roof_tex)}):", roof_tex[:10])
print(f"Wall textures ({len(wall_tex)}):", wall_tex[:10])
print(f"Wood textures ({len(wood_tex)}):", wood_tex[:10])
print(f"Floor textures ({len(floor_tex)}):", floor_tex[:10])
