with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\apply_ground_fix.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"apply_ground_fix.py has {len(lines)} lines")
for i in range(0, min(100, len(lines))):
    print(lines[i], end="")
