df = pd.read_csv('minimalistbaker_ingredient_output_standardized_units_values2.csv')
df.shape

food = df['IFoods'].value_counts() # 5,175
food

df['IFoods'] = df.IFoods.apply(lambda x: str(x).lower().strip())

# Previously, I replaced the phrase ' to ' with '-' for phrases like '2 to 3 bananas'.
# This also wound up with some phrases like 'salt-taste' that should be 'salt to taste.'

tos = ['sweetener-taste', 'water-cover', 'water-cook', 'seasonings-taste', 'water-boil', 'salt-taste', 'ice-chill', 'water-thin', 'more-taste']

def find_tos(food):
    for t in tos:
        if food.find(t) != -1:
            return(food.replace('-', ' to '))
    return food

df['IFoods'] = df.IFoods.apply(lambda x: find_tos(x))

# Create a list of food keys: words that indicate an actual food item without associated descriptions or preparation instructions
# e.g. 'apples' vs. 'sliced apples'ArithmeticError
# Find a list of single-word ingredients by looking for ingredients that don't contain spaces.

test = df.copy()
test['space'] = test.IFoods.apply(lambda x: x.find(' ') != -1)
test = test[(test['space'] == False) & (test['IFoods'] != 'nan')]
# test

# for key, val in test['IFoods'].value_counts().items():
#     print (key, val)

# Manually evaluate list

check = ['orange', 'white', 'plain', 'sauce', 'seasonings', 'dried', 'sucanat', 'cheese']

test['check'] = test.IFoods.apply(lambda x: x in check)
test[test['check'] == False]

food_keys = list(set(list(test[test['check'] == False]['IFoods'])))
food_keys

new_food_keys = []

no_plural = ['asparagus', 'lemongrass', 'hummus', 'molasses', ]
no_singular = ['breadcrumbs', 'bitters', 'greens', 'sprinkles']
fix_plural = {'radishes' : 'radish', 'tomatoes' : 'tomato', 'potatoes' : 'potato', 'peaches' : 'peach', 'blackberries' : 'blackberry', 'raspberries' : 'raspberry', 
              'cherries' : 'cherry', 'strawberries' : 'strawberry', 'berries' : 'berry', 'cranberries' : 'cranberry', 'blueberries' : 'blueberry'}

for f in food_keys:
    if f[-1] == 's':
        if f[:-1] not in food_keys:
            
            if f in fix_plural.keys():
                new_food_keys.append(fix_plural[f])
            elif f not in no_plural:
                new_food_keys.append(f[:-1])

print(len(food_keys))
print(len(new_food_keys))
new_food_keys = new_food_keys + food_keys
print(len(list(set(new_food_keys))))

test = df.copy()
test = test[test['IFoods'] != 'nan']
test['comma'] = test.IFoods.apply(lambda x: x.find(',') != -1)
test['space'] = test.IFoods.apply(lambda x: x.find(' ') != -1)
test['or'] = test.IFoods.apply(lambda x: x.find(' or ') != -1)

test = test[(test['or'] == False) & (test['comma'] == False) & (test['space'] == True)]

test

def find_food_key(phrase):

    phrase = phrase.split(' ')
    output = [f for f in food_keys if f in phrase]

    if len(output) == 0:
        return ('')
    else:
        return(output)
    
def not_food_key(phrase):

    phrase = phrase.split(' ')
    output = [p for p in phrase if p not in food_keys]

    if len(output) == 0:
        return ('')
    else:
        return(output)

test['find_food'] = test.IFoods.apply(lambda x: find_food_key(x))
test[test['find_food'] != ''][['IFoods', 'find_food']]

output = list(test[test['find_food'] != '']['find_food'])
output = [i for sublist in output for i in sublist]
vals = pd.DataFrame(output, columns = ['found'])
for key, val in vals['found'].value_counts().items():
    print(key, val)

test['extra'] = test.IFoods.apply(lambda x: not_food_key(x))
test[test['extra'] != ''][['IFoods', 'find_food', 'extra']]

output = list(test[test['extra'] != '']['extra'])
output = [i for sublist in output for i in sublist]
not_vals = pd.DataFrame(output, columns = ['not_found'])
for key, val in not_vals['not_found'].value_counts().items():
    print(key, val)

test = df.copy()
test['comma'] = test.IFoods.apply(lambda x: x.find(',') != -1)
test = test[(test['comma'] == True) & (test['IFoods'] != 'nan')]

test['a1'] = test.IFoods.apply(lambda x: x.split(',')[0].strip())
test['a2'] = test.IFoods.apply(lambda x: x.split(',')[1:])
test['a2'] = test.a2.apply(lambda x: ', '.join([y.strip() for y in x]))

for key, val in test['a2'].value_counts().items():
    print(key, val)

# test[['a1', 'a2']].value_counts()

# for key, val in test[['a1', 'a2']].value_counts().items():
#     print(key, '\t', val)
prep = ['chopped', 'sliced', 'diced', 'roasted', 'pitted', 'dried', 'refined', 'toasted', 'peeled', 'cubed', 'minced', 'packed', 'ground', 'raw', 'juiced',
        'uncooked']
adv = ['lightly', 'finely', 'loosely', 'tightly', 'finely']
amts = ['cloves', 'clove', 'head', 'handfuls', 'handful', 'bundles', 'bundle', 'cup', 'cups', 'knobs', 'tsp']
desc = ['fresh', 'each', 'unsweetened', 'plain', 'vegan', 'dairy-free', 'short-grain', 'gluten-free', 
        'salted', 'natural', 'low-sodium', 'easy']


# for key, val in test[['a1', 'a2']].value_counts().items():
#     print(key, val)

# for key, val in test['a1'].value_counts().items():
#     if str(key).find(' or ') != -1:
#         print(key, val)

test['a1a'] = test.a1.apply(lambda x: x.split(' or ')[0].split(' '))
test['a2a'] = test.a1.apply(lambda x: x.split(' or ')[1].split(' ') if x.find(' or ') != -1 else '')

test['a1a'] = test.a1a.apply(lambda x: ' '.join([y for y in x if y not in prep and y not in adv and y not in amts and y not in desc]).strip())
test['a2a'] = test.a2a.apply(lambda x: ' '.join([y for y in x if y not in prep and y not in adv and y not in amts and y not in desc]).strip())


test = test[(test['a2a'] != '') & (test['a1a'] != '')]

test['a1b'] = test.apply(lambda row: row['a1a'] + ' ' + row['a2a'].split(' ')[-1] if len(row['a2a'].split(' ')) > 1 else row['a1a'], axis = 1)

test[['a1a', 'a2a', 'a1b']].value_counts()
all_foods = list(df['IFoods'])
all_foods = [f.split(' ') for f in all_foods]
all_foods = [f for food in all_foods for f in food]
all_foods = pd.DataFrame(data = all_foods, columns = ['food'])
all_foods = all_foods['food'].value_counts()

test = df.copy()

test['food'] = test.IFoods.apply(lambda x: x.split(' '))
test['food'] = test.food.apply(lambda x: ' '.join([y for y in x if y not in prep and y not in adv and y not in amts and y not in desc]).strip())
test['food'] = test.food.apply(lambda x: x[:x.find(',')] if x.find(',') != -1 else x)

# for key, val in test['food'].value_counts().items():
#     print(key, val)

val_counts = test['food'].value_counts().items()

foods = [(key, val) for key, val in val_counts if key.find(' or ') == -1 and key[:3] != 'or ']
len(foods)

def find_num(word):
    return any(c.isdigit() for c in word)

weird = [f for f in all_foods.keys() if find_num(f)]

for key, val in list(all_foods.items())[100:]:
    print(key, val)

extra = ['or', 'and', 'each', 'meal', 'nutritional', 'of', '+']
discard = ['nan']
amount = ['cup']
desc = ['fresh', 'vegan', 'ground', 'red', 'chopped', 'black', 'raw', 'unsweetened', 'white', 'gluten-free', 'green', 'dairy-free', 'brown', 'sliced', 
        'dried', 'ripe', 'organic', 'yellow', 'packed', 'melted', 'plain', 'finely', 'rolled', 'diced', 'roasted', 'salted', 'blend', 'light', 'minced', 
        'frozen', 'dark', 'shredded', 'pure', 'paste', 'thinly', 'choice', '']

test = df.copy()
test['or'] = test.IFoods.apply(lambda x: x.find(' or ') != -1)
test = test[test['or'] == True]
test['a1'] = test.IFoods.apply(lambda x: x.split(' or ')[0])
test['a2'] = test.IFoods.apply(lambda x: x.split(' or ')[1])
test

pairs = test[['a1', 'a2']].value_counts()
for key, val in pairs.items():
    print(key, val)

test = df.copy()
test['weird'] = test.IFoods.apply(lambda x: find_num(x))
test[test['weird'] == True]



