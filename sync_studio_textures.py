import os
import shutil

src_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"
roots = [
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Roblox", "Versions"),
    os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Roblox", "Versions"),
    os.path.join(os.environ.get("ProgramFiles", ""), "Roblox", "Versions")
]

dest_dirs = []
for r in roots:
    if os.path.exists(r):
        for d in os.listdir(r):
            full_d = os.path.join(r, d)
            if os.path.isdir(full_d):
                pz42 = os.path.join(full_d, "content", "pz42")
                if os.path.exists(pz42):
                    dest_dirs.append(pz42)

print(f"Found {len(dest_dirs)} Studio content/pz42 directories:")
for dd in dest_dirs:
    print(" ", dd)

for fn in ["28f483ee7d0736992bde.png", "334d48f51be74b5e9e1a.png", "e6f1472b169f9a674721.png",
           "f897bb35b4c9b00e4359.png", "109d70ae137a46eff0bd.png", "7557fa72aaf5e0e0799a.png"]:
    sp = os.path.join(src_dir, fn)
    for dd in dest_dirs:
        dp = os.path.join(dd, fn)
        shutil.copy2(sp, dp)
        print(f"Copied {fn} -> {dp}")
