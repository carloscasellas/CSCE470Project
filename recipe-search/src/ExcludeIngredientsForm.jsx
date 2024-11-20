import React, { useState, useEffect } from 'react';
import './stylesheets/ExcludeIngredientsForm.css'; // Import the CSS file

function ExcludeIngredientsForm({ ingredientsList = [], onChange }) {
    const [fields, setFields] = useState([{ value: "" }]);

    useEffect(() => {
        onChange(fields.map(field => field.value));
    }, [fields, onChange]);

    const handleAddField = () => {
        setFields([...fields, { value: "" }]);
    };

    const handleFieldChange = (index, event) => {
        const newFields = fields.slice();
        newFields[index].value = event.target.value;
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
        <div style={{width: "100%", display: "flex", flexDirection: "column", alignItems: "center"}}>
            <h2>Exclude Ingredients</h2>
            {fields.map((field, index) => (
                <div style={{display: "inline"}} key={index} className="field-container">
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
                    <button type="button" onClick={() => handleRemoveField(index)}>Remove</button>
                </div>
            ))}
            <button type="button" onClick={handleAddField} disabled={isAddButtonDisabled}>Add Ingredient</button>
        </div>
    );
}

export default ExcludeIngredientsForm;