from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
import io

app = FastAPI()

# CORS: allow browser calls from the deployed site and localhost
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
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

# On Vercel, requests to /api/generate are routed here
@app.post("/generate")
async def generate(file: UploadFile, theme: str = Form(...)):
    content = await file.read()
    text_stream = io.StringIO(content.decode('utf-8', errors='ignore'))
    reader = csv.DictReader(text_stream)
    inventory_items = []
    for row in reader:
        value = row.get('item')
        if value is None:
            # try first column if header differs
            if len(row.values()):
                value = list(row.values())[0]
        if value is not None and str(value).strip():
            inventory_items.append(str(value).strip().lower())
	generator = RecipeGenerator(inventory_items, theme)
	recipes = generator.generate_recipes()
	return JSONResponse(content={"recipes": recipes})

# Alias to support Vercel forwarding full path /api/generate
@app.post("/api/generate")
async def generate_alias(file: UploadFile, theme: str = Form(...)):
	return await generate(file=file, theme=theme)
