with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

for ref in ['R133562', 'R133568']:
    idx = text.find(f'referent="{ref}"')
    end = text.find('</Item>', idx)
    print(f"=== {ref} ===")
    print(text[idx:end+7])
