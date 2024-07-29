import pandas as pd
import numpy as np
import pumpkinpy as ppy

def find_to_replace(item):
    
    to_replace = ['sweetener-taste', 'water-cover', 'water-cook', 'seasonings-taste', 'water-boil', 'salt-taste', 'ice-chill', 'water-thin', 'more-taste',
                  'need-be']

    for t in to_replace:
        if item.find(t) != -1:
            return(item.replace('-', ' to '))
    
    return(item)

    df['ingredItem'] = df.ingredItem.apply(lambda x: find_to_replace(x))

def basic_std(df):

    df['ingredItem'] = df.ingredItem.apply(lambda x: str(x).lower().strip())

    # Previously, I replaced the phrase ' to ' with '-' for phrases like '2 to 3 bananas'.
    # This also wound up with some phrases like 'salt-taste' that should be 'salt to taste.'

    df['ingredItem'] = df.ingredItem.apply(lambda x: find_to_replace(x))

def find_food_keys(df):
    # Create a list of food keys: words that indicate an actual food item without associated descriptions or preparation instructions
    # e.g. 'apples' vs. 'sliced apples'ArithmeticError
    # Find a list of single-word ingredients by looking for ingredients that don't contain spaces.

    test = df.copy()
    test['space'] = test.ingredItem.apply(lambda x: x.find(' ') != -1)
    test = test[(test['space'] == False) & (test['ingredItem'] != 'nan')]

    # Manually evaluate list

    exclude = ['orange', 'white', 'plain', 'sauce', 'seasonings', 'dried', 'sucanat', 'cheese']

    test['check'] = test.ingredItem.apply(lambda x: x in exclude)

    food_keys = list(set(list(test[test['check'] == False]['ingredItem'])))

    new_food_keys = []

    no_plural = ['asparagus', 'lemongrass', 'hummus', 'molasses', ]
    fix_plural = {'radishes' : 'radish', 'tomatoes' : 'tomato', 'potatoes' : 'potato', 'peaches' : 'peach', 
                  'blackberries' : 'blackberry', 'raspberries' : 'raspberry', 'cherries' : 'cherry', 'strawberries' : 'strawberry', 
                  'berries' : 'berry', 'cranberries' : 'cranberry', 'blueberries' : 'blueberry'}

    for f in food_keys:
        if f[-1] == 's':
            if f[:-1] not in food_keys:
                
                if f in fix_plural.keys():
                    new_food_keys.append(fix_plural[f])
                elif f not in no_plural:
                    new_food_keys.append(f[:-1])

    new_food_keys = new_food_keys + food_keys

    return(new_food_keys)

def find_desc(df):
    test = df.copy()
    test['desc'] = test.ingredItem.apply(lambda x: x.split(', ')[1] if x.find(', ') != -1 else '')
    test['not_desc'] = test.ingredItem.apply(lambda x: x.split(', ')[0] if x.find(', ') != -1 else '')
    # print(test[test['desc'] != ''][['ingredItem', 'desc']])
    # for k, v in test[test['desc'] != '']['desc'].value_counts().items():
        # if k.find('cut ') == -1 and k.find('diced ') == -1 and k.find('finely ') == -1 and k.find('ed') == -1:
        #     print(k, v)
        # if k.find('ed') != -1:
        #     print(k, v)
    test_1 = [k.split(' ') for k, v in test[test['desc'] != '']['desc'].value_counts().items()]
    test_1 = [i for sublist in test_1 for i in sublist]
    eds_1 = [i for i in test_1 if i.find('ed') != -1]
    eds = list(set([(i, eds_1.count(i)) for i in eds_1]))
    eds.sort(key = lambda x: x[1], reverse = True)
    eds = [i for i in eds if i not in ['seed', 'medjool', 'seaweed']]

    ly_1 = [i for i in test_1 if i.find('ly') != -1]
    ly = list(set([(i, ly_1.count(i)) for i in ly_1]))
    ly.sort(key = lambda x: x[1], reverse = True)
    # ly = [i for i in ly if i not in ['seed', 'medjool', 'seaweed']]

    eds = [e[0] for e in eds]
    additional = ['cut', 'more', 'optional', 'cooking', 'whole', 'powder', 'or', 'for', 'torn', 'temperature', 'juices', 'beaten', 'ripe', 'such', 'pulp']
    eds = eds + additional

    new_food_keys = []

    for k, v in test[test['desc'] != '']['desc'].value_counts().items():
        k_sub = k.split(' ')
        truth_vals = any([e in k_sub for e in eds])
        if not truth_vals:
            new_food_keys.append(k)

    # for item, row in test.iterrows():
    #     if row['desc'] in new_food_keys:
    #         print(row['not_desc'], ' | ', row['desc'])

    return eds

def every_two(df):

    # 6,326
    # 2,126

    new_combos = []
    two_vals = []
    test = df.copy()
    test['by2'] = test.ingredItem.apply(lambda x: x.split(' '))
    by2 = list(test['by2'])

    for b in by2:
        i = 0
        while i < len(b) - 1:
            new_combos.append((b[i], b[i+1]))
            i += 1

    new_combos = [(x[0].replace(',', '').replace('(', '').replace(')', '').replace('.', '').replace('\\', ''), 
                   x[1].replace(',', '').replace('(', '').replace(')', '').replace('.', '').replace('\\', '')) for x in new_combos]
    
    new_combos = [(x[0], x[1]) for x in new_combos if x[0] not in off_limits and x[1] not in off_limits]
    
    test = pd.DataFrame(new_combos, columns = ['x1', 'x2'])
    vals = test[['x1', 'x2']].value_counts()
    # print(len(vals))
    for k, v in list(vals.items())[:250]:
        two_vals.append((' '.join(list(k)), v))

    return (two_vals)

def every_three(df):

    # 6,800
    # 986

    new_combos = []
    three_vals = []
    test = df.copy()
    test['by3'] = test.ingredItem.apply(lambda x: x.split(' '))
    by3 = list(test['by3'])

    for b in by3:
        i = 0
        while i < len(b) - 2:
            new_combos.append((b[i], b[i+1], b[i+2]))
            i += 1

    new_combos = [(x[0].replace(',', '').replace('(', '').replace(')', '').replace('.', '').replace('\\', ''), 
                   x[1].replace(',', '').replace('(', '').replace(')', '').replace('.', '').replace('\\', ''),
                   x[2].replace(',', '').replace('(', '').replace(')', '').replace('.', '').replace('\\', '')) for x in new_combos]
    
    new_combos = [(x[0], x[1], x[2]) for x in new_combos 
                  if x[0] not in off_limits and x[1] not in off_limits and x[2] not in off_limits]
    
    test = pd.DataFrame(new_combos, columns = ['x1', 'x2', 'x3'])
    vals = test[['x1', 'x2', 'x3']].value_counts()
    # print(len(vals))
    
    for k, v in list(vals.items())[:100]:
        three_vals.append((' '.join(list(k)), v))

    return (three_vals)

def extract_keys(df, k1, k2, k3):

    df['ingredItem_test'] = df.ingredItem.apply(lambda x: x.replace(',', '').replace('(', '').replace(')', '').replace('.', '').replace('\\', '').replace('  ', ''))
    df['key3'] = df.ingredItem_test.apply(lambda x: [(k[0], k[1], x.find(k[0])) for k in k3])
    df['key3'] = df.key3.apply(lambda x: [(y[0], y[1], y[2]) for y in x if y[2] != -1])
    df['len3'] = df.key3.apply(lambda x: len(x))

    df['key2'] = df.ingredItem.apply(lambda x: [(k[0], k[1], x.find(k[0])) for k in k2])
    df['key2'] = df.key2.apply(lambda x: [(y[0], y[1], y[2]) for y in x if y[2] != -1])
    df['len2'] = df.key2.apply(lambda x: len(x))

    df['key1'] = df.ingredItem.apply(lambda x: [(k, x.find(k)) for k in k1])
    df['key1'] = df.key1.apply(lambda x: [(y[0], y[1]) for y in x if y[1] != -1])
    df['len1'] = df.key1.apply(lambda x: len(x))

    df['misc'] = df.ingredItem.apply(lambda x: [(m, x.find(m)) for m in misc_food_list])
    df['misc'] = df.misc.apply(lambda x: [(y[0], y[1]) for y in x if y[1] != -1])
    df['misc'] = df.misc.apply(lambda x: sorted(x, key = lambda y: len(y[0]), reverse = True) if len(x) > 0 else x)

    df['best'] = df.key3.apply(lambda x: x[0][0] if len(x) != 0 else '')
    df['best'] = df.apply(lambda row: row['key2'][0][0] if len(row['key2']) != 0 and row['best'] == '' else row['best'], axis = 1)
    df['best'] = df.apply(lambda row: row['key1'][0][0] if len(row['key1']) != 0 and row['best'] == '' else row['best'], axis = 1)
    df['best'] = df.apply(lambda row: row['misc'][0][0] if len(row['misc']) != 0 and row['best'] == '' else row['best'], axis = 1)

    df['ingredItem'] = df.apply(lambda row: row['best'] if row['best'] != '' else row['ingredItem'], axis = 1)

    return (df)

def extra_words(df):

    df['ingredItem_test'] = df.apply(lambda row: row['ingredItem_test'].replace(row['best'], ''), axis = 1)
    rm = list(df['ingredItem_test'])
    rm = [x.split(' ') for x in rm]
    rm = [x for sublist in rm for x in sublist]
    rm = [x for x in rm if x != '' and x not in off_limits]
    
    test = pd.DataFrame(rm, columns = ['word'])
    vals = test['word'].value_counts()

    # for k, v in list(vals.items())[:100]:
    #     print(k, v)

def find_units(df):
    test = df.copy()
    unit_keys = list(set(list(df['ingredUnit'])))
    print(unit_keys)
    test['find_units'] = test.ingredItem.apply(lambda x: x.split(' '))
    test['find_units'] = test.find_units.apply(lambda x: ', '.join([y for y in x if y in unit_keys]).strip())
    print(test[test['find_units'] != ''][['ingredItem', 'find_units']])

misc_food_list = ['baking powder', 'curry powder', 'cocoa powder', 'fresh herbs', 'dill', 'rosemary', 'orange', 'matcha',
     'masa harina', 'coffee', 'arrowroot', 'mayo', 'yogurt', 'sage', 'feta', 'mayonnaise', 'yeast', 'cheddar cheese', 'moringa', 'he shou wu', 'cream of tartar',
     'protein powder', 'triple sec', 'white rum', 'probiotic capsules', 'currant', 'club soda', 'tartar sauce', 'italian seasoning', 'chives', 'carob', 'chicken',
     'everything bagel seasoning', 'agar agar', 'teriyaki', 'parmesan', 'lentils', 'chorizo', 'edamame', 'cannellini bean', 'psyllium husk', 'aji amarillo', 
     'hibiscus flowers', 'magic shell', 'habanero pepper', 'turkey', 'ranch', 'grilled cheese', 'simple syrup', 'poblano pepper', 'penne', 'swiss chard',
     'pie crust', 'hot fudge', 'mung beans', 'maple extract', 'cantaloupe', 'champagne', 'linguini', 'fettuccini', 'anise', 'pimento pepper', 'tofu', 'pizza sauce', 
     'steak sauce', 'bamboo shoots', 'figs', 'apricot', 'marjoram', 'zest', 'queso', 'habanero sauce', 'meatballs', 'ricotta', 'coleslaw', 'baked beans', 'cacao', 'rolls',
     'baba ganoush', 'acai', 'mozzarella', 'falafel', 'tzatziki', 'papaya', 'cotija', 'bok choy', 'manchego', 'wonton wrapper', 'sucanat', 'wine', 'dough', 'shells',
     'manchego', 'food coloring', 'beer', 'candy cane', 'heavy cream', 'root beer', 'bleu cheese', 'pancake batter', 'couscous', 'dark rum', 'refried beans', 
     'ramen', 'rooibos', 'delicata', 'fish sauce', 'pancake mix', 'st. germain', 'elderflower liqueur', 'chai', 'kidney', 'cookies', 'pumpkin', 'celeriac',
     'pepperoni', 'fries', 'slaw', 'tomatillos', 'parsnip', 'lasagna', 'shishito', 'dukkah', 'pistachio', 'bechamel', 'bacon', 'beef', 'bison', 'bee pollen',
     'serrano', 'jalapeno', 'spaghetti', 'bolognese', 'aloo sabzi', 'white fish', 'pizza crust', 'bay leaf', 'chiles', 'baobab powder', 'lima beans', 'red beans',
     'romaine', 'radicchio', 'balsamic reduction', 'chiles de arbol', 'gravy', 'pepperoncini', 'cod  fillets', 'english muffin', 'orzo', 'noodle', 'old bay',
     'seaweed snack', 'calabrian pepper', 'hemp heart', 'jerk seasoning', 'aji verde', 'cheese', 'seasoning', 'dal', 'pepper', 'herbs', 'turnip', 'pancake mix', 
     'pancake', 'cake ball', 'food dye', 'cottage cheese']

off_limits = ['', "&amp;", '(divided', '+', '/', '/2 inch', '1-inch', '1/2-inch', '1/4 inch', ':', '\\ribboned\\', 'ribboned', '\\riced\\', 'all-purpose', 
              'and', 'and/or', 'baby-carrot-sized', 'beaten', 'bite-size', 'bite-sized', 'blitzed', 'brewed', 'browned', 'bundle', 'bundles', 
              'by', 'canned', 'chilled', 'choice', 'chopped', 'chopped/cut', 'clove', 'cloves', 'cooked', 'cooking', 'cooled', 'cored', 
              'crumbled', 'crushed', 'cubed', 'cup', 'cups', 'cut', 'dairy-free', 'de-stemmed', 'deseeded', 'desired', 'diced', 'divided', 'drained', 
              'dried', 'each', 'easy', 'extra', 'favorite', 'finely', 'flaky', 'for', 'fresh', 'from', 'frozen', 'gf', 'gluten-free', 'grapeseed', 
              'grated', 'ground', 'halved', 'handful', 'handfuls', 'head', 'hulled', 'if', 'in', 'into', 'juiced', 'juices', 'knobs', 'large', 'light', 
              'lightly', 'like', 'lite', 'loosely', 'low', 'low-fat', 'low-sodium', 'marinated', 'mashed', 'measured', 'medium', 'medjool', 'melted', 
              'mild', 'minced', 'mixed', 'more', 'natural', 'needed', 'non-dairy', 'not', 'of', 'on', 'only', 'optional', 'or', 'organic', 'packed', 
              'patted', 'peeled', 'pickled', 'pieces', 'pitted', 'plain', 'plus', 'powder', 'powdered', 'pressed', 'pulp', 'quartered', 'reduce', 'refined', 
              'removed', 'ribboned', 'riced', 'rinsed', 'ripe', 'roasted', 'salted', 'scrubbed', 'seaweed', 'seed', 'seeded', 'seeds', 'short-grain', 
              'shredded', 'sifted', 'skin', 'sliced', 'smashed', 'smoked', 'soaked', 'sodium', 'softened', 'sorted', 'squeezed', 'stalked', 'such', 'taste', 
              'temperature', 'thawed', 'thinly', 'tightly', 'to', 'toasted', 'torn', 'trimmed', 'tsp', 'unbleached', 'unsalted', 'unsweetened', 'vegan', 
              'washed', 'wedges', 'whisked', 'whole', 'witha', 'zested', '“riced”', 'riced', 'divided', 'with', 'a', 'other', 'quality', 'good', 'diy',
              'shaved', 'skin-on', 'pure', 'steamed', 'slightly', 'tbsp', '/2-inch', 'boneless', 'skinless']

def standardize_items(df):

    ppy.get_val_count(df, 'ingredItem', 'items')

    basic_std(df)
    one_vals = find_food_keys(df)
    two_vals = every_two(df)
    three_vals = every_three(df)
    extract_keys(df, one_vals, two_vals, three_vals)

    df = df[['recipeTitle', 'ingredAmount', 'ingredUnit', 'ingredItem',
       'ingredNotes', 'recipeCalories', 'recipeProtein', 'recipeFat',
       'recipeCarbs', 'recipeTags', 'recipeURL']]

    ppy.get_val_count(df, 'ingredItem', 'food items')
    
    return(df)
