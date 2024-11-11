import React, { useState, useEffect } from 'react';
import './IngredientsForm.css'; // Import the CSS file

function IngredientsForm({ ingredientsList = [], onChange }) {
    const [fields, setFields] = useState([{ value: "", rank: 1 }]);

    useEffect(() => {
        onChange(fields.map(field => ({ value: field.value, rank: field.rank })));
    }, [fields, onChange]);

    const handleAddField = () => {
        setFields([...fields, { value: "", rank: 1 }]);
    };

    const handleFieldChange = (index, event) => {
        const newFields = fields.slice();
        newFields[index].value = event.target.value;
        setFields(newFields);
    };

    const handleRankChange = (index, event) => {
        const newFields = fields.slice();
        newFields[index].rank = event.target.value;
        setFields(newFields);
    };

    const handleRemoveField = (index) => {
        const newFields = fields.slice();
        newFields.splice(index, 1);
        setFields(newFields);
    };

    const selectedValues = fields.map(field => field.value);

    const isAddButtonDisabled = fields[fields.length - 1].value === "" || fields.some(field => field.value === "");

    return (
        <div>
            <h2>Ingredients</h2>
            {fields.map((field, index) => (
                <div key={index} className="field-container">
                    <input
                        type="text"
                        value={field.value}
                        onChange={(e) => handleFieldChange(index, e)}
                        list={`ingredients-list-${index}`}
                        placeholder="Type an ingredient"
                        className="styled-input"
                    />
                    <datalist id={`ingredients-list-${index}`}>
                        {ingredientsList
                            .filter(value => !selectedValues.includes(value))
                            .map((value, i) => (
                                <option key={i} value={value} />
                            ))}
                    </datalist>
                    <select className="styled-select" value={field.rank} onChange={(e) => handleRankChange(index, e)}>
                        {[1, 2, 3, 4, 5].map(rank => (
                            <option key={rank} value={rank}>{rank}</option>
                        ))}
                    </select>
                    <button type="button" onClick={() => handleRemoveField(index)}>Remove</button>
                </div>
            ))}
            <button type="button" onClick={handleAddField} disabled={isAddButtonDisabled}>Add Ingredient</button>
        </div>
    );
}

export default IngredientsForm;