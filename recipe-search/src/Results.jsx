import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import rankedRecipes from './backend/ranked_recipes.json'; // Import the JSON file

function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const formData = location.state?.formData;

    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        // Read the ranked recipes from the JSON file
        setRecipes(rankedRecipes);
    }, []);

    const handleBackClick = () => {
        navigate('/');
    };

    const getLinkName = (url) => {
        const parts = url.split('/');
        const name = parts[parts.length - 2].replace(/-/g, ' ');
        return name.replace(/\b\w/g, char => char.toUpperCase());
    };

    return (
        <div>
            <h2>Ranked Recipes</h2>
            <ul>
                {recipes.map((recipe, index) => (
                    <li key={index}>
                        <a href={recipe.url} target="_blank" rel="noopener noreferrer">
                            {getLinkName(recipe.url)}
                        </a>
                    </li>
                ))}
            </ul>
            <button onClick={handleBackClick}>Back to Home</button>
        </div>
    );
}

export default Results;