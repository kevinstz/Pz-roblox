with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

for ref in ['R133837', 'R133846', 'R131081']:
    idx = text.find(f'referent="{ref}"')
    block = text[idx:text.find('</Item>', idx)+7]
    print(f"=== {ref} ===")
    print(block[:1000])
