import json


def exclude_ingredients(ingredients_list, recipes):
    filtered = []
    for recipe in recipes:
        append = True
        for recipe_ingredient in recipe["ingredients"]:
            for ingredient in ingredients_list:
                if ingredient in recipe_ingredient["ingredient"]:
                    append = False
                    break
                if not append:
                    break
        if append and len(recipe["ingredients"]) > 0:
            filtered.append(recipe)
    return filtered


def filter_cuisine(cuisine_list, recipes):
    filtered = []
    for cuisine in cuisine_list:
        for recipe in recipes:
            if cuisine in recipe["category"]:
                filtered.append(recipe)
    return filtered


def run(recipes, exclude_ingredients_list, cuisine_list):
    cuisine_list = [cuisine.lower() for cuisine in cuisine_list]
    filtered_recipes = exclude_ingredients(
        exclude_ingredients_list, filter_cuisine(cuisine_list, recipes)
    )
    # print(f"Filtered recipes: {len(filtered_recipes)}")
    return filtered_recipes


if __name__ == "__main__":
    with open("./src/backend/recipes.json", "r") as file:
        recipes = json.load(file)
        exclude_ingredients_list = []
        cuisine_list = ["mexican", "africa", "moroccan"]
        filtered_recipes = run(recipes, exclude_ingredients_list, cuisine_list)
        with open("./src/backend/filtered_recipes.json", "w") as output:
            json.dump(filtered_recipes, output, indent=4)
