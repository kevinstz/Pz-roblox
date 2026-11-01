import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

REMOVE_REFS = [
    'R133864', 'R133580', 'R133855',
    'R131872', 'R131875', 'R131878', 'R131881', 'R131884', 'R131887', 'R131890',
    'R131841', 'R131858'
]

def find_item_bounds(text, ref):
    pattern = f'<Item class="[^"]+" referent="{ref}">'
    m = re.search(pattern, text)
    if not m:
        return None, None
    start = m.start()
    
    # We find the matching </Item> by tracking open/close Item tags
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
                # also include trailing newline if present
                if pos < len(text) and text[pos] == '\r': pos += 1
                if pos < len(text) and text[pos] == '\n': pos += 1
                return start, pos
    return None, None

for ref in REMOVE_REFS:
    s, e = find_item_bounds(text, ref)
    block = text[s:e]
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    child_items = len(re.findall(r'<Item', block)) - 1
    print(f"Ref={ref:8s} | Range=({s:9d}, {e:9d}) | Len={e-s:5d} | Name={m_name.group(1):30s} | Children={child_items}")
