from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS for local dev and common deploy hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        "*"  # Relaxed for demos; tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/generate")
async def generate(file: UploadFile, theme: str = Form(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    inventory_items = df["item"].str.lower().tolist()
    generator = RecipeGenerator(inventory_items, theme)
    recipes = generator.generate_recipes()
    return JSONResponse(content={"recipes": recipes})

# Alias route to support /api prefix used by frontend and Vercel rewrite
@app.post("/api/generate")
async def generate_alias(file: UploadFile, theme: str = Form(...)):
    return await generate(file=file, theme=theme)