import pandas as pd
import pumpkinpy as ppy
import mb_recipe_scraper as mb
import mb_unit_std as mb_unit
import mb_amt_std as mb_amt
import mb_item_std as mb_item

recipe_df = mb.scrape_mb_recipes(max_pages = 100, 
                                 print_page_interval = 10,
                                 print_recipe_interval = 100)

recipe_df = mb_unit.standardize_units(recipe_df)

recipe_df = mb_amt.standardize_amounts(recipe_df)

recipe_df = mb_item.standardize_items(recipe_df)

print(recipe_df.shape)



