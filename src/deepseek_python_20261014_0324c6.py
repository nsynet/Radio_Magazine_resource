import re

def md_table_to_mediawiki(text):
    lines = text.strip().splitlines()
    # 提取所有表格行（以 | 开头和结尾）
    table_lines = [line.strip() for line in lines if line.strip().startswith('|') and line.strip().endswith('|')]
    
    if not table_lines:
        return "未找到 Markdown 表格"
    
    # 解析表头
    header_line = table_lines[0]
    headers = [cell.strip() for cell in header_line.strip('|').split('|')]
    # 去掉末尾空列（如果全是空）
    while headers and headers[-1] == '':
        headers.pop()
    col_count = len(headers)
    
    # 解析数据行，跳过第二行（|---| 分隔线）
    data_lines = []
    for line in table_lines[1:]:
        if re.match(r'^\|[\s\-\|:]+\|$', line):  # 分隔线
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        # 只保留前 col_count 列，不足补空
        cells = cells[:col_count] + [''] * (col_count - len(cells))
        data_lines.append(cells)
    
    # 生成 MediaWiki
    wiki = ['{| class="wikitable"']
    # 表头
    wiki.append('! ' + ' !! '.join(headers))
    for row in data_lines:
        wiki.append('|-')
        # 每个单元格一行，便于阅读；也可合并为一行
        for cell in row:
            wiki.append(f'| {cell}')
    wiki.append('|}')
    return '\n'.join(wiki)

# 读取文件
with open('input.txt', 'r', encoding='utf-8') as f:
    content = f.read()

result = md_table_to_mediawiki(content)

with open('output.mediawiki', 'w', encoding='utf-8') as f:
    f.write(result)

print("转换完成，已保存到 output.mediawiki")