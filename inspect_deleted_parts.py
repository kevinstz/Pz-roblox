import re

bak_path = r"out\PZ_Rosewood.rbxlx.bak_turn11"
cur_path = r"out\PZ_Rosewood.rbxlx"

with open(bak_path, "r", encoding="utf-8", errors="ignore") as f:
    bak_text = f.read()

with open(cur_path, "r", encoding="utf-8", errors="ignore") as f:
    cur_text = f.read()

print(f"Bak len: {len(bak_text)}, Cur len: {len(cur_text)}")

# Let's find all referents that exist in bak but not in cur:
bak_refs = set(re.findall(r'<Item class="[^"]+" referent="([^"]+)">', bak_text))
cur_refs = set(re.findall(r'<Item class="[^"]+" referent="([^"]+)">', cur_text))

deleted = bak_refs - cur_refs
print(f"Total deleted referents: {len(deleted)}")

# For each deleted referent, find its Name and Class in bak_text:
for ref in sorted(deleted):
    idx = bak_text.find(f'referent="{ref}"')
    if idx != -1:
        end = bak_text.find('</Item>', idx)
        block = bak_text[idx:end]
        m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
        m_cls = re.search(r'<Item class="([^"]+)"', bak_text[max(0, idx-50):idx+30])
        name = m_name.group(1) if m_name else "Unknown"
        cls = m_cls.group(1) if m_cls else "Unknown"
        print(f"Deleted: {ref:8s} | Cls={cls:10s} | Name={name}")
