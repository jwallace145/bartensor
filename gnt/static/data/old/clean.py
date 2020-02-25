import json

# https://cloud.ibm.com/docs/discovery?topic=discovery-addcontent

# https://cloud.ibm.com/apidocs/discovery/discovery#add-configuration
# https://cloud.ibm.com/apidocs/discovery/discovery#add-a-document

dirty = json.loads(open('drinks.json').read())

i = 1
clean = []
for dirty_drink in dirty:
    clean_drink = {
        'names': dirty_drink['names'],
        'ingredients': dirty_drink['ingredients'],
        'method': dirty_drink['method'],
        'picture': 'images/placeholder.jpg'
    }
    with open('drinks/' + str(i) + '.json', 'w') as f:
        f.write(json.dumps(clean_drink, indent=4))
    clean.append(clean_drink)
    i += 1

with open('drinks-cleaned.json', 'w') as f:
    f.write(json.dumps(clean, indent=4, ensure_ascii=False))
