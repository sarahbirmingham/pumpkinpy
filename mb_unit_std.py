import pandas as pd
import numpy as np
import pumpkinpy as ppy

df = pd.read_csv('output_file.csv')
df.shape

units = df['IUnits'].value_counts() # 248 -> 133 # 208 -> 56
len(units)
for key, val in units.items():
    print(key, val)

df['IUnits'] = df.IUnits.apply(lambda x: str(x).lower())
df['IUnits'] = df.IUnits.apply(lambda x: str(x).replace('~', '').replace(')', '').replace(',', ''))
df['IUnits'] = df.IUnits.apply(lambda x: 'ounce' if x in ['ounces', 'oz', 'oz.', '-oz', '-oz.', '-ounce', 'oz.)'] else x)
df['IUnits'] = df.IUnits.apply(lambda x: 'cup' if x in ['cups', 'cu'] else x)
df['IUnits'] = df.IUnits.apply(lambda x: 'lb' if x in ['lbs', 'lb.', 'pound', 'pounds', 'lbs.'] else x)
df['IUnits'] = df.IUnits.apply(lambda x: '' if x in ['~', 'nan', 'just', 'very', 'homemade', 'generous', 'xl', 'perfectly'] else x)
df['IUnits'] = df.IUnits.apply(lambda x: 'tsp' if x in ['teaspoon', 'tps', 'teaspoons'] else x)
df['IUnits'] = df.IUnits.apply(lambda x: 'tbsp' if x in ['tbsp.', 'Tbs'] else x)
df['IUnits'] = df.IUnits.apply(lambda x: str(x).replace('~', ''))
df['INotes'] = df.INotes.apply(lambda x: str(x).replace('(Yes, Tablespoon)', '').replace('(seriously)', '').replace('(yes Tablespoon)', ''))

df['IUnits'] = df.apply(lambda row: 'pinch' if str(row['IFoods']).find('pinch') != -1 else row['IUnits'], axis = 1)
df['IFoods'] = df.IFoods.apply(lambda x: str(x).replace('pinch', '').strip())

df['IUnits'] = df.apply(lambda row: str(row['IUnits']) + str(row['IFoods']) if len(str(row['IFoods'])) == 1 else row['IUnits'], axis = 1)
df['IFoods'] = df.apply(lambda row: str(row['INotes']) if len(str(row['IFoods'])) == 1 else row['IFoods'], axis = 1)
df['INotes'] = df.apply(lambda row: str(row['IFoods'])[str(row['IFoods']).find('('):str(row['IFoods']).find(')')+1] if str(row['IFoods']).find('(') != -1 else str(row['INotes']), axis = 1)
df['IFoods'] = df.apply(lambda row: str(row['IFoods']).replace(str(row['INotes']), '') if str(row['INotes']) != 'nan' else str(row['IFoods']), axis = 1)

df['IUnits'] = df.apply(lambda row: row['IFoods'][:row['IFoods'].find(' ')].strip() if row['IUnits'] == 'heaping' else row['IUnits'], axis = 1)

plurals = {'cups' : 'cup', 'cloves' : 'clove', 'stalks' : 'stalk', 'slices' : 'slice', 'sprigs' : 'sprig', 
           'batches' : 'batch', 'scoops' : 'scoop', 'ears' : 'ear', 'leaves' : 'leaf', 'pinches' : 'pinch',
           'packets' : 'packet', 'sheets' : 'sheet', 'heads' : 'head', 'squares' : 'square', 'dashes' : 'dash',
           'pieces' : 'piece', 'rounds' : 'round', 'shots' : 'shot', 'cans' : 'can', 'ribs' : 'rib',
           'sticks' : 'stick', 'capsules' : 'capsule', 'bundles' : 'bundle'}

df['IUnits'] = df.IUnits.apply(lambda x: plurals[x] if x in list(plurals.keys()) else x)

desc = ['ripe', 'pitted', 'fresh', 'dried', 'frozen', 'organic', 'homemade', 'sliced']

df['INotes'] = df.apply(lambda row: str(row['IUnits']) + ', ' + str(row['INotes']) if str(row['IUnits']) in desc else str(row['INotes']), axis = 1)
df['INotes'] = df.INotes.apply(lambda x: x.replace(', nan', '').strip())
df['IUnits'] = df.IUnits.apply(lambda x: '' if x in desc else x)

size = ['medium', 'large', 'small', 'medium-large', 'small-medium', 'big', 'medium-sized', 'standard-size', 'mini', 'medium-size', 'burrito-size', 
        'average-size', 'quarter-size']

df['INotes'] = df.apply(lambda row: str(row['IUnits']) + ', ' + str(row['INotes']) if str(row['IUnits']) in size else str(row['INotes']), axis = 1)
df['INotes'] = df.INotes.apply(lambda x: x.replace(', nan', '').strip())
df['IUnits'] = df.IUnits.apply(lambda x: '' if x in size else x)

food = ['chipotle', 'red', 'medjool', 'lemon', 'white', 'corn', 'serrano', 'bay', 'coconut', 'green', 'lemons', 'egg', 'spring', 
        'baby', 'thai', 'probiotic', 'lime', 'tart', 'yellow', 'mint', 'rice', 'ciabatta', 'milk', 'bell', 'grapfruit', 'sugar', 
        'brown', 'brownies', 'basil',  'kumquats', 'candy', 'wonton', 'bosc', 'granny', 'russet', 'button', 'sweet', 'ginger', 
        'vanilla', 'mild', 'black', 'bones', 'boneless', 'makrut', 'kale', 'habanero', 'tea', 'roma', 'jalapeño', 'poblano', 'blood', 
        'pita', 'cherry', 'delicata', 'rooibos', 'cinnamon', 'portobello', 'roasted', 'peeled', 'ice', 'thinly', 'raw', 'jumbo', 'watermelon']

df['IFoods'] = df.apply(lambda row: str(row['IUnits']) + ' ' + str(row['IFoods']) if str(row['IUnits']) in food else str(row['IFoods']), axis = 1)
df['IUnits'] = df.IUnits.apply(lambda x: '' if x in food else x)

steal = ['heaping', 'scant', 'heaped', 'rounded']

df['IUnits'] = df.apply(lambda row: row['IFoods'][:row['IFoods'].find(' ')].strip() if row['IUnits'] in steal else row['IUnits'], axis = 1)

combine1 = ['minute', 'ingredient']

df['IFoods'] = df.apply(lambda row: str(row['IValues']) + str(row['IUnits']) + ' ' + str(row['IFoods']) if str(row['IUnits']) in combine1 else row['IFoods'], axis = 1)
df['IValues'] = df.apply(lambda row: '' if str(row['IUnits']) in combine1 else row['IValues'], axis = 1)
df['IUnits'] = df.apply(lambda row: '' if str(row['IUnits']) in combine1 else row['IUnits'], axis = 1)

combine2 = ['-', 'inch-long']

df['IFoods'] = df.apply(lambda row: (row['IValues'][row['IValues'].find(' '):] + row['IUnits'] + row['IFoods']).strip() if str(row['IUnits']) in combine2 else row['IFoods'], axis = 1)
df['IValues'] = df.apply(lambda row: row['IValues'][:row['IValues'].find(' ')] if str(row['IUnits']) in combine2 else row['IValues'], axis = 1)
df['IUnits'] = df.IUnits.apply(lambda x: '' if str(x) in combine2 else x)

discard = ['just', 'very', 'homemade', 'generous', 'xl', 'whole', 'th', 'quot;honeyquot;', 'more', 'vegan-friendly', 'of', 'cu', 'Tbs']

df['IUnits'] = df.IUnits.apply(lambda x: '' if x in discard else x)
df['IUnits'] = df.IUnits.apply(lambda x: 'cup' if x == 'cupp' else x)

df['IFoods'] = df.apply(lambda row: 'tortillas' if row['IUnits'] == 'tortillas' else row['IFoods'], axis = 1)
df['IUnits'] = df.IUnits.apply(lambda x: '' if x == 'tortillas' else x)

df['IFoods'] = df.apply(lambda row: row['IUnits'] + ' ' + row['IFoods'] if row['IUnits'] == 'salmon' else row['IFoods'], axis = 1)
df['IUnits'] = df.IUnits.apply(lambda x: '' if x == 'salmon' else x)

df['IFoods'] = df.apply(lambda row: row['IUnits'] if row['IUnits'] == 'kumquats,' else row['IFoods'], axis = 1)
df['IUnits'] = df.IUnits.apply(lambda x: '' if x == 'kumquats,' else x)

df['IFoods'] = df.apply(lambda row: row['IUnits'] + ' ' + row['IFoods'] if row['IUnits'] == 'skin-on' else row['IFoods'], axis = 1)
df['IUnits'] = df.IUnits.apply(lambda x: '' if x == 'skin-on' else x)

df['IUnits'] = df.IUnits.apply(lambda x: '' if x == 'vegan' else x.lower())

df.to_csv('output_file.csv', index = False)


