import React, { useState } from 'react';
import InputForm from '../components/InputForm';
import PredictionResult from '../components/PredictionResult';
import ExplanationCharts from '../components/ExplanationCharts';
import { predictHeartDisease, getExplanation } from '../services/api';
import './Predict.css';

const Predict = () => {
    const [prediction, setPrediction] = useState(null);
    const [explanation, setExplanation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [patientData, setPatientData] = useState(null);

    const handleSubmit = async (formData) => {
        setIsLoading(true);
        setError(null);
        setPatientData(formData);

        try {
            // Get prediction
            const predictionResult = await predictHeartDisease(formData);
            setPrediction(predictionResult);

            // Get explanation
            const explanationResult = await getExplanation(formData);
            setExplanation(explanationResult);
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'An error occurred during prediction.');
            setPrediction(null);
            setExplanation(null);
        } finally {
            setIsLoading(false);
        }
    };

    const resetForm = () => {
        setPrediction(null);
        setExplanation(null);
        setPatientData(null);
        setError(null);
    };

    return (
        <div className="predict-container">
            <h1 className="predict-title">Heart Disease Risk Assessment</h1>

            {error && (
                <div className="error-message">
                    <p>{error}</p>
                    <button onClick={resetForm} className="btn secondary-btn">
                        Try Again
                    </button>
                </div>
            )}

            {!prediction ? (
                <div className="form-section">
                    <p className="intro-text">
                        Enter your health information below to get a heart disease risk assessment.
                        All fields are required for an accurate prediction.
                    </p>
                    <InputForm onSubmit={handleSubmit} isLoading={isLoading} />
                </div>
            ) : (
                <div className="results-section">
                    <div className="results-header">
                        <h2>Your Results</h2>
                        <button onClick={resetForm} className="btn secondary-btn">
                            Start Over
                        </button>
                    </div>

                    <PredictionResult prediction={prediction} patientData={patientData} />

                    {explanation && (
                        <div className="explanation-section">
                            <h3>Understanding Your Prediction</h3>
                            <p className="explanation-intro">
                                Below are visualizations that explain which factors influenced your risk assessment.
                                Factors pushing your risk higher are shown in red, while protective factors are shown in green.
                            </p>
                            <ExplanationCharts explanation={explanation} patientData={patientData} />
                        </div>
                    )}

                    <div className="disclaimer-box">
                        <h4>Medical Disclaimer</h4>
                        <p>
                            This prediction is for educational purposes only and should not be used for
                            medical diagnosis. Always consult healthcare professionals for medical advice.
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Predict;