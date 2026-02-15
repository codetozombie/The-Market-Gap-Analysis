# Market Gap Analysis: Open Food Facts

## A. The Executive Summary
This market analysis of the Open Food Facts dataset reveals a significant "Blue Ocean" opportunity in the Meat & Seafood snack category, which remains underserved compared to the saturated, high-sugar Energy Bar market. The data identifies a specific "Opportunity Zone" for products containing over 37g of protein and less than 1.6g of sugar per 100g, targets that maximize nutritional value for health-conscious consumers. Furthermore, the "Candidate's Choice" complexity analysis confirms that Meat & Seafood snacks offer a decisive "Clean Label" advantage, averaging a median of ~12 ingredients compared to ~25 ingredients in competitor cereal bars. Consequently, the recommended strategy is to launch a high-protein, savory snack that competes on both superior macronutrients and ingredient simplicity.

## B. Project Links
* **Notebook:** The full analysis code, PDF, and HTML reports can be found in the [GitHub Repository](https://github.com/codetozombie/amalitech_nss).
* **Dashboard:** [Interactive Streamlit Dashboard](https://codetozombie-amalitech-nss-app-iirfmj.streamlit.app/)
* **Presentation:** [Link to Slides (PDF/PPT)](https://ugedugh-my.sharepoint.com/:p:/g/personal/ankamoako_st_ug_edu_gh/IQAwgeSfabzwSJgxo-naogyVATivDB1el0Zc5WeGf5My4oU?e=csbPt0)
* **Video Walkthrough :** [Link to YouTube](https://youtu.be/sYY7Z_WsLF4)

## C. Technical Explanation

### Data Cleaning Strategy
The data cleaning process was executed in `helpers/task_1.ipynb` and encapsulated in a reusable `wrangle` function. The approach focused on data integrity and removing noise:
1.  **Scope Filtering:** The dataset was strictly subsetted to relevant "Snack" categories.
2.  **Dimensionality Reduction:** Dropped columns with >80% missing values and administrative metadata (e.g., `url`, `created_t`, `states_tags`) that offered no analytical value.
3.  **Imputation:** Missing values in `product_name` and `countries_en` were labeled as "Unknown." Statistical mode imputation was used for the `nova_group` (processing level).
4.  **Outlier Removal & Biological Limits:**
    * Removed rows exceeding theoretical nutritional limits (e.g., Energy > 900 kcal/100g, Macronutrients > 100g/100g).
    * Enforced logical constraints (e.g., Saturated Fat must be ≤ Total Fat).
    * Removed Nutri-Score outliers (< -15 or > 40).

### Candidate's Choice: Ingredient Complexity Analysis
For the "Candidate's Choice" requirement, I developed a **Clean Label/Ingredient Complexity Metric**.
* **Goal:** To determine which high-protein categories offer a "cleaner" product profile to appeal to health-conscious consumers avoiding ultra-processed foods (UPFs).
* **Implementation:** I engineered a feature `ingredient_count` by parsing the comma-separated `ingredients_text`.
* **Result:** A comparative analysis revealed that **Meat & Seafood** snacks (Median ~12 ingredients) are significantly "cleaner" than **Energy & Cereal Bars** (Median ~25 ingredients). This strengthens the recommendation to pivot toward savory protein snacks, as they compete on both macronutrients and ingredient simplicity.

---

## Methodology: Category Engineering

To ensure accurate analysis, raw category data was normalized and reclassified using a **Hierarchical Keyword Matching System**.

### 1. Text Preparation
Fields (`categories_en`, `product_name`) were combined, lowercased, and normalized (hyphens converted to spaces) to create a searchable text string.

### 2. Priority-Based Assignment
Categories were assigned based on a "Waterfall" priority logic—matches at Level 1 override matches at Level 5.

* **Level 1 (Non-Snack/Meals):** Beverages, Supplements, Meals & Sandwiches.
* **Level 2 (High Value/Natural):** Meat & Seafood, Fruit & Veggie, Nuts & Seeds, Dairy.
* **Level 3 (Salty):** Chips & Popcorn.
* **Level 4 (Sweet):** Breakfast/Cereals, Energy Bars, Biscuits/Cakes, Chocolates.
* **Level 5 (Fallback):** Savory Misc, Plant-Based Misc.

*If no keywords matched, the product was labeled "Other Snacks".*

---

## Dashboard Features

The Streamlit dashboard allows stakeholders to visualize the "Opportunity Zone" (High Protein, Low Sugar).

* **Opportunity Zone Definition:** Products containing **Sugar < 5g/100g** AND **Protein > 20g/100g**.
* **Leaderboard:** Ranks top products by their Protein-to-Sugar ratio.
* **Ingredient Drivers:** Identifies that **Chicken**, **Dairy**, and **Beef** are the primary protein drivers in the current opportunity zone.

---

## Project Structure

* `main.ipynb`: The primary analysis notebook.
* `app.py`: Source code for the Streamlit visualization dashboard.
* `helpers/`: Contains the cleaning scripts and data wrangling functions.
* `dataset/`:
    * `snacks.csv`: The cleaned, processed data used for visualization.
    * *Note: Raw data is not included due to size.*
* `requirements.txt`: Python dependencies.

---

## How to Run Locally

### 1. Setup
Clone the repository:
```bash
git clone [https://github.com/codetozombie/amalitech_nss](https://github.com/codetozombie/amalitech_nss)
cd amalitech_nss
```

### 2. Data Acquisition
Create a dataset folder. Download the Open Food Facts CSV. To replicate the analysis on the first 100,000 rows, run the following command for your OS:

Windows (PowerShell):
```bash
Get-Content "en.openfoodfacts.org.products.csv" -TotalCount 100000 | Set-Content "dataset/openfoodfacts_100k.csv"
```
Mac/Linux (Terminal):
```bash
head -n 100000 en.openfoodfacts.org.products.csv > dataset/openfoodfacts_100k.csv
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Analysis
Open main.ipynb in Jupyter or VS Code and run all cells.

### 5. Launch Dashboard
```bash
streamlit run app.py
```

## 🛑 CRITICAL: Pre-Submission Checklist

**Before you submit your form, you MUST complete this checklist.**

> ⚠️ **WARNING:** If you miss any of these items, your submission will be flagged as "Incomplete" and you will **NOT** be invited to an interview. 
>
> **We do not accept "permission error" excuses. Test your links in Incognito Mode.**

### 1. Repository & Code Checks
- [x] **My GitHub Repo is Public.** (Open the link in a Private/Incognito window to verify).
- [x] **I have uploaded the `.ipynb` notebook file.**
- [x] **I have ALSO uploaded an HTML or PDF export** of the notebook.
- [x] **I have NOT uploaded the massive raw dataset.** (Use `.gitignore` or just don't commit the CSV).
- [x] **My code uses Relative Paths.** 

### 2. Deliverable Checks
- [x] **My Dashboard link is publicly accessible.** (No login required).
- [x] **My Presentation link is publicly accessible.** (Permissions set to "Anyone with the link can view").
- [x] **I have updated this `README.md` file** with my Executive Summary and technical notes.

### 3. Completeness
- [x] I have completed **User Stories 1-4**.
- [x] I have completed the **"Candidate's Choice"** challenge and explained it in the README.

**✅ Only when you have checked every box above, proceed to the submission form.**

---
