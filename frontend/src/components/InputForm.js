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
    thal: '0'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="heart-disease-form" onSubmit={handleSubmit}>
      <h2>Heart Disease Risk Assessment</h2>
      
      <div className="form-group">
        <label htmlFor="age">Age</label>
        <input
          type="number"
          id="age"
          name="age"
          value={formData.age}
          onChange={handleChange}
          required
          min="1"
          max="120"
        />
      </div>

      <div className="form-group">
        <label htmlFor="sex">Sex</label>
        <select
          id="sex"
          name="sex"
          value={formData.sex}
          onChange={handleChange}
          required
        >
          <option value="1">Male</option>
          <option value="0">Female</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="cp">Chest Pain Type</label>
        <select
          id="cp"
          name="cp"
          value={formData.cp}
          onChange={handleChange}
          required
        >
          <option value="0">Typical Angina</option>
          <option value="1">Atypical Angina</option>
          <option value="2">Non-anginal Pain</option>
          <option value="3">Asymptomatic</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="trestbps">Resting Blood Pressure (mm Hg)</label>
        <input
          type="number"
          id="trestbps"
          name="trestbps"
          value={formData.trestbps}
          onChange={handleChange}
          required
          min="80"
          max="220"
        />
      </div>

      <div className="form-group">
        <label htmlFor="chol">Serum Cholesterol (mg/dl)</label>
        <input
          type="number"
          id="chol"
          name="chol"
          value={formData.chol}
          onChange={handleChange}
          required
          min="100"
          max="600"
        />
      </div>

      <div className="form-group">
        <label htmlFor="fbs">Fasting Blood Sugar > 120 mg/dl</label>
        <select
          id="fbs"
          name="fbs"
          value={formData.fbs}
          onChange={handleChange}
          required
        >
          <option value="0">No</option>
          <option value="1">Yes</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="restecg">Resting ECG Results</label>
        <select
          id="restecg"
          name="restecg"
          value={formData.restecg}
          onChange={handleChange}
          required
        >
          <option value="0">Normal</option>
          <option value="1">ST-T Wave Abnormality</option>
          <option value="2">Left Ventricular Hypertrophy</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="thalach">Maximum Heart Rate</label>
        <input
          type="number"
          id="thalach"
          name="thalach"
          value={formData.thalach}
          onChange={handleChange}
          required
          min="60"
          max="220"
        />
      </div>

      <div className="form-group">
        <label htmlFor="exang">Exercise Induced Angina</label>
        <select
          id="exang"
          name="exang"
          value={formData.exang}
          onChange={handleChange}
          required
        >
          <option value="0">No</option>
          <option value="1">Yes</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="oldpeak">ST Depression Induced by Exercise</label>
        <input
          type="number"
          id="oldpeak"
          name="oldpeak"
          step="0.1"
          value={formData.oldpeak}
          onChange={handleChange}
          required
          min="0"
          max="10"
        />
      </div>

      <div className="form-group">
        <label htmlFor="slope">Slope of Peak Exercise ST Segment</label>
        <select
          id="slope"
          name="slope"
          value={formData.slope}
          onChange={handleChange}
          required
        >
          <option value="0">Upsloping</option>
          <option value="1">Flat</option>
          <option value="2">Downsloping</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="ca">Number of Major Vessels Colored by Fluoroscopy</label>
        <select
          id="ca"
          name="ca"
          value={formData.ca}
          onChange={handleChange}
          required
        >
          <option value="0">0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="thal">Thalassemia</label>
        <select
          id="thal"
          name="thal"
          value={formData.thal}
          onChange={handleChange}
          required
        >
          <option value="0">Normal</option>
          <option value="1">Fixed Defect</option>
          <option value="2">Reversible Defect</option>
        </select>
      </div>

      <button type="submit" className="submit-btn" disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Predict Risk'}
      </button>
    </form>
  );
};

export default InputForm;