import streamlit as st
import plotly.express as px
import pandas as pd
# from helpers import assign_category, wrangle


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




# 1. SETUP & DATA LOAD
st.set_page_config(page_title="Nutrient Matrix", layout="wide")

# Assume 'df' is loaded or load it here
df = wrangle("dataset_vs.csv")

# Apply your classifier function
df['high_level_category'] = df.apply(assign_category, axis=1)

# 2. DASHBOARD HEADER
st.title("🍎 The Nutrient Matrix Dashboard")
st.markdown("Identify product clusters and spot the **'High Protein, Low Sugar'** opportunity gap.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
selected_cats = st.sidebar.multiselect(
    "Select Categories:",
    options=df['high_level_category'].unique(),
    default=df['high_level_category'].unique() # Select all by default
)

# Filter Data based on selection
filtered_df = df[df['high_level_category'].isin(selected_cats)]

# --- INTERACTIVE PLOT (Plotly) ---
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.scatter(
        filtered_df,
        x="sugars_100g",
        y="proteins_100g",
        color="high_level_category",
        hover_name="product_name", 
        # FIX: Removed 'brands' because it is missing from your CSV
        hover_data=["sugars_100g", "proteins_100g"],
        title="Sugar vs. Protein Content",
        template="plotly_white",
        height=600,
        opacity=0.7
    )

    # Add Quadrant Lines (The "Golden Cross")
    fig.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Low Sugar (<5g)")
    fig.add_hline(y=15, line_dash="dash", line_color="green", annotation_text="High Protein (>15g)")

    st.plotly_chart(fig, use_container_width=True)

# --- METRICS SECTION (Right Column) ---
# --- METRICS SECTION (Right Column) ---
with col2:
    st.subheader("📊 Key Insights")
    
    # 1. Define the "Opportunity Zone"
    opportunity_df = filtered_df[
        (filtered_df['sugars_100g'] < 5) & 
        (filtered_df['proteins_100g'] > 15)
    ].copy() # Use .copy() to avoid SettingWithCopy warnings
    
    # Calculate Ratio for the metrics (Safe division)
    opportunity_df['safe_sugar'] = opportunity_df['sugars_100g'].replace(0, 0.1)
    opportunity_df['ratio'] = opportunity_df['proteins_100g'] / opportunity_df['safe_sugar']

    # Metric 1: Total Count
    opportunity_count = opportunity_df.shape[0]
    st.metric(label="Products in Opportunity Zone", value=opportunity_count)
    
    if not opportunity_df.empty:
        # Metric 2: Volume Winner (The Category with the MOST items)
        top_vol_cat = opportunity_df['high_level_category'].value_counts().idxmax()
        top_vol_count = opportunity_df['high_level_category'].value_counts().max()
        st.metric(
            label="🏆 Most Options (Volume)", 
            value=top_vol_cat, 
            delta=f"{top_vol_count} products"
        )

        # Metric 3: Quality Winner (The Category with the BEST Average Ratio)
        # We group by category and take the MEAN of the ratio
        best_ratio_cat = opportunity_df.groupby('high_level_category')['ratio'].mean().idxmax()
        best_ratio_val = opportunity_df.groupby('high_level_category')['ratio'].mean().max()
        
        st.metric(
            label="🚀 Best Nutrition (Avg Ratio)", 
            value=best_ratio_cat, 
            delta=f"{best_ratio_val:.1f} P:S Ratio",
            help="Average Protein-to-Sugar ratio for products in the zone."
        )
    else:
        st.warning("No products found in the Opportunity Zone with current filters.")

    st.info("The 'Opportunity Zone' is defined as >15g Protein and <5g Sugar.")

# --- LEADERBOARD SECTION (Bottom) ---
st.markdown("---")
st.subheader(f"🏆 Top 5 High-Protein Products per Category")

# 1. Calculate the Ratio SAFELY
# We create a temporary 'safe_sugar' column where 0 is replaced by 0.1
# This avoids division by zero errors while keeping the math sortable.
filtered_df['safe_sugar'] = filtered_df['sugars_100g'].replace(0, 0.1)
filtered_df['protein_sugar_ratio'] = filtered_df['proteins_100g'] / filtered_df['safe_sugar']

# 2. Logic to get Top 5
top_products = (
    filtered_df
    .sort_values(by=['protein_sugar_ratio'], ascending=False) # Sort by your new Ratio!
    .groupby('high_level_category')
    .head(5)
    # Select the columns to display
    [['high_level_category', 'product_name', 'proteins_100g', 'sugars_100g', 'protein_sugar_ratio']]
)

# 3. Display with nice formatting
st.dataframe(
    top_products, 
    use_container_width=True,
    hide_index=True,
    column_config={
        "high_level_category": "Category",
        "product_name": "Product Name",
        "proteins_100g": st.column_config.NumberColumn("Protein (g)", format="%.1f"),
        "sugars_100g": st.column_config.NumberColumn("Sugar (g)", format="%.1f"),
        "protein_sugar_ratio": st.column_config.NumberColumn(
            "Protein:Sugar Ratio", 
            format="%.1f x", # Displays as "5.0 x" (5 times more protein than sugar)
            help="Higher is better. Shows how much Protein you get for every 1g of Sugar."
        ),
    }
)