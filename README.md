# PumpkinPy
*A recipe web scraper/parser and meal planner designed to optimize nutrition, minimize food waste, and maximize flavor.*

**Author**: Sarah Birmingham

This project was inspired by trying to plan Thanksgiving dinner, 
and more specifically inspired by the single three-year old container of French's fried onions
that I can't seem to use up. When finished, pumpkinpy will be able to amass thousands of recipes
from different sources, parse them into usable data, and create potential menus that feature cohesive 
and complimentary flavors by optimizing the number of ingredients shared between recipes. On a larger 
scale, pumpkinpy will also create customized meal plans tailored to the user's dietary needs, 
nutritional requirements, and tastes. As food costs rise nationwide, shared-ingredient-optimization
will also help keep grocery bills low and reduce the food waste that inevitably follows inefficient 
meal planning. Importantly, users will be able to elect to use either a range or a minimum for their nutritional 
preferences and opt to hide nutritional info in the final output.

The first use case extracts recipes from [MinimalistBaker](https://minimalistbaker.com/).

## To-do list:
**Web Scraping**

`X` Extracts all recipes from one website

` ` Extracts recipes from multiple websites

` ` Extracts recipes from any given website

**Recipe Parsing**

`X` Reliably parses recipe title and URL where available

`X` Reliably parses ingredient list into amount/unit/item/notes, where available

`X` Reliably parses recipe tags/keywords/categories where available

`X` Reliably parses nutrition info into calories/protein/carbs/fat, where available

**Nutrition Inferral**

` ` Converts ingredient units into a common factor

` ` Uses systems of equations to determine nutrition content of individual ingredients

` ` Uses open FDA data to determine/confirm nutrition content of individual ingredients

` ` Calculates recipe nutrition info where it's missing

**Recipe Tagging**

` ` Uses supervised learning techniques to tag untagged recipes based on shared ingredients with 
tagged recipes into categories like 'breakfast', 'lunch', 'snack'

` ` Tags untagged recipes as vegetarian, vegan, dairy-free, etc.

**Meal Prep Planning**

` ` Accepts specified number of meal options as a parameter for a given period 
(2 breakfast options, 3 lunch options, 5 days)

` ` Accepts target calories and macronutrients per day as a parameter

` ` Accepts an ED-friendly *minimum* nutrition requirement as the only parameter

` ` Accepts desired cuisines or ingredients as a parameter 

` ` Accepts dietary requirements as a parameter

` ` Creates groups of different recipes that satisfy the above parameters

` ` Rank meal plans by how closely they match input parameters

` ` Rank meal plans by number of unique ingredients (food waste/cost reduction)

` ` Option to hide nutrition info in final output

**Menu Planning**

` ` Accepts number of dishes as a parameter for a single meal (3 entrees, 6 sides, 2 drinks)

` ` Accepts desired cuisines or ingredients as a parameter 

` ` Accepts dietary requirements as a parameter 

` ` Creates sample menus that satisfy the above parameters

` ` Rank menus by how closely they match input parameters

` ` Rank menus by number of unique ingredients (food waste/cost reduction, as well as meal cohesion!)

**Bonus**

 ` ` Identify when a recipe can be modified to fit certain dietary requirements

 ` ` Retain info on previously-used recipes to ensure variety

 ` ` Re-do regex-heavy ingredient parsing in favor of NLP techniques 
 like the [New York Times](https://archive.nytimes.com/open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/)
