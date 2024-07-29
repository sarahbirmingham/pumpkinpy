import pandas as pd
import numpy as np
import re
import pumpkinpy as ppy

def basic_std(df):

    df['ingredUnit'] = df.ingredUnit.apply(lambda x: str(x).lower().strip())
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: re.sub("[~),]", '', x))
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' if x in ['~', 'nan', 'just', 'very', 'homemade', 'generous', 'xl', 'perfectly'] else x)

def common_unit_std(df):

    common_unit_dict = {'ounce' : ['ounces', 'oz', 'oz.', '-oz', '-oz.', '-ounce', 'oz.)'],
                        'cup'   : ['cups', 'cu'],
                        'lb'    : ['lbs', 'lb.', 'pound', 'pounds', 'lbs.'],
                        'tsp'   : ['teaspoon', 'tps', 'teaspoons'],
                        'tbsp'  : ['tbsp.', 'Tbs']}
    
    common_unit_dict = [[(v, i) for i in common_unit_dict[v]] for v, k in common_unit_dict.items()]
    common_unit_dict = [i for sublist in common_unit_dict for i in sublist]
    common_unit_dict = {i[1] : i[0] for i in common_unit_dict}    

    df['ingredUnit'] = df.ingredUnit.apply(lambda x: common_unit_dict[x] if x in common_unit_dict.keys() else x)

def plurals(df):
    
    plurals = {'cups' : 'cup', 'cloves' : 'clove', 'stalks' : 'stalk', 'slices' : 'slice', 'sprigs' : 'sprig', 
                'batches' : 'batch', 'scoops' : 'scoop', 'ears' : 'ear', 'leaves' : 'leaf', 'pinches' : 'pinch',
                'packets' : 'packet', 'sheets' : 'sheet', 'heads' : 'head', 'squares' : 'square', 'dashes' : 'dash',
                'pieces' : 'piece', 'rounds' : 'round', 'shots' : 'shot', 'cans' : 'can', 'ribs' : 'rib',
                'sticks' : 'stick', 'capsules' : 'capsule', 'bundles' : 'bundle', 'jars' : 'jar'}
    
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: plurals[x] if x in list(plurals.keys()) else x)

def misc(df):

    df['ingredUnit'] = df.apply(lambda row: 'pinch' 
                                if     str(row['ingredItem']).find('pinch') != -1 
                                else   row['ingredUnit'], 
                                axis = 1)
    
    df['ingredItem'] = df.ingredItem.apply(lambda x: str(x).replace('pinch', '').strip())

    df['ingredItem'] = df.apply(lambda row: str(row['ingredUnit']) + str(row['ingredItem']) 
                                if     len(str(row['ingredItem'])) == 1 
                                else   row['ingredItem'], 
                                axis = 1)
    
    df['ingredUnit'] = df.apply(lambda row: row['ingredItem'][:row['ingredItem'].find(' ')].strip() 
                                if     row['ingredUnit'] == 'heaping' 
                                else   row['ingredUnit'], 
                                axis = 1)

    desc = ['ripe', 'pitted', 'fresh', 'dried', 'frozen', 'organic', 'homemade', 'sliced']

    df['ingredNotes'] = df.apply(lambda row: str(row['ingredUnit']) + ', ' + str(row['ingredNotes']) 
                                if      str(row['ingredUnit']) in desc 
                                else    str(row['ingredNotes']), 
                                axis = 1)
    df['ingredNotes'] = df.ingredNotes.apply(lambda x: x.replace(', nan', '').strip())
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' 
                                           if     x in desc 
                                           else   x)

    size = ['medium', 'large', 'small', 'medium-large', 'small-medium', 'big', 'medium-sized', 'standard-size', 'mini', 'medium-size', 'burrito-size', 
            'average-size', 'quarter-size']


    df['ingredNotes'] = df.apply(lambda row: str(row['ingredUnit']) + ', ' + str(row['ingredNotes']) 
                                 if     str(row['ingredUnit']) in size 
                                 else   str(row['ingredNotes']), 
                                 axis = 1)
    
    df['ingredNotes'] = df.ingredNotes.apply(lambda x: x.replace(', nan', '').strip())
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' 
                                           if     x in size 
                                           else   x)

    food = ['chipotle', 'red', 'medjool', 'lemon', 'white', 'corn', 'serrano', 'bay', 'coconut', 'green', 'lemons', 'egg', 'spring', 
            'baby', 'thai', 'probiotic', 'lime', 'tart', 'yellow', 'mint', 'rice', 'ciabatta', 'milk', 'bell', 'grapfruit', 'sugar', 
            'brown', 'brownies', 'basil',  'kumquats', 'candy', 'wonton', 'bosc', 'granny', 'russet', 'button', 'sweet', 'ginger', 
            'vanilla', 'mild', 'black', 'bones', 'boneless', 'makrut', 'kale', 'habanero', 'tea', 'roma', 'jalapeño', 'poblano', 'blood', 
            'pita', 'cherry', 'delicata', 'rooibos', 'cinnamon', 'portobello', 'roasted', 'peeled', 'ice', 'thinly', 'raw', 'jumbo', 'watermelon']

    df['ingredItem'] = df.apply(lambda row: str(row['ingredUnit']) + ' ' + str(row['ingredItem']) 
                                if     str(row['ingredUnit']) in food 
                                else   str(row['ingredItem']), 
                                axis = 1)
    
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' 
                                           if     x in food 
                                           else   x)

    steal = ['heaping', 'scant', 'heaped', 'rounded']

    df['ingredUnit'] = df.apply(lambda row: row['ingredItem'][:row['ingredItem'].find(' ')].strip() 
                                if     row['ingredUnit'] in steal 
                                else   row['ingredUnit'],
                                axis = 1)

    combine1 = ['minute', 'ingredient']

    df['ingredItem'] = df.apply(lambda row: str(row['ingredAmount']) + str(row['ingredUnit']) + ' ' + str(row['ingredItem']) 
                                if     str(row['ingredUnit']) in combine1 
                                else   row['ingredItem'], 
                                axis = 1)
    df['ingredAmount'] = df.apply(lambda row: '' 
                                  if     str(row['ingredUnit']) in combine1 
                                  else row['ingredAmount'], 
                                  axis = 1)
    df['ingredUnit'] = df.apply(lambda row: '' 
                                if     str(row['ingredUnit']) in combine1 
                                else row['ingredUnit'], 
                                axis = 1)

    combine2 = ['-', 'inch-long']

    df['ingredItem'] = df.apply(lambda row: (row['ingredAmount'][row['ingredAmount'].find(' '):] + row['ingredUnit'] + row['ingredItem']).strip() 
                                if     str(row['ingredUnit']) in combine2 
                                else   row['ingredItem'], 
                                axis = 1)

    df['ingredAmount'] = df.apply(lambda row: row['ingredAmount'][:row['ingredAmount'].find(' ')] 
                                  if     str(row['ingredUnit']) in combine2 
                                  else   row['ingredAmount'], 
                                  axis = 1)
    
    discard = ['just', 'very', 'homemade', 'generous', 'xl', 'whole', 'th', 'quot;honeyquot;', 
               'more', 'vegan-friendly', 'of', 'cu', 'Tbs', 'jalapeñ', 'brownie', 
               'ripe', 'eg', '-', 'inch-long', 'vegan', '(seriously)', '(packed)']

    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' if x in discard else x)

    df['ingredItem'] = df.apply(lambda row: 'tortillas' if row['ingredUnit'] == 'tortillas' else row['ingredItem'], axis = 1)
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' if x == 'tortillas' else x)

    df['ingredItem'] = df.apply(lambda row: row['ingredUnit'] + ' ' + row['ingredItem'] if row['ingredUnit'] == 'salmon' else row['ingredItem'], axis = 1)
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' if x == 'salmon' else x)

    df['ingredItem'] = df.apply(lambda row: row['ingredUnit'] if row['ingredUnit'] == 'kumquats,' else row['ingredItem'], axis = 1)
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' if x == 'kumquats' else x)

    df['ingredItem'] = df.apply(lambda row: row['ingredUnit'] + ' ' + row['ingredItem'] if row['ingredUnit'] == 'skin-on' else row['ingredItem'], axis = 1)
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: '' if x == 'skin-on' else x)

    df['ingredUnit'] = df.ingredUnit.apply(lambda x: x.lower())

def standardize_units(df):

    ppy.get_val_count(df, 'ingredUnit', 'unit')
    basic_std(df)
    common_unit_std(df)
    plurals(df)
    misc(df)
    ppy.get_val_count(df, 'ingredUnit', 'unit')

    return(df)
