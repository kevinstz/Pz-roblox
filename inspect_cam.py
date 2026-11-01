with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()
idx = text.find("<string name=\"Name\">IsometricCamera</string>")
start = text.rfind("<Item class=\"LocalScript\"", 0, idx)
ps_start = text.find("<ProtectedString", start)
ps_end = text.find("</ProtectedString>", start)
print(text[ps_start:ps_start+1500])
