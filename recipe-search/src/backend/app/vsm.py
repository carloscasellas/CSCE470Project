import json
import math
import heapq
from collections import defaultdict

def train(recipes):
    bow = []
    for recipe in recipes:
        vector = dict()
        for ingredientProps in recipe["ingredients"]:
            vector[ingredientProps["ingredient"]] = 5  # Consider adjusting this value or using TF-IDF
        bow.append((recipe["url"], vector, recipe["category"]))
    return bow

def neighborDistance(A, B):
    magnitudeA = math.sqrt(sum(x**2 for x in A.values()))
    magnitudeB = math.sqrt(sum(x**2 for x in B.values()))
    dotProduct = sum(A.get(k, 0) * B.get(k, 0) for k in set(A) | set(B))
    if magnitudeA == 0 or magnitudeB == 0:
        return 0
    return dotProduct / (magnitudeA * magnitudeB)

def rank(query, bow):
    qVector = query.copy()  # Ensure we don't modify the original query
    scoredList = []
    for item in bow:
        distance = neighborDistance(qVector, item[1])
        heapq.heappush(scoredList, (-1 * distance, item[0], item[2]))
    return scoredList

def run(recipes, query):
    bow = train(recipes)          # Now bow is local to this function
    scoredList = rank(query, bow) # Pass bow to rank()
    ranked_recipes = []
    while scoredList:
        item = heapq.heappop(scoredList)
        ranked_recipes.append({
            "url": item[1],
            "score": -item[0],
            "category": item[2]
        })
    return ranked_recipes

if __name__ == "__main__":
    query = {"curry powder": 1, "shrimp": 5, "cinnamon stick": 1}
    with open("./src/backend/app/filtered_recipes.json", "r") as file:
        filtered_recipes = json.load(file)
        ranked_recipes = run(filtered_recipes, query)
        with open("./src/backend/app/ranked_recipes.json", "w") as output:
            json.dump(ranked_recipes, output, indent=4)
