import re
import uuid

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Find referents and UniqueIds to see current maximum
max_ref = 0
unique_ids = set()

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m_ref = re.search(r'referent="R(\d+)"', line)
        if m_ref:
            ref_num = int(m_ref.group(1))
            if ref_num > max_ref:
                max_ref = ref_num
        m_uid = re.search(r'<UniqueId name="UniqueId">([0-9a-fA-F]+)</UniqueId>', line)
        if m_uid:
            unique_ids.add(m_uid.group(1).lower())

print(f"Max referent found: R{max_ref}")
print(f"Total UniqueIds found: {len(unique_ids)}")
