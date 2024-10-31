import pytest

from crawler import extract_recipe_data, extract_ingredients
import json


def test_scrape_recipe_f1():
    url = "https://www.curiouscuisiniere.com/roti"

    data = extract_recipe_data(url)

    print(json.dumps(data, indent=4))

    assert 1 == 1


def test_scrape_recipe_f2():
    url = "https://www.curiouscuisiniere.com/homemade-ravioli"

    data = extract_recipe_data(url)

    print(json.dumps(data, indent=4))

    assert 1 == 1
