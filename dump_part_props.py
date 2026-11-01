# Let us dump all properties of R133864
with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

for ref in ['R133864', 'R133580', 'R133571', 'R133855']:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        end = text.find('</Item>', idx)
        print(f"=== {ref} ===")
        print(text[idx:end+7])
