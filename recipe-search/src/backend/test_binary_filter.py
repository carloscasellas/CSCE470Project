import pytest
from app.binary_filter import run

@pytest.fixture
def sample_recipes():
    return [
        {
            "title": "Mexican Tacos",
            "category": "mexican",
            "ingredients": [
                {"ingredient": "tortilla", "amount": "2"},
                {"ingredient": "beef", "amount": "200g"}
            ]
        },
        {
            "title": "Moroccan Tagine",
            "category": "moroccan",
            "ingredients": [
                {"ingredient": "chicken", "amount": "500g"},
                {"ingredient": "couscous", "amount": "200g"}
            ]
        },
        {
            "title": "Pasta",
            "category": "italian",
            "ingredients": [
                {"ingredient": "pasta", "amount": "200g"},
                {"ingredient": "tomato", "amount": "3"}
            ]
        }
    ]

def test_run_empty_filters(sample_recipes):
    result = run(sample_recipes, [], [])
    assert len(result) == 0

def test_run_single_cuisine(sample_recipes):
    result = run(sample_recipes, [], ["mexican"])
    assert len(result) == 1
    assert result[0]["title"] == "Mexican Tacos"

def test_run_multiple_cuisines(sample_recipes):
    result = run(sample_recipes, [], ["mexican", "moroccan"])
    assert len(result) == 2

def test_run_with_excluded_ingredient(sample_recipes):
    result = run(sample_recipes, ["chicken"], ["moroccan"])
    assert len(result) == 0

def test_run_case_insensitive_cuisine(sample_recipes):
    result = run(sample_recipes, [], ["MEXICAN"])
    assert len(result) == 1
    assert result[0]["title"] == "Mexican Tacos"

def test_run_combined_filters(sample_recipes):
    result = run(sample_recipes, ["beef"], ["mexican", "moroccan"])
    assert len(result) == 1
    assert result[0]["title"] == "Moroccan Tagine"