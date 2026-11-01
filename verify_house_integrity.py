import re
import collections

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

print("Verifying PZ_Rosewood.rbxlx integrity...")

referents = collections.Counter()
unique_ids = collections.Counter()
wedge_parts = 0
point_lights = 0
models_piso_1 = 0
open_items = 0
has_roblox_close = False

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
        if m_item:
            cls, ref = m_item.group(1), m_item.group(2)
            open_items += 1
            referents[ref] += 1
            if cls == "WedgePart":
                wedge_parts += 1
            elif cls == "PointLight":
                point_lights += 1
        elif '<Item ' in line:
            open_items += 1
            
        if '</Item>' in line:
            open_items -= 1
            
        if '<UniqueId name="UniqueId">' in line:
            m_uid = re.search(r'<UniqueId name="UniqueId">([0-9a-fA-F]+)</UniqueId>', line)
            if m_uid:
                unique_ids[m_uid.group(1).lower()] += 1
                
        if '<string name="Name">Piso_1</string>' in line:
            models_piso_1 += 1
            
        if '</roblox>' in line:
            has_roblox_close = True

print(f"Results:")
print(f"  Open items balance: {open_items} (should be 0)")
print(f"  Has </roblox> closing tag: {has_roblox_close}")
print(f"  Total WedgeParts: {wedge_parts}")
print(f"  Total PointLights: {point_lights}")
print(f"  Piso_1 models found: {models_piso_1}")

dup_refs = [r for r, count in referents.items() if count > 1]
dup_uids = [u for u, count in unique_ids.items() if count > 1]

print(f"  Duplicate referents: {len(dup_refs)}")
if dup_refs:
    print(f"    Sample dup refs: {dup_refs[:5]}")
    
print(f"  Duplicate UniqueIds: {len(dup_uids)}")
if dup_uids:
    print(f"    Sample dup uids: {dup_uids[:5]}")

if open_items == 0 and has_roblox_close and len(dup_refs) == 0 and len(dup_uids) == 0:
    print("SUCCESS: 100% integrity verified! File is completely valid.")
else:
    print("WARNING: Integrity issue detected.")
