import pandas as pd
import numpy as np
import pumpkinpy as ppy


def basic_std(df):

    df['ingredAmount'] = df.ingredAmount.apply(lambda x: str(x).replace('~', '').replace('(', ''))

def std_dash_vals(val_col, unit_col, food_col, notes_col):


    if val_col == '1-':
        return(['', '', val_col + ' ' + unit_col + ' ' + food_col, notes_col])
    
    elif val_col[-1] == '-':

        real_val = val_col[val_col.find(' '):].strip()
        real_unit = food_col[:food_col.find(' ')].strip()

        if real_unit in ['wraps', 'pieces', 'bags', 'strips', 'jars']:
            real_unit = real_unit[:-1]
        if real_unit in ['black', 'chicken', 'flat', 'pizza', 'raspberry', 'salmon', 'nan', '(or', 'flour', '/', 'whole']:
            real_unit = ''

        new_val_col = val_col[:val_col.find(' ')].strip()
        new_unit_col = real_unit
        new_food_col = food_col[len(real_unit):]
        new_notes_col = '(' + real_val + unit_col + '), ' + notes_col

        if new_unit_col in ['cod', 'salmon']:
            new_food_col = new_unit_col + ' ' + new_food_col
            new_unit_col = ''
        
        return ([new_val_col, new_unit_col, new_food_col, new_notes_col])
    
    else:

        return([val_col, unit_col, food_col, notes_col])
    
def fix_dash_vals(df):

    df['dash_vals'] = df.apply(lambda row: std_dash_vals(str(row['ingredAmount']), str(row['ingredUnit']), str(row['ingredItem']), str(row['ingredNotes'])), axis = 1)
    df['ingredAmount'] = df.dash_vals.apply(lambda x: x[0])
    df['ingredUnit'] = df.dash_vals.apply(lambda x: x[1])
    df['ingredItem'] = df.dash_vals.apply(lambda x: x[2])
    df['ingredNotes'] = df.dash_vals.apply(lambda x: x[3])
    df.drop(['dash_vals'], axis = 1, inplace = True)

def std_space_vals(val_col, unit_col, food_col, notes_col):

    if val_col.find(' ') != -1 and val_col.find('/') == -1:

        real_val = val_col[val_col.find(' '):].strip()
        real_unit = food_col[:food_col.find(' ')].strip()

        if real_unit in ['cans']:
            real_unit = real_unit[:-1]
        if real_unit in ['each)', 'skin-on', 'whole', 'nan']:
            real_unit = ''

        new_val_col = val_col[:val_col.find(' ')].strip()
        new_unit_col = real_unit
        new_food_col = food_col[len(real_unit):].strip()
        new_notes_col = '(' + real_val + ' ' + unit_col + '), ' + notes_col

        if new_unit_col in ['chicken', 'sugar', 'salmon']:
            new_food_col = new_unit_col + ' ' + new_food_col
            new_unit_col = ''

        if new_unit_col in ['wraps']:
            new_unit_col = new_unit_col[:-1]

        
        return ([new_val_col, new_unit_col, new_food_col, new_notes_col])
    
    else:
        return([val_col, unit_col, food_col, notes_col])

def fix_space_vals(df):


    df['space_vals'] = df.apply(lambda row: std_space_vals(str(row['ingredAmount']), str(row['ingredUnit']), str(row['ingredItem']), str(row['ingredNotes'])), axis = 1)
    df['ingredAmount'] = df.space_vals.apply(lambda x: x[0])
    df['ingredUnit'] = df.space_vals.apply(lambda x: x[1])
    df['ingredItem'] = df.space_vals.apply(lambda x: x[2])
    df['ingredNotes'] = df.space_vals.apply(lambda x: x[3])
    df.drop(['space_vals'], axis = 1, inplace = True)
        
def misc(df):

    df['ingredAmount'] = df.ingredAmount.apply(lambda x: str(x).replace('nan', ''))
    df['ingredAmount'] = df.ingredAmount.apply(lambda x: x.replace(' - ', '-').replace('- ', '-').replace(' -', '-').strip())
    df['ingredAmount'] = df.ingredAmount.apply(lambda x: x.replace('1.2', '12'))  
    df['ingredItem'] = df.apply(lambda row: row['ingredUnit'] + ' ' + row['ingredItem'] 
                                if     row['ingredUnit'] == 'wraps'
                                else   row['ingredItem'],
                                axis = 1)
    df['ingredUnit'] = df.ingredUnit.apply(lambda x: x.replace('nan', '').replace('wraps', ''))
    df['ingredAmount'] = df.ingredAmount.apply(lambda x: x.replace('0.5', '1/2').replace('.5', ' 1/2').replace('&', ''))

def standardize_amounts(df):
    ppy.get_val_count(df, 'ingredAmount', 'amount')
    basic_std(df)
    fix_dash_vals(df)
    misc(df)
    fix_space_vals(df)
    ppy.get_val_count(df, 'ingredAmount', 'amount')

    return(df)
