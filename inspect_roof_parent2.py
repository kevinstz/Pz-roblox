with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

target = '<string name="Name">roofs_30_07_29</string>'
idx = text.find(target)
if idx != -1:
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    # Let's count line indentation of item_start:
    line_start = text.rfind('\n', 0, item_start) + 1
    indent = text[line_start:item_start]
    print(f"Item indentation: {len(indent)} tabs")
    
    # The parent has one less tab
    parent_indent = indent[:-1]
    # search backwards from item_start for \n + parent_indent + '<Item '
    p_pos = text.rfind('\n' + parent_indent + '<Item ', 0, item_start)
    print("Parent item starts at", p_pos)
    # print properties of parent
    p_name_m = text[p_pos:p_pos+1500]
    import re
    m = re.search(r'<string name="Name">([^<]+)</string>', p_name_m)
    print("Parent Name:", m.group(1) if m else "Unknown")
    m_cls = re.search(r'<Item class="([^"]+)"', p_name_m)
    print("Parent Class:", m_cls.group(1) if m_cls else "Unknown")
