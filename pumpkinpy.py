import pandas as pd
import numpy as np

class Recipe:

    def __init__(self, title, ingredients, nutrition, tags, url):
        self.title = title
        self.ingredients = ingredients
        self.nutrition = nutrition
        self.tags = tags
        self.url = url

class Nutrition:

    def __init__(self, calories, protein, fat, carbs):
        self.calories = calories
        self.protein = protein 
        self.fat = fat
        self.carbs = carbs

class Ingredient:

    def __init__(self, food, unit, value, notes):
        self.food = food
        self.unit = unit
        self.value = value
        self.notes = notes

def get_val_count(df, col_name, col_type):

    vals = df[col_name].value_counts()
    print('Unique %s count: %d' % (col_type, len(vals)))

    return(vals.items())
