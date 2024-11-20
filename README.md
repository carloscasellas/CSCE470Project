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

## Setting Up the Frontend

Download and install Node.js from [nodejs.org](https://nodejs.org/).

From here, run ```cd recipe-search npm install``` on the ```CSCE470Project``` directory


## Flow of Information:

Start at ```binary_filter.py```, where it will filter recipes by only including desired cultures and exclude any ingredients the user inputs

The output will be in ```filtered_recipes.json```

Next, ```vsm.py``` will rank the filtered recipes from ```filtered_recipes.json``` based on a query of form ```{ingredient: rating, ingredient: rating, ...}``` by using cosine similarity

The output of the vsm will be in ```ranked_recipes.json```

## How to Customize Query
The main components are the ```exclude_ingredient_list``` and ```cuisine_list``` in ```binary_filter.py``` and the ```query``` in ```vsm.py```. These can be modified, but it may not give good results as we will limit what selections will work when designing the UI.

## How to Run All Files

Make sure you are in the ```recipe-search``` directory. Then, to run the frontend, do ```npm start```. To run the backend scripts, do ```src/backend/<script>.py```, where script can be ```crawler, binary_filter, vsm```