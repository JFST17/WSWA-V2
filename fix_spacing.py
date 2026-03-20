import re
with open(r'c:\Users\Utilizador\Desktop\GITHub Databases\Protracted Wars\Project-Western-Sahara-War-Archive\modules\statistical_module.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_text = re.sub(r'^(\s*)st\.plotly_chart\((fig[A-Za-z0-9_]*)\s*,', lambda m: f'{m.group(1)}{m.group(2)}.update_layout(title_pad=dict(b=25), margin=dict(t=75))\n{m.group(1)}st.plotly_chart({m.group(2)},', text, flags=re.MULTILINE)

with open(r'c:\Users\Utilizador\Desktop\GITHub Databases\Protracted Wars\Project-Western-Sahara-War-Archive\modules\statistical_module.py', 'w', encoding='utf-8') as f:
    f.write(new_text)
