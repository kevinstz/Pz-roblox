import os

studio_dir = r"C:\Users\julia\AppData\Local\Roblox\Versions\version-7062aec9dbe74b14\content\pz42"
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"

hashes = [
    'a8a5c370590b10b7fab3',
    '9f722cda42b3e8299dab',
    '7b5a7835f5ededb9039b',
    'ff5ca3c4ea2334782a2f',
    '5b739f8939cb952826d4',
    'd658da83eeb812996967',
]

for h in hashes:
    f_out = os.path.join(out_dir, h + '.png')
    f_stu = os.path.join(studio_dir, h + '.png')
    print(f"{h}: out={os.path.exists(f_out)}, studio={os.path.exists(f_stu)}")
