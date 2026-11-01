rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    chunk_count = 0
    modes = {}
    for line in f:
        if '<Item class="Model"' in line and 'Chunk_' in line:
            chunk_count += 1
        if '<token name="ModelStreamingMode">' in line:
            mode = line.strip()
            modes[mode] = modes.get(mode, 0) + 1
            if len(modes) < 5:
                pass
    print(f"Total ModelStreamingMode tokens: {modes}")
    print(f"Total Chunk models: {chunk_count}")
