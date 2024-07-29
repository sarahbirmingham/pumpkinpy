# Load libraries
# Uses custom classes from pumpkinpy

import pandas as pd
import numpy as np
import re
import time
import pumpkinpy as ppy
from urllib.request import urlopen

# Iterate through MinimalistBaker recipe index pages and scrape indiviual recipe URLs

def pass_time(start):

    end = time.time()
    elapsed = (end - start)
    minutes = int(np.floor(elapsed/60))
    seconds = int(elapsed % 60)

    print('\nTime elapsed: %d minutes and %d seconds' % (minutes, seconds))

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

def get_ingredient_notes(ingredient_string):

    # Notes are almost always included in parentheses at the end of a string
    p1 = ingredient_string.rfind('(')
    p2 = ingredient_string.rfind(')')
     
    # Separate out text contained in parentheses and remove any found notes from remaining ingredient string
    if p1 != -1:
        notes = ingredient_string[p1:p2+1]
        ingredient_string = ingredient_string.replace(notes, '').strip()
        notes = re.sub('[()]', '', notes)
        notes = notes.strip()
    else:
        notes = ''

    return ((ingredient_string, notes))

def get_ingredient_amount(ingredient_string):

    # # # Search for amount

    # If we just extract all numbers, the following case becomes an issue:
        # 4 salmon fillets, 4 oz each -> 44

    # If we just extract numbers before the first space, the following case becomes an issue:
        # 1 1/2 cups of flour -> 1

    # So the 'amount' is usually a number, eventually followed by letters (e.g. 1 cup, 2 tbsp, 3 whole, 3/4 tsp)
        # 4 salmon fillets, 4 oz each -> 4 salmon
        # 1 1/2 cups of flour         -> 1 1/2 cups
    

    amt_key = "[^0-9] [a-zA-Z]+ "

    amt = re.sub(amt_key, '', ingredient_string)
    amt = re.sub("/$|-$", '', amt)

    first_text = re.search("[a-zA-Z]", amt)
    
    try:
        amt = amt[:first_text.start()].strip()

    except:
        amt = amt.strip()

    # Remove 'amount' from remaining ingredient string
    ingredient_string = ingredient_string.replace(amt, '').strip()

    return((ingredient_string, amt))

def get_ingredient_unit(ingredient_string, amt):
     
     # If we find a non-empty amount, the unit is typically the proceeding word

     if amt == '':
          return ((ingredient_string, amt, ''))
     
     unit = ingredient_string[:ingredient_string.find(' ')].strip()
     item = ingredient_string.replace(unit, '').strip()

     return(item, amt, unit)

def ingredient_parser(ingredient_text):
     
     # Parses ingredient list by separating each unformatted ingredient into amount (1), unit (Tbsp), item (sugar), notes (or sub maple syrup)
     
    new_ingredient_list = []

    for ingredient_string in ingredient_text:

        # Quick clean-up
        ingredient_string = ingredient_string.replace('¼', '1/4').replace("⅓", '1/3').replace('½', '1/2').replace('⅔', '2/3').replace('¾', '3/4')
        ingredient_string = ingredient_string.replace("\"", '').replace('*', '').replace(' to ', '-').replace('//', '/').replace('((', '(').replace('))', ')')   
        
        (ingredient_string, notes) = get_ingredient_notes(ingredient_string)
        (ingredient_string, amount) = get_ingredient_amount(ingredient_string)
        (item, amount, unit) = get_ingredient_unit(ingredient_string, amount)

        new_ingredient_list.append(ppy.Ingredient(item, unit, amount, notes))
        
    return (new_ingredient_list)

def get_recipe_nutrition_info(text):

    try:
        nutrition_key = "wprm-nutrition-label-text-nutrition-label.*</span>"
        nutrition_content = re.findall(nutrition_key, text)
        nutrition_content = nutrition_content[0]

        find_labels = ">[A-Z][a-z]* *[A-Za-z]*: <"
        find_values = ">[0-9.]+<"
        labels = re.findall(find_labels, nutrition_content)
        values = re.findall(find_values, nutrition_content)

        labels = [l.replace('>', '').replace(': <', '') for l in labels]
        values = [v.replace('>', '').replace('<', '') for v in values]
        values = [float(v) for v in values]

        nutrition_info = {}

        for i in range(len(labels)):
            nutrition_info[labels[i]] = values[i]

        nutrition = ppy.Nutrition(calories = nutrition_info['Calories'], 
                                  protein = nutrition_info['Protein'], 
                                  fat = nutrition_info['Fat'], 
                                  carbs = nutrition_info['Carbohydrates'])
    
    except:
        nutrition = ppy.Nutrition(calories = 0, protein = 0, fat = 0, carbs = 0)

    return (nutrition)

def get_recipe_ingredients(text):
    
    # Ingredients are also labeled

    try:
        ingredient_key = "recipeIngredient\":.*recipeInstructions"
        ingredient_text = re.findall(ingredient_key, text)
        ingredient_text = ingredient_text[0]

        ingredients = ingredient_text[ingredient_text.index("["):ingredient_text.index("]")]

        ingredients = ingredients.replace("\",\"", '~split~')
        ingredients = ingredients.replace("[", '').replace("]", '').replace('\'', '').replace("\"", '').replace('((', '(').replace('))', ')').replace('  ', ' ')
        ingredients = ingredients.split('~split~')

    except:
        ingredients = []

    ingredient_list = ingredient_parser(ingredients)

    return (ingredient_list)

def get_recipe_tags(text):

    try: 
        tag_key = "articleSection.*],\"inLanguage\""
        tag_text = re.findall(tag_key, text)
        tag_text = tag_text[0]

        recipe_tags = tag_text[tag_text.find('[')+1:tag_text.find(']')]
        recipe_tags = recipe_tags.replace("\"", '').replace(",", ", ")

        recipe_tags = recipe_tags.split(', ')
    
    except:
        recipe_tags = []

    return (recipe_tags)

def get_recipe_info(url):

    # Accesses each URL and scrapes nutrition info, ingredient list, and tags
    
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # For MinimalistBaker, the recipe title is always included in the URL
    title = url.replace('https://minimalistbaker.com/', '').replace('/', '').replace('-', ' ')
    title = title.title()

    ingredient_list = get_recipe_ingredients(html)
    nutrition_info = get_recipe_nutrition_info(html)
    recipe_tags = get_recipe_tags(html)

    recipe = ppy.Recipe(title = title, ingredients = ingredient_list, nutrition = nutrition_info, tags = recipe_tags, url = url)

    return (recipe)

def get_ingredient_df(recipe_urls, print_recipe_interval):
    
    recipe_data = []
    n_recipes = len(recipe_urls)

    for i in range(n_recipes):

        r = get_recipe_info(recipe_urls[i])

        ingredient_amts = [f.value for f in r.ingredients]
        ingredient_units  = [f.unit for f in r.ingredients]
        ingredient_items  = [f.food for f in r.ingredients]
        ingredient_notes  = [f.notes for f in r.ingredients]

        recipe_df = pd.DataFrame([r.title, 
                                  ingredient_amts, ingredient_units, ingredient_items, ingredient_notes,
                                  r.nutrition.calories, r.nutrition.protein, r.nutrition.fat, r.nutrition.carbs,
                                  r.tags, 
                                  r.url]).transpose()
        
        recipe_df.columns = ['recipeTitle', 
                             'ingredAmount', 'ingredUnit', 'ingredItem', 'ingredNotes', 
                             'recipeCalories', 'recipeProtein', 'recipeFat', 'recipeCarbs', 
                             'recipeTags', 
                             'recipeURL']
        
        recipe_df = recipe_df.explode(column = ['ingredAmount', 'ingredUnit', 'ingredItem', 'ingredNotes'])

        recipe_data.append(recipe_df)

        if print_recipe_interval != 0 and i % print_recipe_interval == 0:
            print('Recipes scanned so far: %d' % i)

    all_recipes = pd.concat(recipe_data)

    return(all_recipes)

def scrape_mb_recipes(max_pages, print_page_interval, print_recipe_interval):

    start = time.time()

    recipe_urls = []

    for i in range(1, max_pages):
        try:
            recipe_urls.append(get_recipe_urls(i))

            if print_page_interval != 0 and i % print_page_interval == 0:
                print('Page %d complete' % i)

        except:
            print('No more recipes found.')
            print('Total pages: %d' % (i - 1))
            break

    recipe_urls = [url for list in recipe_urls for url in list]
    n_recipes = len(recipe_urls)

    print('\n%d potential recipes URLs found\n' % n_recipes)

    final_df = get_ingredient_df(recipe_urls, print_recipe_interval)

    rejected_recipes = set(list(final_df[final_df['ingredItem'].isna()].copy()['recipeURL']))
    
    final_df = final_df[final_df['ingredItem'].notna()]
    accepted_recipes = len(set(list(final_df['recipeURL'])))

    print('\nTotal accepted recipes: %d' % accepted_recipes)
    print('Total rejected recipes: %d' % len(rejected_recipes))
    print('\nThe following recipe URLs did not contain a recipe: ')

    for r in rejected_recipes:
        print(r)

    pass_time(start)

    final_df = final_df[(final_df['Ingredients'] != '[]') &
                        (final_df['Tags'] != '[]')]

    return(final_df)
