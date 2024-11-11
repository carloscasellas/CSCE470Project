import requests
from bs4 import BeautifulSoup
import time
import json
import re
import string

BASE_URL = "https://www.curiouscuisiniere.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}

units = set(
    {
        "teaspoon",
        "teaspoons",
        "tsp",
        "t",
        "tablespoon",
        "tablespoons",
        "tbsp",
        "T",
        "c",
        "cup",
        "cups",
        "pint",
        "pints",
        "pt",
        "quart",
        "quarts",
        "qt",
        "gallon",
        "gallons",
        "gal",
        "milliliter",
        "milliliters",
        "ml",
        "liter",
        "liters",
        "l",
        "ounce",
        "ounces",
        "oz",
        "pound",
        "pounds",
        "lb",
        "lbs",
        "gram",
        "grams",
        "g",
        "kilogram",
        "kilograms",
        "kg",
        "pinch",
        "dash",
        "clove",
        "cloves",
        "slice",
        "slices",
        "package",
        "packages",
        "pkg",
        "can",
        "cans",
        "stick",
        "sticks",
        "piece",
        "pieces",
        "drop",
        "drops",
        "bunch",
        "bunches",
        "head",
        "heads",
        # Add more as needed
    }
)

symbols = set({"+", "-", "*"})


def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print(f"Failed to fetch {url}: Status code {response.status_code}")
        return None
    
def extract_name(soup):
        breadcrumbs = soup.find("p", {"class": "breadcrumbs"})
    if breadcrumbs:
        category = [crumb.get_text().strip() for crumb in breadcrumbs.find_all("a")]
        if len(category) > 1:
            return parse_category(category[-1])
    return "Unknown"


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
        if (
            contents[i] == "hour"
            or contents[i] == "hours"
            or contents[i] == "hr"
            or contents[i] == "hrs"
        ):
            minutes += int(contents[i - 1]) * 60
        if (
            contents[i] == "minute"
            or contents[i] == "minutes"
            or contents[i] == "min"
            or contents[i] == "mins"
        ):
            minutes += int(contents[i - 1])
    return minutes


def extract_time(soup):
    time_tag = soup.find("span", {"class": "mv-time-part"})  # Adjust class if needed
    if time_tag:
        return turn_to_minutes(time_tag.get_text().strip())
    elif soup.find("span", {"class": "wprm-recipe-total_time"}):
        return turn_to_minutes(
            soup.find("span", {"class": "wprm-recipe-total_time"}).get_text().strip()
        )

    return "N/A"


def trim_ingredient(ingr):
    # Remove special characters and convert fractions to decimals
    ingr = ingr.lower()
    ingr = ingr.replace("½", "1/2")
    ingr = ingr.replace("¼", "1/4")
    ingr = ingr.replace("¾", "3/4")
    ingr = ingr.replace("⅓", "1/3")
    ingr = ingr.replace("⅔", "2/3")
    ingr = ingr.replace("⅛", "1/8")
    ingr = ingr.replace("⅜", "3/8")
    ingr = ingr.replace("⅝", "5/8")
    ingr = ingr.replace("⅞", "7/8")

    ingr = ingr.strip()

    punc = string.punctuation.replace("/", "").replace("-", "")

    translator = str.maketrans("", "", punc)
    ingr = ingr.translate(translator)

    return ingr


def parse_ingredient(ingredient):
    # print("parsing ingredient: ", ingredient)
    ingredient = trim_ingredient(ingredient)

    # regex pattern to extract quantity, unit and ingredient from the same string
    pattern = (
        r"""(?P<quantity>
                (?:\d+\s?\d?/\d+|\d+|\d*\.\d+)          
                (?:\s*-\s*(?:\d+\s?\d?/\d+|\d+|\d*\.\d+))?
              )?
              \s?
              (?P<unit>{})?
              \s?
              (?P<ingredient>.+)
           """.format(
            "|".join(units)
        )
        .replace("\n", "")
        .replace(" ", "")
    )

    match = re.match(pattern, ingredient)
    if match:
        dict_match = match.groupdict()
        dict_match = {k: v for k, v in dict_match.items() if v is not None}

        return dict(dict_match)

    return None


def extract_ingredients(soup):
    ingredients_section = soup.find("div", {"class": "mv-create-ingredients"})

    ingredients_list = []

    if ingredients_section:
        ingredients_list = ingredients_section.find_all("li")
        ingredients_list = [
            parse_ingredient(item.get_text()) for item in ingredients_list
        ]
    elif soup.find("ul", {"class": "wprm-recipe-ingredients"}):
        ingredient_names = soup.find_all(
            "span", {"class": "wprm-recipe-ingredient-name"}
        )
        ingredient_amounts = soup.find_all(
            "span", {"class": "wprm-recipe-ingredient-amount"}
        )
        ingredients_units = soup.find_all(
            "span", {"class": "wprm-recipe-ingredient-unit"}
        )

        ingredients_list = [
            {
                "quantity": trim_ingredient(amount.get_text()),
                "unit": trim_ingredient(unit.get_text()),
                "ingredient": trim_ingredient(name.get_text()),
            }
            for amount, unit, name in zip(
                ingredient_amounts, ingredients_units, ingredient_names
            )
        ]

    # print("ingredients_list: ", ingredients_list)

    return ingredients_list


def extract_recipe_data(recipe_url):
    soup = get_soup(recipe_url)
    if soup:
        name = extract_name(soup)
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
    all_ingredient_names = set()
    for url in recipe_urls:
        print("Scraping " + url)
        data = extract_recipe_data(url)
        if data:
            all_recipes.append(data)
            for ingredient in data["ingredients"]:
                all_ingredient_names.add(ingredient["ingredient"])
        time.sleep(2)
    return (all_recipes, all_ingredient_names)


def find_recipe_urls(page_urls):
    recipe_urls = []
    for url in page_urls:
        soup = get_soup(url)
        titles = soup.find_all("h2", {"class": "excerpt-title"})
        for title in titles:
            link = title.find("a", href=True)
            recipe_urls.append(link["href"])
    return scrape_recipes(recipe_urls)


if __name__ == "__main__":
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

    (scraped_data, all_ingredients) = find_recipe_urls(page_urls)

    with open("recipes.json", "w") as f:
        json.dump(scraped_data, f, indent=4)

    with open("ingredients.json", "w") as f:
        json.dump(list(all_ingredients), f, indent=4)

    print("Scraping completed")
