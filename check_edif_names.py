import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

# Let's check what buildings exist in Edificios and what their parts are
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find Edificios
m_edif = re.search(r'<string name="Name">Edificios</string>.*?</Item>', content, re.DOTALL)
if m_edif:
    print("Found Edificios folder")

# Find all Models directly inside Edificios
edif_block = content[content.find('<string name="Name">Edificios</string>'):]
# Find first closing of folder
bld_names = re.findall(r'<Item class="Model"[^>]*>\s*<Properties>.*?<string name="Name">([^<]+)</string>', edif_block[:50000])
print("Buildings found:", bld_names)
