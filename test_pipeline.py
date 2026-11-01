import re
import time

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("File loaded, size:", len(text))

# Let's count how many:
# 1. Puerta_ parts have CanCollide false
p_matches = list(re.finditer(r'<Item class="Part"[^>]*>.*?</Item>', text[:500000], re.DOTALL))
print("Sample scan done")
