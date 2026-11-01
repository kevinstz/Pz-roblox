rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

single_line_items = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if '<Item' in line and ('/>' in line or '</Item>' in line):
            print(f"Single line item at {idx+1}: {line.strip()}")
            single_line_items += 1
            if single_line_items > 5:
                break

print("Total single line items:", single_line_items)
