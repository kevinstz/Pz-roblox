import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's find each script's parents and full context
for match in re.finditer(r'<Item class="(?:Script|LocalScript)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>', content, re.DOTALL):
    ref, name = match.groups()
    # find where this item is
    start_pos = match.start()
    # search backwards for parent Item
    sub = content[max(0, start_pos - 1000):start_pos]
    parents = re.findall(r'<Item class="([^"]+)" referent="([^"]+)">', sub)
    parent_str = " -> ".join([p[0] for p in parents[-3:]]) if parents else "root"
    print(f"Script {name} (ref={ref}) parent path: {parent_str}")
