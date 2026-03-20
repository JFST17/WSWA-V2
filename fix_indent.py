with open(r'c:\Users\Utilizador\Desktop\GITHub Databases\Protracted Wars\Project-Western-Sahara-War-Archive\modules\statistical_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 'st.plotly_chart(' in line and i > 0 and 'update_layout(title_pad=dict(b=25)' in lines[i-1]:
        indent = len(lines[i-1]) - len(lines[i-1].lstrip())
        line = (' ' * indent) + line.lstrip()
    new_lines.append(line)

with open(r'c:\Users\Utilizador\Desktop\GITHub Databases\Protracted Wars\Project-Western-Sahara-War-Archive\modules\statistical_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
