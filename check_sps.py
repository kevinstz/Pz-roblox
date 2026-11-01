p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pos_sps = content.find('<string name="Name">StarterPlayerScripts</string>')
if pos_sps != -1:
    print("Found StarterPlayerScripts at pos:", pos_sps)
    # Print next 10,000 chars
    print(content[pos_sps:pos_sps+10000])
