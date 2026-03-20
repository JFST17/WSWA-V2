with open("rebuilder.py", "r", encoding="utf-8") as f:
    content = f.read()

content_lines = []
for line in content.split("\n"):
    if line.startswith("import") or line.startswith("from"):
        continue
    content_lines.append(line)

filtered_content = "\n".join(content_lines)

with open(r"modules\statistical_module.py", "a", encoding="utf-8") as f:
    f.write("\n\n" + filtered_content)
