import re

def find_item_bounds(text, ref):
    pattern = f'<Item class="[^"]+" referent="{ref}">'
    m = re.search(pattern, text)
    if not m:
        return None, None
    start = m.start()
    pos = m.end()
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = text.find('<Item', pos)
        next_close = text.find('</Item>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 7
            if depth == 0:
                if pos < len(text) and text[pos] == '\r': pos += 1
                if pos < len(text) and text[pos] == '\n': pos += 1
                return start, pos
    return None, None

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Test on R91073 (has child Decal R91074)
s, e = find_item_bounds(text, 'R91073')
print(f"R91073 bounds: {s}..{e} (len: {e-s if s else 0})")
if s is not None:
    block = text[s:e]
    print("Contains R91074?", 'R91074' in block)
    print("Ends with </Item>?", block.strip().endswith('</Item>'))
    print("Number of open Items:", block.count('<Item'))
    print("Number of close Items:", block.count('</Item>'))
