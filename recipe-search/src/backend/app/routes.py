from flask import jsonify, current_app, request
from flask_cors import cross_origin
import json
from . import binary_filter, vsm

app = current_app


@app.route("/recipes", methods=["POST"])
@cross_origin()
def get_recipes():
    body = request.get_json()
    ingredients = body.get("ingredients")
    cultures = body.get("cultures")
    excluded_ingredients = body.get("excludedIngredients")

    # translate ingredients from [{value: "ingredient", rank: 1}] to [{ingredient: 1}]
    ingredients = {
        ingredient["value"]: ingredient["rank"] for ingredient in ingredients
    }

    # print(f"Ingredients: {ingredients}")
    # print(f"Cultures: {cultures}")
    # print(f"Excluded Ingredients: {excluded_ingredients}")

    with open("./recipes.json", "r") as f:
        recipes = json.load(f)
        # print(f"Loaded {len(recipes)} recipes")
        filtered_recipes = binary_filter.run(recipes, excluded_ingredients, cultures)
        ranked_recipes = vsm.run(filtered_recipes, ingredients)

    return jsonify(ranked_recipes)
