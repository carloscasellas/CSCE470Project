const fs = require('fs');

// Read the recipes.json file
const recipes = JSON.parse(fs.readFileSync('backend/recipes.json', 'utf8'));

const uniqueIngredients = new Set();
const uniqueCategories = new Set();

// Function to capitalize the first letter of every word
const capitalizeWords = (str) => {
    return str.replace(/\b\w/g, char => char.toUpperCase());
};

recipes.forEach(recipe => {
    recipe.ingredients.forEach(ingredient => {
        const ingredientName = ingredient.ingredient.trim();
        if (ingredientName.split(' ').length <= 2) {
            uniqueIngredients.add(ingredientName);
        }
    });

    const capitalizedCategory = capitalizeWords(recipe.category.trim());
    uniqueCategories.add(capitalizedCategory);
});

const availableIngredients = Array.from(uniqueIngredients);
const availableCultures = Array.from(uniqueCategories);

console.log('Available Ingredients:', availableIngredients);
console.log('Available Cultures:', availableCultures);

// Write the lists to JSON files
fs.writeFileSync('availableIngredients.json', JSON.stringify(availableIngredients, null, 2));
fs.writeFileSync('availableCultures.json', JSON.stringify(availableCultures, null, 2));