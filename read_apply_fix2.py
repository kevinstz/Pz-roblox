with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\apply_ground_fix.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(100, min(250, len(lines))):
    print(lines[i], end="")
