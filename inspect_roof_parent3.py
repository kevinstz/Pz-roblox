with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

p_pos = 300491552
print(text[p_pos:p_pos+2500])
