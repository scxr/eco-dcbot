import json
with open("stakeMines.json", "r") as f:
    stakeMines = json.load(f)
amounts = []
for i, v in stakeMines.items():
    print(i, v)
    a = i.split('d')[0]
    mines = a[1:]
    d = i[3:]
    text = f"Mines : {mines}, Diamonds : {d} - Multiplier : {v}"
    amounts.append(text)

with open("out.txt", "w") as f:
    f.write('\n'.join(amounts))