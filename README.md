# CSCE470Project

## Getting Started

This web app requires some setup (initial data collection) to work.

To begin, make sure Python is installed and create a virtual environment.
To do this, run the following commands
```
cd recipe-search/src/backend
python3 -m venv venv
source venv/bin/activate
```

Then, install dependencies

```
pip install -r requirements.txt
```

Now getting to actual data gathering, there's a script which does this for a predetermined corpus of web data
(which takes around 30 minutes to complete, and saves the data to a JSON file, which the app then accesses when running).
Run the crawler by simply:
```
python3 crawler.py
```

### Setting Up the Frontend

Download and install Node.js from [nodejs.org](https://nodejs.org/).

From here, run ```cd recipe-search npm install``` on the ```CSCE470Project``` directory

### Running the app

Now finally, to run the app (from the `recipe-search` directory):
```
npm start
```

<br/>

## Flow of Information (running backend algorithm manually):

Start at ```binary_filter.py```, where it will filter recipes by only including desired cultures and exclude any ingredients the user inputs

The output will be in ```filtered_recipes.json```

Next, ```vsm.py``` will rank the filtered recipes from ```filtered_recipes.json``` based on a query of form ```{ingredient: rating, ingredient: rating, ...}``` by using cosine similarity

The output of the vsm will be in ```ranked_recipes.json```

### How to Customize Query
The main components are the ```exclude_ingredient_list``` and ```cuisine_list``` in ```binary_filter.py``` and the ```query``` in ```vsm.py```. These can be modified, but it may not give good results as we will limit what selections will work when designing the UI.
