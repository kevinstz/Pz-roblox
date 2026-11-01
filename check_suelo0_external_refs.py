import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
suelo0_refs = set()
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        line_no = idx + 1
        if 50439 <= line_no <= 2357376:
            m = re.findall(r'referent="([^"]+)"', line)
            for r in m:
                suelo0_refs.add(r)

print(f"Total referents defined inside Suelo_Piso_0: {len(suelo0_refs)}")

# Now scan entire file OUTSIDE 50439..2357376 to see if any referent in suelo0_refs is referenced
external_refs = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        line_no = idx + 1
        if 50439 <= line_no <= 2357376:
            continue
        m = re.findall(r'>([^<]+)</Ref>', line)
        for r in m:
            if r in suelo0_refs:
                print(f"External reference found at line {line_no}: {r}")
                external_refs += 1

print(f"Total external references to Suelo_Piso_0: {external_refs}")
