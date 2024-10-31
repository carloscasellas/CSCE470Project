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

def parse_category(category):
    
    category = category.lower()
    
    if "recipes from" in category:
        category = category.replace("recipes from", "").strip()
        
    if "recipes" in category:
        category = category.replace("recipes", "").strip()
        
    return category

def extract_category(soup):
    breadcrumbs = soup.find("p", {"class": "breadcrumbs"})
    if breadcrumbs:
        category = [crumb.get_text().strip() for crumb in breadcrumbs.find_all("a")]
        if len(category) > 1:
            return parse_category(category[-1])
    return "Unknown"

def turn_to_minutes(text):
    minutes = 0
    contents = text.split(" ")
    for i in range(len(contents)):
        if contents[i] == "hour" or contents[i] == "hours" or contents[i] == "hr" or contents[i] == "hrs":
            minutes += int(contents[i-1]) * 60
        if contents[i] == "minute" or contents[i] == "minutes" or contents[i] == "min" or contents[i] == "mins":
            minutes += int(contents[i-1])
    return minutes

def extract_time(soup):
    time_tag = soup.find("span", {"class": "mv-time-part"})  # Adjust class if needed
    if time_tag:
        return turn_to_minutes(time_tag.get_text().strip())
    elif soup.find("span", {"class": "wprm-recipe-total_time"}):
        return turn_to_minutes(soup.find("span", {"class": "wprm-recipe-total_time"}).get_text().strip())
        
    return "N/A"

def parse_ingredient(ingredient):
    text = ingredient.lower().split(" ")
    indices = set()
    for i in range(len(text)):
        if text[i] in units:
            indices.add(i)
            indices.add(i - 1)
            
        if len(text[i]) > 0 and text[i][0] == "(":
            for j in range(i, len(text)):
                indices.add(j)
                        
        if len(text[i]) > 0 and text[i][-1] == ",":
            for j in range(i + 1, len(text)):
                indices.add(j)
            text[i] = text[i][0:-1]
            
        if len(text[i]) > 0 and text[i][0].isdigit():
            indices.add(i)
        
        if len(text[i]) > 0 and text[i][0] in symbols:
            text[i] = text[i][1:]
        
        if len(text[i]) > 0 and text[i][-1] in symbols:
            text[i] = text[i][:-1]
            
        if len(text[i]) > 0 and any(ord(char) > 127 for char in text[i]):
            indices.add(i)
    
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
    elif soup.find("ul", {"class": "wprm-recipe-ingredients"}):
        ingredients_list = soup.find_all("span", {"class": "wprm-recipe-ingredient-name"})
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
        print("Scraping " + url)
        data = extract_recipe_data(url)
        if data:
            all_recipes.append(data)
        time.sleep(2)
    return all_recipes

def find_recipe_urls(page_urls):
    recipe_urls = []
    for url in page_urls:
        soup = get_soup(url)
        titles = soup.find_all("h2", {"class": "excerpt-title"})
        for title in titles:
            link = title.find("a", href=True)
            recipe_urls.append(link["href"])
    return scrape_recipes(recipe_urls)


page_urls = [
    "https://www.curiouscuisiniere.com/africa/",
    "https://www.curiouscuisiniere.com/africa/page/2/",
    "https://www.curiouscuisiniere.com/europe/british/",
    "https://www.curiouscuisiniere.com/europe/british/page/2/",
    "https://www.curiouscuisiniere.com/north-america/caribbean/",
    "https://www.curiouscuisiniere.com/asia/chinese/",
    "https://www.curiouscuisiniere.com/asia/chinese/page/2/",
    "https://www.curiouscuisiniere.com/europe/french/",
    "https://www.curiouscuisiniere.com/europe/french/page/2/",
    "https://www.curiouscuisiniere.com/europe/french/page/3/",
    "https://www.curiouscuisiniere.com/europe/french/page/4/",
    "https://www.curiouscuisiniere.com/europe/german/",
    "https://www.curiouscuisiniere.com/europe/german/page/2/",
    "https://www.curiouscuisiniere.com/europe/greek/",
    "https://www.curiouscuisiniere.com/europe/greek/page/2/",
    "https://www.curiouscuisiniere.com/asia/indian/",
    "https://www.curiouscuisiniere.com/asia/indian/page/2/",
    "https://www.curiouscuisiniere.com/europe/italian/",
    "https://www.curiouscuisiniere.com/europe/italian/page/2/",
    "https://www.curiouscuisiniere.com/europe/italian/page/3/",
    "https://www.curiouscuisiniere.com/europe/italian/page/4/",
    "https://www.curiouscuisiniere.com/europe/italian/page/5/",
    "https://www.curiouscuisiniere.com/asia/japanese/",
    "https://www.curiouscuisiniere.com/north-america/mexican/",
    "https://www.curiouscuisiniere.com/north-america/mexican/page/2/",
    "https://www.curiouscuisiniere.com/north-america/mexican/page/3/",
    "https://www.curiouscuisiniere.com/europe/polish/",
    "https://www.curiouscuisiniere.com/asia/southeast-asia/thai/",
    "https://www.curiouscuisiniere.com/north-america/american/",
    "https://www.curiouscuisiniere.com/north-america/american/page/2/",
    "https://www.curiouscuisiniere.com/north-america/american/page/3/",
    "https://www.curiouscuisiniere.com/north-america/american/page/4/",
    "https://www.curiouscuisiniere.com/north-america/american/page/5/",
    "https://www.curiouscuisiniere.com/north-america/american/page/6/",
    "https://www.curiouscuisiniere.com/north-america/american/page/7/",
    "https://www.curiouscuisiniere.com/north-america/american/page/8/",
    "https://www.curiouscuisiniere.com/north-america/american/page/9/",
    "https://www.curiouscuisiniere.com/north-america/american/page/10/",
    "https://www.curiouscuisiniere.com/north-america/american/page/11/",
    "https://www.curiouscuisiniere.com/north-america/american/page/12/",
]

scraped_data = find_recipe_urls(page_urls)

with open("recipes.json", "w") as f:
    json.dump(scraped_data, f, indent=4)

print("Scraping completed")
