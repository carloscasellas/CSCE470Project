from flask import Blueprint, jsonify, request
import json
import heapq
from .binary_filter import run as filter_run
from .vsm import run as vsm_run
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

recipes_bp = Blueprint('recipes_bp', __name__)

@recipes_bp.route("/recipes", methods=["POST"])
def get_recipes():
    body = request.get_json()
    logging.info(f"Received request body: {body}")
    
    ingredients = body.get("ingredients")
    cultures = body.get("cultures")
    excluded_ingredients = body.get("excludedIngredients")

    if not ingredients:
        logging.warning("No ingredients provided in the request.")
        return jsonify({"error": "No ingredients provided"}), 400

    if not cultures:
        logging.warning("No cultures provided in the request.")
        return jsonify({"error": "No cultures provided"}), 400

    # Translate ingredients from list of dicts to a single dict
    ingredients_dict = {ingredient["value"]: ingredient["rank"] for ingredient in ingredients}
    logging.info(f"Translated ingredients: {ingredients_dict}")

    try:
        with open("./app/recipes.json", "r") as f:
            recipes = json.load(f)
            logging.info(f"Loaded {len(recipes)} recipes.")

        # Filter recipes
        filtered_recipes = filter_run(recipes, excluded_ingredients, cultures)
        logging.info(f"Filtered down to {len(filtered_recipes)} recipes.")

        # Rank recipes using VSM
        ranked_recipes = vsm_run(filtered_recipes, ingredients_dict)
        logging.info(f"Ranked {len(ranked_recipes)} recipes.")

        return jsonify({"recipes": ranked_recipes}), 200

    except FileNotFoundError:
        logging.error("recipes.json not found.")
        return jsonify({"error": "recipes.json not found"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
