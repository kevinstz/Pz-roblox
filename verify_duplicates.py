import re
from collections import Counter

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

ref_counts = Counter()
uid_counts = Counter()

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m_ref = re.search(r'referent="([^"]+)"', line)
        if m_ref:
            ref_counts[m_ref.group(1)] += 1
        m_uid = re.search(r'<UniqueId name="UniqueId">([0-9a-fA-F]+)</UniqueId>', line)
        if m_uid:
            uid_counts[m_uid.group(1).lower()] += 1

dup_refs = {k: v for k, v in ref_counts.items() if v > 1}
dup_uids = {k: v for k, v in uid_counts.items() if v > 1}

print(f"Total Unique Referents: {len(ref_counts)}, Duplicates: {len(dup_refs)}")
if dup_refs:
    print("Sample duplicate referents:", list(dup_refs.items())[:5])

print(f"Total Unique UniqueIds: {len(uid_counts)}, Duplicates: {len(dup_uids)}")
if dup_uids:
    print("Sample duplicate UniqueIds:", list(dup_uids.items())[:5])
