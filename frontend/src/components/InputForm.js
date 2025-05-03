import React, { useState } from 'react';
import './InputForm.css';

const InputForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    age: '',
    sex: '1',
    cp: '0',
    trestbps: '',
    chol: '',
    fbs: '0',
    restecg: '0',
    thalach: '',
    exang: '0',
    oldpeak: '',
    slope: '0',
    ca: '0',
    thal: '0',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const renderInput = (label, id, type, options = null, additionalProps = {}) => (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      {options ? (
        <select id={id} name={id} value={formData[id]} onChange={handleChange} required {...additionalProps}>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          id={id}
          name={id}
          value={formData[id]}
          onChange={handleChange}
          required
          {...additionalProps}
        />
      )}
    </div>
  );

  return (
    <form className="heart-disease-form" onSubmit={handleSubmit}>
      <h2>Heart Disease Risk Assessment</h2>

      {renderInput('Age', 'age', 'number', null, { min: '1', max: '120' })}
      {renderInput('Sex', 'sex', 'select', [
        { value: '1', label: 'Male' },
        { value: '0', label: 'Female' },
      ])}
      {renderInput('Chest Pain Type', 'cp', 'select', [
        { value: '0', label: 'Typical Angina' },
        { value: '1', label: 'Atypical Angina' },
        { value: '2', label: 'Non-anginal Pain' },
        { value: '3', label: 'Asymptomatic' },
      ])}
      {renderInput('Resting Blood Pressure (mm Hg)', 'trestbps', 'number', null, { min: '80', max: '220' })}
      {renderInput('Serum Cholesterol (mg/dl)', 'chol', 'number', null, { min: '100', max: '600' })}
      {renderInput('Fasting Blood Sugar > 120 mg/dl', 'fbs', 'select', [
        { value: '0', label: 'No' },
        { value: '1', label: 'Yes' },
      ])}
      {renderInput('Resting ECG Results', 'restecg', 'select', [
        { value: '0', label: 'Normal' },
        { value: '1', label: 'ST-T Wave Abnormality' },
        { value: '2', label: 'Left Ventricular Hypertrophy' },
      ])}
      {renderInput('Maximum Heart Rate', 'thalach', 'number', null, { min: '60', max: '220' })}
      {renderInput('Exercise Induced Angina', 'exang', 'select', [
        { value: '0', label: 'No' },
        { value: '1', label: 'Yes' },
      ])}
      {renderInput('ST Depression Induced by Exercise', 'oldpeak', 'number', null, {
        step: '0.1',
        min: '0',
        max: '10',
      })}
      {renderInput('Slope of Peak Exercise ST Segment', 'slope', 'select', [
        { value: '0', label: 'Upsloping' },
        { value: '1', label: 'Flat' },
        { value: '2', label: 'Downsloping' },
      ])}
      {renderInput('Number of Major Vessels Colored by Fluoroscopy', 'ca', 'select', [
        { value: '0', label: '0' },
        { value: '1', label: '1' },
        { value: '2', label: '2' },
        { value: '3', label: '3' },
      ])}
      {renderInput('Thalassemia', 'thal', 'select', [
        { value: '0', label: 'Normal' },
        { value: '1', label: 'Fixed Defect' },
        { value: '2', label: 'Reversible Defect' },
      ])}

      <button type="submit" className="submit-btn" disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Predict Risk'}
      </button>
    </form>
  );
};

export default InputForm;