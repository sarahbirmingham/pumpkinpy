# Load libraries
# Uses custom classes from pumpkinpy

import pandas as pd
import numpy as np
import re
import pumpkinpy as ppy
from urllib.request import urlopen

# Iterate through MinimalistBaker recipe index pages and scrape indiviual recipe URLs

def get_recipe_urls(page):

    url = "https://minimalistbaker.com/recipe-index/?fwp_paged=" + str(page)

    page = urlopen(url)
    
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    url_search_key = "href=\"https://minimalistbaker.com/.*/\" tabindex"
    all_urls = re.findall(url_search_key, html)
    all_urls = all_urls[0]
    all_urls = all_urls.split("><")

    new_search_key = "https://minimalistbaker.com/.*/\""
    new_urls = [re.findall(new_search_key, u) for u in all_urls]
    new_urls = [u for u in new_urls if len(u) > 0]

    new_urls = [u[0].replace('\"', '') for u in new_urls]
    new_urls = list(set(new_urls))
    
    return(new_urls)

# Parses ingredient list by separating each unformatted ingredient into amount (1), unit (Tbsp), item (sugar), notes (or sub maple syrup)

def ingredient_parser(ingredient_list):

    new_ingredient_list = []

    for item in ingredient_list:

        # quick clean-up
        item = item.replace('¼', '1/4').replace("⅓", '1/3').replace('½', '1/2').replace('⅔', '2/3').replace('¾', '3/4')
        item = item.replace("\"", '').replace('*', '').replace(' to ', '-').replace('//', '/').replace('((', '(').replace('))', ')')
        

        # # # Find notes first
        # most 'notes' on MinimalistBaker are enclosed within parentheses, making them easy to find
        if item.find('(') != -1:
             notes = item[item.rfind('('):item.rfind(')')+1]
        else:
             notes = ''

        # If notes are found, remove them from remaining ingredient string             
        if notes != '':
             item = item.replace(notes, '')

        notes = notes.replace('(', '').replace(')', '')

        # # # Search for amount
        # The 'amount' is usually a number, eventually followed by letters (e.g. 1 cup, 2 tbsp, 3 whole, 3/4 tsp)
        key = "[^0-9] [a-zA-Z]+ "

        amount = re.sub(key, '', item)

        try:
            if amount[-1] == '/':
                    amount = amount.replace('/', '').strip()
                        
            if amount[-1] == '-':
                    amount = amount.replace('-', '').strip()
        
        except:
            pass

        # Remove letters from amount, keep other quantities (e.g. 1-2, 1/2)
        first_text = re.search("[a-zA-Z]", amount)
    
        try:
            amount = amount[:first_text.start()]

        except:
             amount = amount

        # Remove 'amount' from remaining ingredient string
        item = item.replace(amount, '').strip()

        # # # Find the unit
        # The unit is typically the first word after the amount
        if amount != '':
            unit = item[:item.find(' ')]
        else:
            unit = ''

        # # # Find the item
        # The item is what's left over
        item = item.replace(unit, '').strip()

        new_ingredient_list.append(ppy.Ingredient(item, unit, amount, notes))

    return(new_ingredient_list)

# Accesses each URL and scrapes nutrition info, ingredient list, and tags

def get_recipe_info(url):
    
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # # Title

    # For MinimalistBaker, the title is always included in the URL
    title = url.replace('https://minimalistbaker.com/', '').replace('/', '').replace('-', ' ')
    title = title.title()

    # # Nutrition information

    # Nutrition information is provided and labeled on the MB website
    try:
        nutrition_key = "wprm-nutrition-label-text-nutrition-label.*</span>"
        nutrition_text = re.findall(nutrition_key, html)
        nutrition_text = nutrition_text[0]

        find_labels = ">[A-Z][a-z]* *[A-Za-z]*: <"
        find_values = ">[0-9.]+<"
        labels = re.findall(find_labels, nutrition_text)
        values = re.findall(find_values, nutrition_text)

        labels = [l.replace('>', '').replace(': <', '') for l in labels]
        values = [v.replace('>', '').replace('<', '') for v in values]
        values = [float(v) for v in values]

        nutrition = {}

        for i in range(len(labels)):
            nutrition[labels[i]] = values[i]

        nutrition = ppy.Nutrition(calories = nutrition['Calories'], protein = nutrition['Protein'], fat = nutrition['Fat'], carbs = nutrition['Carbohydrates'])
    
    except:
        nutrition = ppy.Nutrition(calories = 0, protein = 0, fat = 0, carbs = 0)

    # # # Ingredients 
    
    # Ingredients are also labeled
    try:
        ingredient_key = "recipeIngredient\":.*recipeInstructions"
        ingredient_text = re.findall(ingredient_key, html)
        ingredient_text = ingredient_text[0]

        ingredients = ingredient_text[ingredient_text.index("["):ingredient_text.index("]")]

        ingredients = ingredients.replace("\",\"", '~split~')
        ingredients = ingredients.replace("[", '').replace("]", '').replace('\'', '').replace("\"", '').replace('((', '(').replace('))', ')').replace('  ', ' ')
        ingredients = ingredients.split('~split~')

    except:
        ingredients = []

    ingredient_list = ingredient_parser(ingredients)


    # # # Classification

    # Categories are labeled
    try: 
        cat_key = "articleSection.*],\"inLanguage\""
        cat_text = re.findall(cat_key, html)
        cat_text = cat_text[0]

        categories = cat_text[cat_text.find('[')+1:cat_text.find(']')]
        categories = categories.replace("\"", '').replace(",", ", ")

        categories = categories.split(', ')
    
    except:
        categories = []

    title = url.replace('https://minimalistbaker.com/', '').replace('/', '').replace('-', ' ')
    title = title.title()

    recipe = ppy.Recipe(title = title, ingredients = ingredient_list, nutrition = nutrition, tags = categories, url = url)

    return (recipe)

# Formats scraped recipes into a dataframe

def get_recipe_df(recipe_urls):
    
    recipe_data = []
    n_recipes = len(recipe_urls)

    for i in range(n_recipes):
        try:
            r = get_recipe_info(recipe_urls[i])
            ingredient_list = [(' '.join([f.value, f.unit, f.food, f.notes])).strip() for f in r.ingredients]
            recipe_df = pd.DataFrame([r.title, r.nutrition.calories, r.nutrition.protein, r.nutrition.fat, r.nutrition.carbs, ingredient_list, r.tags, r.url]).transpose()
            recipe_df.columns = ['Title', 'Calories', 'Protein', 'Fat', 'Carbs', 'Ingredients', 'Tags', 'URL']
            recipe_data.append(recipe_df)
        except:
            print(recipe_urls[i])
            pass

    all_recipes = pd.concat(recipe_data)
        
    return(all_recipes)

recipes = []

for i in range(1, 100):
    try:
        recipes.append(get_recipe_urls(i))
        # print('Page %d complete' % i)
    except:
        print('No more recipes found.')
        break

recipes = [url for list in recipes for url in list]

print('\n%d recipes found' % len(recipes))

j = 0

for i in range(1, 18):

    print(j, i*100)
    
    recs = recipes[j:i*100]
    df = get_recipe_df(recs)
    df.to_csv('mb_output_test' + str(i) + '.csv', index = False)
    j += 100

df_list = []

for i in range(1, 18):
    
    df = pd.read_csv('mb_output_test' + str(i) + '.csv')
    df_list.append(df)

df = pd.concat(df_list)
    
df = df[(df['Ingredients'] != '[]') & (df['Tags'] != '[]')]

df.to_csv('output_file.csv', index = False)

# Formats scraped recipes into a dataframe

def get_ingredient_df(recipe_urls):
    
    recipe_data = []
    n_recipes = len(recipe_urls)

    for i in range(n_recipes):
        r = get_recipe_info(recipe_urls[i])
        ingredient_values = [f.value for f in r.ingredients]
        ingredient_units  = [f.unit for f in r.ingredients]
        ingredient_foods  = [f.food for f in r.ingredients]
        ingredient_notes  = [f.notes for f in r.ingredients]
        recipe_df = pd.DataFrame([r.title, ingredient_values, ingredient_units, ingredient_foods, ingredient_notes, r.tags, r.url]).transpose()
        recipe_df.columns = ['Title', 'IValues', 'IUnits', 'IFoods', 'INotes', 'Tags', 'URL']
        recipe_df = recipe_df.explode(column = ['IValues', 'IUnits', 'IFoods', 'INotes'])
        recipe_data.append(recipe_df)

    all_recipes = pd.concat(recipe_data)
        
    return(all_recipes)

j = 0

for i in range(1, 18):

    print(j, i*100)
    
    recs = recipes[j:i*100]
    df = get_ingredient_df(recs)
    df.to_csv('mb_ingredient_output_test' + str(i) + '.csv', index = False)
    print(df.shape)
    j += 100

df_list = []

for i in range(1, 18):
    
    df = pd.read_csv('mb_ingredient_output_test' + str(i) + '.csv')
    df_list.append(df)

df = pd.concat(df_list)

df.to_csv('ingredient_output_file.csv', index = False)
