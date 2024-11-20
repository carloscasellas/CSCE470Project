import json
import math
import heapq

bow = []


def train(recipes):
    for recipe in recipes:
        vector = dict()
        for ingredientProps in recipe["ingredients"]:
            vector[ingredientProps["ingredient"]] = 1
        bow.append((recipe["url"], vector, recipe["category"]))


def rank(query):
    qVector = dict()
    for term in query:
        qVector[term] = query[term]

    scoredList = []
    for item in bow:
        distance = neighborDistance(qVector, item[1])
        heapq.heappush(scoredList, (-1 * distance, item[0], item[2]))

    return scoredList


def neighborDistance(A, B):
    magnitudeA = math.sqrt(sum(x**2 for x in A.values()))
    magnitudeB = math.sqrt(sum(x**2 for x in B.values()))

    dotProduct = sum(A.get(k, 0) * B.get(k, 0) for k in set(A) | set(B))

    return dotProduct / (magnitudeA * magnitudeB)


def run(recipes, query):
    train(recipes)
    scoredList = rank(query)

    ranked_recipes = []
    while scoredList:
        item = heapq.heappop(scoredList)
        ranked_recipes.append({"url": item[1], "score": -item[0], "category": item[2]})

    # print(f"Ranked recipes: {len(ranked_recipes)}")
    return ranked_recipes


if __name__ == "__main__":
    query = {"curry powder": 1, "shrimp": 5, "cinnamon stick": 1}
    with open("./src/backend/filtered_recipes.json", "r") as file:
        filtered_recipes = json.load(file)
        ranked_recipes = run(filtered_recipes, query)

        with open("./src/backend/ranked_recipes.json", "w") as output:
            json.dump(ranked_recipes, output, indent=4)
