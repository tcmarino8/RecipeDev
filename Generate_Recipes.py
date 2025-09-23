import streamlit as st
import pandas as pd
import random

class RecipeGenerator:
    def __init__(self, inventory, cuisine_theme):
        self.inventory = set(inventory)
        self.cuisine_theme = cuisine_theme.lower()
        self.recipe_templates = {
            "breakfast": [
                {"name": "Omelette", "ingredients": ["eggs", "milk", "cheese", "spinach"]},
                {"name": "Pancakes", "ingredients": ["flour", "milk", "eggs", "syrup"]},
            ],
            "bbq": [
                {"name": "Grilled Chicken", "ingredients": ["chicken", "bbq sauce", "salt", "pepper"]},
                {"name": "Veggie Skewers", "ingredients": ["bell pepper", "onion", "zucchini", "olive oil"]},
            ],
            "thai": [
                {"name": "Pad Thai", "ingredients": ["rice noodles", "egg", "peanuts", "bean sprouts"]},
                {"name": "Green Curry", "ingredients": ["coconut milk", "green curry paste", "chicken", "basil"]},
            ]
        }

    def generate_recipes(self):
        templates = self.recipe_templates.get(self.cuisine_theme, [])
        possible_recipes = []
        for recipe in templates:
            if set(recipe["ingredients"]).issubset(self.inventory):
                possible_recipes.append(recipe)
        return possible_recipes

st.title("AI Recipe Generator")

uploaded_file = st.file_uploader("Upload your inventory CSV", type="csv")
theme = st.selectbox("Select cuisine theme", ["Breakfast", "BBQ", "Thai"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    inventory_items = df["item"].str.lower().tolist()
    generator = RecipeGenerator(inventory_items, theme)
    recipes = generator.generate_recipes()
    if recipes:
        st.subheader("Recipes you can make:")
        for recipe in recipes:
            st.markdown(f"**{recipe['name']}**")
            st.write(", ".join(recipe["ingredients"]))
    else:
        st.warning("No recipes found with your inventory and selected theme.")
        # To run this Streamlit app, open a terminal and execute:
        # streamlit run "/C:/Users/Tyler Marino/OneDrive/Desktop/Generate_Recipes.py"
        # Make sure you have installed streamlit and pandas:
        # pip install streamlit pandas