import re

sample = '''<Vector3 name="size">
\t\t\t\t\t\t\t\t<X>2.91450000</X>
\t\t\t\t\t\t\t\t<Y>0.0599999987</Y>
\t\t\t\t\t\t\t\t<Z>2.92000000</Z>
\t\t\t\t\t\t\t</Vector3>'''

def close_roof_seams(block):
    m = re.search(r'(<Vector3 name="size">\s*<X>)([^<]+)(</X>\s*<Y>[^<]+</Y>\s*<Z>)([^<]+)(</Z>)', block)
    if m:
        sx = float(m.group(2))
        sz = float(m.group(4))
        new_sx = 3.02 if 2.85 < sx < 3.0 else sx
        new_sz = 3.02 if 2.85 < sz < 3.0 else sz
        if new_sx != sx or new_sz != sz:
            new_size_tag = f"{m.group(1)}{new_sx:.4f}{m.group(3)}{new_sz:.4f}{m.group(5)}"
            block = block[:m.start()] + new_size_tag + block[m.start() + len(m.group(0)):]
    return block

print("Original:")
print(sample)
print("\nTransformed:")
print(close_roof_seams(sample))
