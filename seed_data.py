# -*- coding: utf-8 -*-
"""
Starter food database used to seed the SQLite `foods` table the first time
the app runs. Values are approximate per-serving macros (grams of protein,
carbs, fat) and calories, gathered from common public nutrition references
(USDA FoodData Central style figures). They are meant as reasonable
defaults, not medical-grade nutrition facts -- users can add their own
custom foods from the UI, which take priority in search results.

Each tuple is: (name, serving_desc, calories, protein_g, carbs_g, fat_g)
"""

FOODS = [
    # Fruits
    ("Apple", "1 medium (182g)", 95, 0.5, 25.0, 0.3),
    ("Banana", "1 medium (118g)", 105, 1.3, 27.0, 0.4),
    ("Orange", "1 medium (131g)", 62, 1.2, 15.4, 0.2),
    ("Strawberries", "1 cup (152g)", 49, 1.0, 11.7, 0.5),
    ("Blueberries", "1 cup (148g)", 84, 1.1, 21.4, 0.5),
    ("Grapes", "1 cup (151g)", 104, 1.1, 27.3, 0.2),
    ("Avocado", "1/2 fruit (100g)", 160, 2.0, 8.5, 14.7),
    ("Mango", "1 cup sliced (165g)", 99, 1.4, 24.7, 0.6),
    ("Pineapple", "1 cup chunks (165g)", 82, 0.9, 21.6, 0.2),
    ("Watermelon", "1 cup diced (152g)", 46, 0.9, 11.5, 0.2),

    # Vegetables
    ("Broccoli", "1 cup chopped (91g)", 31, 2.6, 6.0, 0.3),
    ("Spinach", "1 cup raw (30g)", 7, 0.9, 1.1, 0.1),
    ("Carrot", "1 medium (61g)", 25, 0.6, 6.0, 0.1),
    ("Sweet Potato", "1 medium baked (114g)", 103, 2.3, 23.6, 0.2),
    ("Potato (baked)", "1 medium (173g)", 161, 4.3, 36.6, 0.2),
    ("Tomato", "1 medium (123g)", 22, 1.1, 4.8, 0.2),
    ("Cucumber", "1 cup sliced (104g)", 16, 0.7, 3.8, 0.1),
    ("Bell Pepper", "1 medium (119g)", 24, 1.0, 5.5, 0.2),
    ("Onion", "1/2 cup chopped (80g)", 32, 0.9, 7.5, 0.1),
    ("Mixed Salad Greens", "2 cups (60g)", 15, 1.2, 2.8, 0.2),

    # Grains & starches
    ("White Rice (cooked)", "1 cup (158g)", 205, 4.3, 44.5, 0.4),
    ("Brown Rice (cooked)", "1 cup (195g)", 216, 5.0, 44.8, 1.8),
    ("Quinoa (cooked)", "1 cup (185g)", 222, 8.1, 39.4, 3.6),
    ("Oatmeal (cooked, plain)", "1 cup (234g)", 166, 5.9, 28.1, 3.6),
    ("White Bread", "1 slice (28g)", 75, 2.6, 13.8, 1.0),
    ("Whole Wheat Bread", "1 slice (28g)", 69, 3.6, 11.6, 1.1),
    ("Bagel (plain)", "1 medium (105g)", 289, 11.0, 56.0, 1.7),
    ("Pasta (cooked)", "1 cup (140g)", 221, 8.1, 43.2, 1.3),
    ("Tortilla (flour, 8in)", "1 tortilla (49g)", 146, 3.9, 24.3, 3.6),
    ("Popcorn (air-popped)", "3 cups (24g)", 93, 3.0, 18.6, 1.1),

    # Protein
    ("Chicken Breast (grilled)", "100g", 165, 31.0, 0.0, 3.6),
    ("Chicken Thigh (grilled)", "100g", 209, 26.0, 0.0, 10.9),
    ("Salmon (baked)", "100g", 206, 22.1, 0.0, 12.4),
    ("Tuna (canned in water)", "1 can, drained (142g)", 128, 28.2, 0.0, 0.8),
    ("Shrimp (cooked)", "100g", 99, 24.0, 0.2, 0.3),
    ("Ground Beef (85% lean, cooked)", "100g", 250, 25.9, 0.0, 15.7),
    ("Sirloin Steak (cooked)", "100g", 206, 29.0, 0.0, 9.0),
    ("Pork Chop (cooked)", "100g", 231, 25.7, 0.0, 13.7),
    ("Eggs", "1 large", 78, 6.3, 0.6, 5.3),
    ("Egg Whites", "1 large", 17, 3.6, 0.2, 0.1),
    ("Tofu (firm)", "100g", 144, 15.8, 3.5, 8.7),
    ("Black Beans (cooked)", "1 cup (172g)", 227, 15.2, 40.8, 0.9),
    ("Chickpeas (cooked)", "1 cup (164g)", 269, 14.5, 45.0, 4.2),
    ("Lentils (cooked)", "1 cup (198g)", 230, 17.9, 39.9, 0.8),
    ("Peanut Butter", "2 tbsp (32g)", 188, 8.0, 6.9, 16.0),
    ("Almonds", "1 oz / 23 nuts (28g)", 164, 6.0, 6.1, 14.2),
    ("Walnuts", "1 oz (28g)", 185, 4.3, 3.9, 18.5),

    # Dairy
    ("Milk (2%)", "1 cup (244g)", 122, 8.1, 11.7, 4.8),
    ("Milk (whole)", "1 cup (244g)", 149, 7.7, 11.7, 8.0),
    ("Almond Milk (unsweetened)", "1 cup (240g)", 39, 1.4, 1.6, 2.9),
    ("Greek Yogurt (plain, nonfat)", "1 cup (245g)", 133, 23.0, 9.0, 0.7),
    ("Yogurt (plain, whole milk)", "1 cup (245g)", 149, 8.5, 11.4, 8.0),
    ("Cheddar Cheese", "1 oz (28g)", 113, 7.0, 0.4, 9.3),
    ("Mozzarella Cheese (part-skim)", "1 oz (28g)", 72, 6.9, 0.8, 4.5),
    ("Cottage Cheese (low-fat)", "1 cup (226g)", 163, 28.0, 6.2, 2.3),
    ("Butter", "1 tbsp (14g)", 102, 0.1, 0.0, 11.5),

    # Fast food / restaurant staples
    ("Cheeseburger (fast food)", "1 sandwich", 300, 15.0, 33.0, 12.0),
    ("Chicken Sandwich (fast food)", "1 sandwich", 490, 28.0, 44.0, 23.0),
    ("French Fries (medium)", "1 medium order (117g)", 365, 4.0, 48.0, 17.0),
    ("Pizza (cheese, chain)", "1 slice (107g)", 285, 12.0, 36.0, 10.0),
    ("Burrito (chicken, chain)", "1 burrito (300g)", 600, 35.0, 70.0, 20.0),
    ("Caesar Salad (with dressing)", "1 entree salad", 470, 18.0, 15.0, 38.0),
    ("Sushi Roll (California)", "8 pieces (approx 250g)", 255, 9.0, 38.0, 7.0),
    ("Ramen (restaurant bowl)", "1 bowl", 550, 20.0, 65.0, 22.0),
    ("Taco (beef, hard shell)", "1 taco", 170, 8.0, 13.0, 10.0),
    ("Sub Sandwich (turkey, 6in)", "1 sandwich", 280, 18.0, 40.0, 4.5),

    # Snacks / sweets / beverages
    ("Potato Chips", "1 oz (28g)", 152, 2.0, 15.0, 10.0),
    ("Dark Chocolate (70-85%)", "1 oz (28g)", 170, 2.2, 13.0, 12.0),
    ("Milk Chocolate Bar", "1 bar (44g)", 235, 3.4, 26.0, 13.0),
    ("Granola Bar", "1 bar (35g)", 140, 3.0, 22.0, 5.0),
    ("Ice Cream (vanilla)", "1/2 cup (66g)", 137, 2.3, 15.9, 7.3),
    ("Cookie (chocolate chip)", "1 medium (16g)", 78, 0.9, 9.6, 4.5),
    ("Donut (glazed)", "1 donut (60g)", 240, 3.6, 27.0, 13.0),
    ("Soda (cola)", "12 fl oz (355ml)", 140, 0.0, 39.0, 0.0),
    ("Orange Juice", "1 cup (248g)", 112, 1.7, 25.8, 0.5),
    ("Coffee (black)", "1 cup (240ml)", 2, 0.3, 0.0, 0.0),
    ("Latte (2% milk)", "12 fl oz", 137, 8.0, 13.0, 5.0),
    ("Beer (regular)", "12 fl oz (355ml)", 153, 1.6, 13.0, 0.0),
    ("Wine (red)", "5 fl oz (147ml)", 125, 0.1, 3.8, 0.0),
    ("Protein Shake (whey, water)", "1 scoop (30g) in water", 120, 24.0, 3.0, 1.5),
    ("Hummus", "2 tbsp (30g)", 70, 2.0, 4.0, 5.0),
    ("Trail Mix", "1/4 cup (35g)", 173, 5.0, 16.0, 11.0),
]
