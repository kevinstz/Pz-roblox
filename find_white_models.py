import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    current_model = ""
    for line in fin:
        if '<Item class="Model"' in line:
            m = re.search(r'referent="([^"]+)"', line)
            # read next lines to get model name
            pass
        if '<string name="Name">' in line:
            name = re.search(r'<string name="Name">([^<]+)</string>', line).group(1)
            if 'Exterior_' in name or 'Bar_' in name:
                current_model = name
        if '684037041b29ec20554a.png' in line:
            print(f"Found 684037041b29ec20554a.png in model: {current_model}")
