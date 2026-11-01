import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

WEST_REFS = [
    'R91073', 'R91522', 'R91781', 'R92150', 'R92334', 'R92933', 'R93272',
    'R133559', 'R133607', 'R133616', 'R133631', 'R133640', 'R133664',
    'R133733', 'R133748', 'R133757', 'R133789', 'R133849', 'R133879',
    'R133894', 'R133906', 'R133921', 'R133933', 'R133945', 'R133996',
    'R134035', 'R134152', 'R134164', 'R134170', 'R134176', 'R134182',
    'R134188', 'R134197', 'R135929', 'R135944', 'R136284', 'R136296'
]

EAST_REFS = [
    'R133577', 'R133604', 'R133613', 'R133622', 'R133637', 'R133679',
    'R133739', 'R133754', 'R133804', 'R135935', 'R135950'
]

SOUTH_REFS = [
    'R91076', 'R93284', 'R133960', 'R136314', 'R136317', 'R136473',
    'R133562', 'R135965', 'R136323', 'R136476', 'R133592', 'R133595',
    'R133598', 'R93275', 'R136692'
]

print(f"West refs in file: {sum(1 for r in WEST_REFS if f'referent=\"{r}\"' in text)} / {len(WEST_REFS)}")
print(f"East refs in file: {sum(1 for r in EAST_REFS if f'referent=\"{r}\"' in text)} / {len(EAST_REFS)}")
print(f"South refs in file: {sum(1 for r in SOUTH_REFS if f'referent=\"{r}\"' in text)} / {len(SOUTH_REFS)}")

# Print a couple to see their XML
for ref in ['R91073', 'R133577', 'R133562']:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        end = text.find('</Item>', idx)
        print(f"\nSample {ref}:")
        print(text[idx:end+7])
