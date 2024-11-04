# CSCE470Project

## Getting Started

To begin, download python3 and create virtual environment
To do this, run the following commands (after python3 installation)
```
python3 -m venv venv
source venv/bin/activate
```

Then, install dependencies

```
pip install -r requirements.txt
```

## Flow of Information:

Start at ```binary_filter.py```, where it will filter recipes by only including desired cultures and exclude any ingredients the user inputs

The output will be in ```filtered_recipes.json```

Next, ```vsm.py``` will rank the filtered recipes from ```filtered_recipes.json``` based on a query of form ```{ingredient: rating, ingredient: rating, ...}``` by using cosine similarity

The output of the vsm will be in ```ranked_recipes.json```