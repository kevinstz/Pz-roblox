with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<Vector3 name="size">' in line:
            block = [line] + [f.readline() for _ in range(4)]
            text = "".join(block)
            if '2.91' in text or '2.96' in text:
                print(repr(text))
                break
