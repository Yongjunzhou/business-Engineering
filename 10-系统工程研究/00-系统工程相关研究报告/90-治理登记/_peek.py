import io
p = r"08-报告用途登记.md"
t = io.open(p, encoding="utf-8").read()
print(t[:2500])
