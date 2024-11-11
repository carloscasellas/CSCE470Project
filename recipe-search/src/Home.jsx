import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import IngredientsForm from './IngredientsForm';
import CulturalForm from './CulturalForm';
import ExcludeIngredientsForm from './ExcludeIngredientsForm';

const availableIngredients = require('./availableIngredients.json');
const availableCultures = require('./availableCultures.json');

function Home() {
    const [ingredients, setIngredients] = useState([]);
    const [cultures, setCultures] = useState([]);
    const [excludedIngredients, setExcludedIngredients] = useState([]);
    const navigate = useNavigate();

    const handleIngredientsChange = (newIngredients) => {
        setIngredients(newIngredients);
    };

    const handleCulturesChange = (newCultures) => {
        setCultures(newCultures);
    };

    const handleExcludedIngredientsChange = (newExcludedIngredients) => {
        setExcludedIngredients(newExcludedIngredients);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = {
            ingredients: ingredients.filter(ingredient => ingredient.value.trim() !== ""),
            cultures: cultures.filter(culture => culture.trim() !== ""),
            excludedIngredients: excludedIngredients.filter(ingredient => ingredient.trim() !== "")
        };
        navigate('/results', { state: { formData } });
    };

    return (
        <div>
            <h1>Recipe Search</h1>
            <form onSubmit={handleSubmit}>
                <IngredientsForm ingredientsList={availableIngredients} onChange={handleIngredientsChange} />
                <CulturalForm culturesList={availableCultures} onChange={handleCulturesChange} />
                <ExcludeIngredientsForm ingredientsList={availableIngredients} onChange={handleExcludedIngredientsChange} />
                <button type="submit">Submit All Forms</button>
            </form>
        </div>
    );
}

export default Home;