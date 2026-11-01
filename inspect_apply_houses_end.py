with open('apply_house_upgrades.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print('\n'.join(lines[350:]))
