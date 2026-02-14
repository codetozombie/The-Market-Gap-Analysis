import pandas as pd

# Bring the function to properly clean the data

def wrangle(filepath):
  df = pd.read_csv(filepath, sep="\t", low_memory=False)
  
  # Select the snacks 
  snacks = df[df["categories_tags"].str.contains("Snack", case=False, na=False)].copy()
  
  #drop the columns with > 20% missing
  max_drop = int(len(snacks) * 0.20)
  snacks.drop(columns=snacks.columns[snacks.isna().sum() > max_drop], inplace=True)
  
  # drop code, url & time columns
  snacks.drop(columns=[
    "code", "url", "created_t", "created_datetime", "last_modified_t", 
    "last_modified_datetime", "last_modified_by", "last_updated_t", "last_updated_datetime"
], inplace=True)
  
  # drop duplicate country & categorie columns
  snacks.drop(columns=["categories", "categories_tags", "countries", "countries_tags", "main_category", "states", "states_tags"], inplace=True)
  
  # drop the ingredients and serving columns
  snacks.drop(columns=["ingredients_text", "ingredients_tags", "ingredients_analysis_tags", "serving_size", "serving_quantity"], inplace=True)


  # Replace missing product & country names with "Unknown"
  snacks["product_name"]=snacks["product_name"].fillna("Unknown")
  snacks["countries_en"]=snacks["countries_en"].fillna("Unknown")

  # Replace nutriscore_grade's missing vale with unknown
  snacks["nutriscore_grade"]=snacks["nutriscore_grade"].fillna("unknown")

  # replace missing nova_group(food_processed) with the most common value (mode)
  snacks["nova_group"]=snacks["nova_group"].fillna(snacks["nova_group"].mode()[0])

  # reomve rows with energy_kcal_100g > 900  
  snacks = snacks[snacks["energy-kcal_100g"] <= 900]

  # reomve rows with energy_100g > 4000
  snacks = snacks[snacks["energy_100g"] <= 4000]

  # reomve rows with fat_100g > 100
  snacks = snacks[snacks["fat_100g"] <= 100]

  # Saturated Fat must be <= Total Fat
  # This removes rows where the math doesn't add up
  snacks = snacks[snacks["saturated-fat_100g"] <= snacks["fat_100g"]]

  # reomve rows with carbohydrates_100g > 100
  snacks=snacks[snacks["carbohydrates_100g"] <= 100]

  # reomve rows with sugars_100g > 100
  snacks=snacks[snacks["sugars_100g"] <= 100]

  # reomve rows with fiber_100g > 40
  snacks = snacks[snacks["fiber_100g"] <= 40]

  # reomve rows with proteins_100g > 100
  snacks = snacks[snacks["proteins_100g"] <= 100]

  # reomve rows with salt_100g > 100
  snacks= snacks[snacks["salt_100g"] <= 100]

  # reomve rows with fruits-vegetables-nuts-estimate-from-ingredients_100g > 100
  snacks = snacks[snacks["fruits-vegetables-nuts-estimate-from-ingredients_100g"] <= 100]

  # reomve rows with nutrition-score-fr_100g < -15 or > 40
  snacks = snacks[(snacks["nutrition-score-fr_100g"] >= -15) & (snacks["nutrition-score-fr_100g"] <= 40)]
  
  # handle na values for categoies_en for snacks and convert to lowercase
  snacks["categories_en"] = snacks["categories_en"].fillna("").str.lower()
  
  snacks = snacks.reset_index(drop=True)
  
  return snacks


def assign_category(row):
    # 1. Setup search text (Combine Category + Product Name)
    # We handle missing values (NaN) by treating them as empty strings
    cat_text = str(row['categories_en']).lower() if isinstance(row['categories_en'], str) else ""
    name_text = str(row['product_name']).lower() if isinstance(row['product_name'], str) else ""
    
    # normalize hyphens and combine
    t = (cat_text + " " + name_text).replace("-", " ")
    
    
    # LEVEL 1: Non Snack / Liquid / Meals
    # beverages
    if any(x in t for x in ['beverage', 'drink', 'juice', 'soda', 'water', 'tea', 'coffee', 'milk', 'latte']):
        return "Beverages"
    
    # supplements
    if any(x in t for x in ['supplement', 'vitamin', 'protein powder', 'capsule', 'whey']):
        return "Supplements"

    # meals & fresh food (lunch items)
    if any(x in t for x in ['pizza', 'sandwich', 'salad', 'meal', 'quiche', 'burger', 'pasta', 'soup', 'noodle']):
        return "Meals & Sandwiches"
    
    
    # LEVEL 2: High Protein & Fruits
    # Meat & Seafood
    if any(x in t for x in ['jerky', 'meat', 'beef', 'pork', 'chicken', 'fish', 'seafood', 'salami', 'ham', 'sausage', 'tuna']):
        return "Meat & Seafood"

    # Fruit & Veggie Snacks
    if any(x in t for x in ['apple compote', 'applesauce', 'fruit based', 'dried fruit', 'raisin', 'prune', 'apricot', 'vegetable', 'berry', 'seaweed']):
        return "Fruit & Veggie Snacks"

    # Nuts & Seeds
    if any(x in t for x in ['nut', 'seed', 'pistachio', 'almond', 'cashew', 'peanut', 'pecan', 'walnut', 'hazelnut', 'trail mix']):
        return "Nuts & Seeds"
        
    # Dairy & Fridge
    if any(x in t for x in ['dairy', 'yogurt', 'yoghurt', 'cheese', 'pudding', 'cream', 'refrigerated', 'butter']):
        return "Dairy & Fridge"


    # LEVEL 3: Salty
    # Chips & Popcorn
    if any(x in t for x in ['popcorn', 'chip', 'crisp', 'puff', 'fries', 'tortilla', 'corn snack', 'pretzel', 'doritos', 'pringles']):
        return "Chips & Popcorn"


    # LEVEL 4: Sweet
    # Breakfast & Cereal
    if any(x in t for x in ['cereal', 'muesli', 'oatmeal', 'oat', 'flake', 'breakfast', 'granola', 'porridge']):
        return "Breakfast & Cereals"

    # Bars
    if 'bar' in t:
        return "Energy & Cereal Bars"

    # Biscuits & Cakes
    if any(x in t for x in ['biscuit', 'cookie', 'cake', 'wafer', 'pastry', 'pie', 'tart', 'brownie', 'muffin', 'doughnut', 'waffle', 'macaron', 'madeleine', 'croissant']):
        return "Biscuits & Cakes"

    # Chocolates & Candies
    if any(x in t for x in ['chocolate', 'cocoa', 'candy', 'candies', 'gummi', 'gummy', 'marshmallow', 'confection', 'sweet', 'bonbon', 'jelly', 'fudge']):
        return "Chocolates & Candies"


    # LEVEL 5: The Fallbacks
    # Savory/Salty Misc
    if any(x in t for x in ['cracker', 'salty', 'salted', 'appetizer']):
        return "Savory & Salty Misc"

    # Plant-Based Misc
    if 'plant based' in t:
        return "Plant-Based Misc"

    # If it is just "Snacks" or "Other"
    return "Other Snacks"


