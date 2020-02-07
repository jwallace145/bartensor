import json

dirty = json.loads(open('drinks.json').read())

i = 1
clean = []
for dirty_drink in dirty.values():
    if dirty_drink['name'][0].strip() == '':
        continue
    clean_drink = {
        'id': i,
        'names': dirty_drink['name'],
        'ingredients': dirty_drink['ingredients'],
        'method': dirty_drink['method']
    }
    i += 1
    clean.append(clean_drink)

with open('drinks-cleaned.json', 'w') as f:
    f.write(json.dumps(clean, indent=4, ensure_ascii=False))
