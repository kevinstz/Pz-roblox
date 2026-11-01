import time
import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

t0 = time.time()
lines_count = 0
items_count = 0

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        lines_count += 1
        if '<Item ' in line:
            items_count += 1

t1 = time.time()
print(f"Read {lines_count} lines, found {items_count} items in {t1 - t0:.2f} seconds!")
