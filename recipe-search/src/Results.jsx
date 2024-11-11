import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const formData = location.state?.formData;

    const handleBackClick = () => {
        navigate('/');
    };

    return (
        <div>
            <h1>Form Data</h1>
            <pre>{JSON.stringify(formData, null, 2)}</pre>
            <button onClick={handleBackClick}>Back to Home</button>
        </div>
    );
}

export default Results;