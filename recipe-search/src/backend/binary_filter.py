import json

def exclude_ingredients(ingredients_list, recipes):
    filtered = []
    for recipe in recipes:
        append = True
        for recipe_ingredient in recipe['ingredients']:
            for ingredient in ingredients_list:
                if ingredient in recipe_ingredient['ingredient']:
                    append = False
                    break
                if not append:
                    break
        if append and len(recipe['ingredients']) > 0:
            filtered.append(recipe)
    return filtered

def filter_cuisine(cuisine_list, recipes):
    filtered = []
    for cuisine in cuisine_list:
        for recipe in recipes:
            if cuisine in recipe["category"]:
                filtered.append(recipe)
    return filtered

if __name__ == "__main__":
    exclude_ingredients_list = []
    cuisine_list = ['mexican', 'africa', 'moroccan']   
    with open('./src/backend/recipes.json', 'r') as file:
        recipes = json.load(file)
        filtered_recipes = exclude_ingredients(exclude_ingredients_list, filter_cuisine(cuisine_list, recipes))
        with open('./src/backend/filtered_recipes.json', 'w') as output:
            json.dump(filtered_recipes, output, indent=4)