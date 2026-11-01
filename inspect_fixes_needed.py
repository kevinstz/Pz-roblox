import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# House 33 remaining refs:
h33_rem = ['R140219', 'R140246', 'R140273', 'R140300', 'R140326', 'R140365', 'R140482', 'R140494', 'R140587', 'R140590', 'R140593', 'R140596', 'R140599']
print(f"H33 remaining refs in file: {[r for r in h33_rem if f'referent=\"{r}\"' in text]}")

# Let's check all roofs with CanCollide=false in file
false_roof_refs = []
for m in re.finditer(r'<Item class="([^"]+)" referent="(R\d+)">\s*<Properties>.*?'
                    r'<bool name="CanCollide">false</bool>.*?'
                    r'<string name="Name">([^<]*roof[^<]*)</string>', text, re.DOTALL):
    false_roof_refs.append((m.group(2), m.group(3)))

print(f"Total roof parts with CanCollide=false: {len(false_roof_refs)}")

# Let's check all Puerta_ parts with CanCollide=false
puertas_nocollide = []
for m in re.finditer(r'<Item class="([^"]+)" referent="(R\d+)">\s*<Properties>.*?'
                    r'<bool name="CanCollide">false</bool>.*?'
                    r'<string name="Name">(Puerta_[^<]+)</string>', text, re.DOTALL):
    puertas_nocollide.append((m.group(2), m.group(3)))

print(f"Total Puerta_ parts with CanCollide=false: {len(puertas_nocollide)}")

# Let's check all exterior walls with CanCollide=false
walls_nocollide = []
for m in re.finditer(r'<Item class="([^"]+)" referent="(R\d+)">\s*<Properties>.*?'
                    r'<bool name="CanCollide">false</bool>.*?'
                    r'<string name="Name">(walls_exterior_[^<]+|walls_commercial_[^<]+)</string>', text, re.DOTALL):
    walls_nocollide.append((m.group(2), m.group(3)))

print(f"Total exterior/commercial walls with CanCollide=false: {len(walls_nocollide)}")
