import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

r2_idx = text.find('referent="R2"')
props_end = text.find('</Properties>', r2_idx)

# Search across the whole file for direct children of R2 (\n\t\t\t<Item class=...)
matches = re.findall(r'\n\t\t\t<Item class="([^"]+)" referent="([^"]+)">', text)
print(f"Total direct children of R2: {len(matches)}")
for cls, ref in matches:
    idx = text.find(f'referent="{ref}"')
    m_name = re.search(r'<string name="Name">([^<]+)</string>', text[idx:idx+400])
    name = m_name.group(1) if m_name else "Unknown"
    print(f"  {cls}: {name} (ref: {ref})")
