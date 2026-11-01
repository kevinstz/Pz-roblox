import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('referent="R39347"')
end_idx = text.find('referent="R116275"')
chunk = text[idx:end_idx]

# Items directly under Edificios (\n\t\t\t\t<Item class=...)
children = re.findall(r'\n\t\t\t\t<Item class="([^"]+)" referent="([^"]+)">', chunk)
print(f"Direct children of Edificios (R39347): {len(children)}")
for cls, ref in children:
    c_idx = text.find(f'referent="{ref}"')
    m_name = re.search(r'<string name="Name">([^<]+)</string>', text[c_idx:c_idx+1200])
    print(f"  {cls}: {m_name.group(1) if m_name else 'Unknown'} (ref: {ref})")
