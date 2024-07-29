import pandas as pd
import numpy as np
import pumpkinpy as ppy

df = pd.read_csv('output_file.csv')
vals = df['IValues'].value_counts() # 284 -> 137
vals

for key, val in vals.items():
    print(key, val)

df[df['IValues'] == '12.3']
df['IValues'] = df.IValues.apply(lambda x: str(x).replace('~', ''))

def fmt_dash_vals(val_col, unit_col, food_col):

    if val_col == '1-':
        return(['', '', val_col + ' ' + unit_col + ' ' + food_col])
    
    elif val_col[-1] == '-':

        real_val = val_col[val_col.find(' '):].strip()
        real_unit = food_col[:food_col.find(' ')].strip()

        if real_unit in ['black', 'chicken', 'flat', 'pizza', 'raspberry', 'salmon']:
            real_unit = ''

        new_val_col = val_col[:val_col.find(' ')].strip()
        new_unit_col = (real_val + unit_col + ' ' + real_unit).strip()
        new_food_col = food_col[len(real_unit):]
        
        return ([new_val_col, new_unit_col, new_food_col])
    
    else:

        return([val_col, unit_col, food_col])

df['dash_vals'] = df.apply(lambda row: fmt_dash_vals(str(row['IValues']), str(row['IUnits']), str(row['IFoods'])), axis = 1)
df['IValues'] = df.dash_vals.apply(lambda x: x[0])
df['IUnits'] = df.dash_vals.apply(lambda x: x[1])
df['IFoods'] = df.dash_vals.apply(lambda x: x[2])
df = df[['Title', 'IValues', 'IUnits', 'IFoods', 'INotes', 'Tags', 'URL']]

df['IValues'] = df.IValues.apply(lambda x: str(x).replace('nan', ''))
df['IValues'] = df.IValues.apply(lambda x: x.replace(' - ', '-').replace('- ', '-').replace(' -', '-').strip())
df['IValues'] = df.IValues.apply(lambda x: x.replace('1.2', '12'))

df['IUnits'] = df.apply(lambda row: row['IValues'][row['IValues'].find(' '):] + ' ' + row['IUnits'] if row['IValues'].find(' ') != -1 and row['IValues'].find('/') == -1 else row['IUnits'], axis = 1)
df['IValues'] = df.apply(lambda row: row['IValues'][:row['IValues'].find(' ')].strip() if row['IValues'].find(' ') != -1 and row['IValues'].find('/') == -1 else row['IValues'], axis = 1)

df.to_csv('output_file.csv', index = False)
