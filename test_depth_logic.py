import re

# Test snippet
sample_xml = """
<Item class="Model" referent="R1">
	<Properties>
		<string name="Name">Livingroom_31_45_28</string>
	</Properties>
	<Item class="Model" referent="R2">
		<Properties>
			<string name="Name">Piso_0</string>
		</Properties>
		<Item class="Part" referent="R3">
			<Properties>
				<string name="Name">Part1</string>
			</Properties>
		</Item>
		<Item class="Part" referent="R4">
			<Properties>
				<string name="Name">Part2</string>
			</Properties>
		</Item>
	</Item>
</Item>
"""

lines = sample_xml.strip().split("\n")
current_house = None
in_piso_0 = False
piso_0_depth = 0
out = []

for line in lines:
    if current_house is None:
        if '<string name="Name">Livingroom_31_45_28</string>' in line:
            current_house = "Livingroom_31_45_28"
    elif current_house:
        if '<string name="Name">Piso_0</string>' in line:
            in_piso_0 = True
            piso_0_depth = 1

        if in_piso_0:
            if '<Item ' in line:
                piso_0_depth += 1
            elif '</Item>' in line:
                piso_0_depth -= 1
                if piso_0_depth == 0:
                    out.append("<!-- INJECT PISO 0 -->")
                    out.append(line)
                    out.append("<!-- INJECT PISO 1 -->")
                    in_piso_0 = False
                    current_house = None
                    continue
    out.append(line)

print("\n".join(out))
