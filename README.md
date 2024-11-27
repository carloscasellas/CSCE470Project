# CSCE470Project

## Getting Started

### Using Docker

To set up and run the application using Docker, follow these steps:

1. **Install Docker and Docker Compose**:

    - **macOS and Linux**:
        ```bash
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        docker compose version
        ```

    - **Windows**:
        Download and install Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. **Build and start the containers**:

    ```bash
    docker compose up --build
    ```

3. **Access the application**:

    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend: [http://localhost:5000](http://localhost:5000)

### Using Virtual Environment

To set up the application using a virtual environment, follow these steps:

1. **Navigate to the backend directory**:

    ```bash
    cd recipe-search/src/backend
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the backend server**:

    ```bash
    python3 run_app.py
    ```

### Setting Up the Frontend

To set up the frontend, follow these steps:

1. **Download and install Node.js** from [nodejs.org](https://nodejs.org/).

2. **Navigate to the frontend directory and install dependencies**:

    ```bash
    cd recipe-search
    npm install
    ```

3. **Run the frontend server**:

    ```bash
    npm start
    ```

## Data Collection

This web app requires some initial data collection to work. There's a script that does this for a predetermined corpus of web data (which takes around 30 minutes to complete) and saves the data to a JSON file, which the app then accesses when running.

1. **Run the crawler**:

    ```bash
    python3 crawler.py
    ```

## Flow of Information

1. **Filter Recipes**: Start at `binary_filter.py`, where it will filter recipes by only including desired cultures and exclude any ingredients the user inputs. The output will be in `filtered_recipes.json`.

2. **Rank Recipes**: Next, `vsm.py` will rank the filtered recipes from `filtered_recipes.json` based on a query of form `{ingredient: rating, ingredient: rating, ...}` by using cosine similarity. The output of the VSM will be in `ranked_recipes.json`.

## How to Customize Query

The main components are the `exclude_ingredient_list` and `cuisine_list` in `binary_filter.py` and the `query` in `vsm.py`. These can be modified, but it may not give good results as we will limit what selections will work when designing the UI.

## How to Run All Files

Make sure you are in the `recipe-search` directory. Then, to run the frontend, do:

```bash
npm start
