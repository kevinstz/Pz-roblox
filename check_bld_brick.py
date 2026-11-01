import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find parts in Exterior_8080_11648 that are walls
idx = text.find('Exterior_8080_11648')
end_model = text.find('</Item>', idx)
# But wait, Exterior_8080_11648 has children until its matching </Item>
# Let's search all parts in Exterior_8080_11648
m_start = text.find('referent="R133834"') # Let's find model referent for Exterior_8080_11648
print("Exterior_8080_11648 around:", text[idx-50:idx+100])
