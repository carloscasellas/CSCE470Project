import pytest
from app.vsm import train, rank, neighborDistance, run, bow

@pytest.fixture(autouse=True)
def clear_bow():
    """Clear the bow list before each test"""
    bow.clear()

def test_train_empty_recipes():
    train([])
    assert len(bow) == 0

def test_train_single_recipe():
    recipe = {
        "url": "test.com",
        "ingredients": [{"ingredient": "salt"}],
        "category": "test"
    }
    train([recipe])
    assert len(bow) == 1
    assert bow[0][0] == "test.com"
    assert bow[0][1] == {"salt": 5}
    assert bow[0][2] == "test"

def test_train_multiple_recipes():
    recipes = [
        {
            "url": "recipe1.com",
            "ingredients": [{"ingredient": "salt"}],
            "category": "cat1"
        },
        {
            "url": "recipe2.com",
            "ingredients": [{"ingredient": "pepper"}],
            "category": "cat2"
        }
    ]
    train(recipes)
    assert len(bow) == 2

def test_neighbor_distance_identical():
    vector1 = {"salt": 5, "pepper": 5}
    vector2 = {"salt": 5, "pepper": 5}
    assert neighborDistance(vector1, vector2) - 1 < 0.0001

def test_neighbor_distance_orthogonal():
    vector1 = {"salt": 5}
    vector2 = {"pepper": 5}
    assert neighborDistance(vector1, vector2) == 0.0

def test_neighbor_distance_partial():
    vector1 = {"salt": 5, "pepper": 5}
    vector2 = {"salt": 5}
    assert 0 < neighborDistance(vector1, vector2) < 1

def test_rank_empty_query():
    recipe = {
        "url": "test.com",
        "ingredients": [{"ingredient": "salt"}],
        "category": "test"
    }
    train([recipe])
    result = rank({})
    assert len(result) == 1
    assert result[0][0] == 0  # Distance will be 0 for empty query

def test_rank_matching_query():
    recipe = {
        "url": "test.com",
        "ingredients": [{"ingredient": "salt"}],
        "category": "test"
    }
    train([recipe])
    result = rank({"salt": 5})
    assert len(result) == 1
    assert result[0][0] == -1  # Perfect match should have distance of -1

def test_run_integration():
    recipes = [{
        "url": "recipe1.com",
        "ingredients": [{"ingredient": "salt"}],
        "category": "test"
    }]
    query = {"salt": 5}
    result = run(recipes, query)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert "url" in result[0]
    assert "score" in result[0]
    assert "category" in result[0]
    assert result[0]["url"] == "recipe1.com"
    assert result[0]["score"] == 1.0
    assert result[0]["category"] == "test"

def test_run_empty():
    result = run([], {})
    assert isinstance(result, list)
    assert len(result) == 0