with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
print('Cursor matches:', re.findall(r'<string name="Name">[^<]*[Cc]ursor[^<]*</string>', text))
print('Camera matches:', re.findall(r'<string name="Name">[^<]*[Cc]amera[^<]*</string>', text))
print('Vehiculos matches:', re.findall(r'<string name="Name">[^<]*[Vv]ehiculo[^<]*</string>', text))
