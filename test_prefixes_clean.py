rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_ground"

prefixes_to_test = ["f70000000000000000000001", "f70000000000000000000002", "a00000000000000000000001", "700000000000000000000001"]

found = {p: 0 for p in prefixes_to_test}
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        for p in prefixes_to_test:
            if p in line:
                found[p] += 1

print("Found occurrences:", found)
