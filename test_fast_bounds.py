import time

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

def find_item_bounds_fast(text, ref):
    target = f'referent="{ref}"'
    ref_idx = text.find(target)
    if ref_idx == -1:
        return None, None
    # find '<Item ' before target
    item_start = text.rfind('<Item ', max(0, ref_idx - 500), ref_idx)
    if item_start == -1:
        return None, None
    # find matching </Item>
    pos = ref_idx + len(target)
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
                return item_start, pos
    return None, None

t0 = time.time()
for ref in ['R91073', 'R133577', 'R133562', 'R126859', 'R119849', 'R137569']:
    s, e = find_item_bounds_fast(text, ref)
    print(f"{ref}: {s}..{e} (len: {e-s if s else 0})")
print(f"Elapsed for 6 lookups: {time.time() - t0:.4f}s")
