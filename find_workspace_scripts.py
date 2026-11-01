import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's find what is inside Workspace referent R1
match = re.search(r'<Item class="Workspace" referent="R1">.*?</Properties>', content, re.DOTALL)
if match:
    print(match.group(0)[:1000])

# Let's find any other scripts anywhere in the file
matches = re.findall(r'<Item class="(?:Script|LocalScript|ModuleScript)"[^>]*>.*?<string name="Name">([^<]+)</string>.*?</Item>', content, re.DOTALL)
print("All script items:", len(matches))
for m in matches:
    print("Script item:", m[:100])
