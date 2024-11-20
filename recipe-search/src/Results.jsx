import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import rankedRecipes from './backend/ranked_recipes.json'; // Import the JSON file
import './stylesheets/Results.css';

function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const formData = location.state?.formData;

    const [recipes, setRecipes] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 9;

    useEffect(() => {
        fetch('http://localhost:5000/recipes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then(response => {
          if (response.status == 400) {
            // must specify ingredient and cuisine
            navigate('/');
            alert("Please specify an ingredient and a cuisine.");
          }

          return response.json();
        })
        .then(data => {
            setRecipes(data);
        });
    }, []);

    const handleBackClick = () => {
        navigate('/');
    };

    const getLinkName = (url) => {
        const parts = url.split('/');
        const name = parts[parts.length - 2].replace(/-/g, ' ');
        return name.replace(/\b\w/g, char => char.toUpperCase());
    };

    const capitalizeWords = (str) => {
        return str.replace(/\b\w/g, char => char.toUpperCase());
    };

    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    // Calculate the items to display based on the current page
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = recipes.slice(indexOfFirstItem, indexOfLastItem);

    // Calculate total pages
    const totalPages = Math.ceil(recipes.length / itemsPerPage);

    return (
        <div>
            <h2>Ranked Recipes</h2>
            <ul>
                {currentItems.map((recipe, index) => (
                    <li key={index}>
                        <a href={recipe.url} target="_blank" rel="noopener noreferrer">
                            {getLinkName(recipe.url)}
                        </a>
                        <p>Culture: {capitalizeWords(recipe.category)}</p>
                    </li>
                ))}
            </ul>
            <div style={{display: "inline", marginBottom: "16px"}}>
                {Array.from({ length: totalPages }, (_, index) => (
                    <button style={{margin:"0 2px"}}
                        key={index}
                        onClick={() => handlePageChange(index + 1)}
                        disabled={currentPage === index + 1}
                    >
                        {index + 1}
                    </button>
                ))}
            </div>
            <button onClick={handleBackClick}>Back to Home</button>
        </div>
    );
}

export default Results;
