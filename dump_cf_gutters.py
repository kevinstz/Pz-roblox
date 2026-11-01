with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

for ref in ['R133507', 'R133537', 'R133571', 'R133580']:
    idx = text.find(f'referent="{ref}"')
    block = text[idx:text.find('</Item>', idx)]
    cf = re.search(r'<CoordinateFrame name="CFrame">(.*?)</CoordinateFrame>', block, re.DOTALL)
    cf_txt = re.sub(r'\s+', ' ', cf.group(1)) if cf else "?"
    print(f"{ref}: {cf_txt}")
