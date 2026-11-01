with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
matches = re.findall(r'<string name="Name">([^<]*bank[^<]*)</string>', text, re.IGNORECASE)
print("Bank name matches:", set(matches))
matches2 = re.findall(r'<string name="Name">([^<]*knox[^<]*)</string>', text, re.IGNORECASE)
print("Knox name matches:", set(matches2))
