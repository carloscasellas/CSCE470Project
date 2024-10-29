import requests
from bs4 import BeautifulSoup
import time
import json
import re

BASE_URL = "https://www.curiouscuisiniere.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}

units = set({"tbsp", "tsp", "g", "cups", "cup", "oz", "c", "teaspoon", "ounces", "tablespoons", "grams", "kg", "kilograms"})
symbols = set({"+", "-", "*"})

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print(f"Failed to fetch {url}: Status code {response.status_code}")
        return None

def extract_category(soup):
    breadcrumbs = soup.find("p", {"class": "breadcrumbs"})
    if breadcrumbs:
        category = [crumb.get_text().strip() for crumb in breadcrumbs.find_all("a")]
        if len(category) > 1:
            return category[-1]
    return "Unknown"

def turn_to_minutes(text):
    minutes = 0
    contents = text.split(" ")
    for i in range(len(contents)):
        if contents[i] == "hour" or contents[i] == "hours":
            minutes += int(contents[i-1]) * 60
        if contents[i] == "minute" or contents[i] == "minutes":
            minutes += int(contents[i-1])
    return minutes

def extract_time(soup):
    time_tag = soup.find("span", {"class": "mv-time-part"})  # Adjust class if needed
    if time_tag:
        return turn_to_minutes(time_tag.get_text().strip())
        
    return "N/A"

def parse_ingredient(ingredient):
    text = ingredient.lower().split(" ")
    indices = set()
    for i in range(len(text)):
        if text[i] in units:
            indices.add(i)
            indices.add(i - 1)
            
        if text[i][0] == "(":
            for j in range(i, len(text)):
                indices.add(j)
                        
        if text[i][-1] == ",":
            for j in range(i + 1, len(text)):
                indices.add(j)
            text[i] = text[i][0:-1]
            
        if text[i][0].isdigit():
            indices.add(i)
        
        if len(text[i]) > 0 and text[i][0] in symbols:
            text[i] = text[i][1:]
        
        if len(text[i]) > 0 and text[i][-1] in symbols:
            text[i] = text[i][:-1]
    
    newText = []
    
    for i in range(len(text)):
        if not (i in indices):
            newText.append(text[i])
    
    return " ".join(newText)
    
def extract_ingredients(soup):
    words = set()
    ingredients_section = soup.find("div", {"class": "mv-create-ingredients"})
    if ingredients_section:
        ingredients_list = ingredients_section.find_all('li')
        for item in ingredients_list:
            parsed_ingredient = parse_ingredient(item.get_text().strip())
            words.update(parsed_ingredient.split())
        return list(words)

def extract_recipe_data(recipe_url):
    soup = get_soup(recipe_url)
    if soup:
        category = extract_category(soup)
        prep_time = extract_time(soup)
        ingredients = extract_ingredients(soup)

        recipe_data = {
            "url": recipe_url,
            "category": category,
            "preparation_time": prep_time,
            "ingredients": ingredients,
        }
        return recipe_data
    return None

def scrape_recipes(recipe_urls):
    all_recipes = []
    for url in recipe_urls:
        data = extract_recipe_data(url)
        if data:
            all_recipes.append(data)
        time.sleep(2)
    return all_recipes

# TODO: Extract URLs from site directly
example_urls = [
    "https://www.curiouscuisiniere.com/chicken-pastilla-moroccan-chicken-pie/",
    "https://www.curiouscuisiniere.com/har-gow-shrimp-dumplings/",
    "https://www.curiouscuisiniere.com/pavlova-wreath/",
    "https://www.curiouscuisiniere.com/honduran-baleadas/",
    "https://www.curiouscuisiniere.com/whole-wheat-pita-bread/",
    "https://www.curiouscuisiniere.com/liptauer-cheese-spread/",
    "https://www.curiouscuisiniere.com/ecuadorian-shrimp-ceviche/",
]

scraped_data = scrape_recipes(example_urls)

with open("recipes.json", "w") as f:
    json.dump(scraped_data, f, indent=4)

print("Scraping completed")
