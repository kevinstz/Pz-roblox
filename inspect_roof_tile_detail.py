import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect a sample roofs_30_06_26 part
idx = text.find('<string name="Name">roofs_30_06_26</string>')
if idx != -1:
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    # find end of part (depth matching)
    pos = item_start + 10
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = text.find('<Item', pos)
        next_close = text.find('</Item>', pos)
        if next_close == -1: break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 7
    print("Sample roofs_30_06_26:")
    print(text[item_start:pos])
