import React from 'react';
import './About.css';

const About = () => {
    return (
        <div className="about-container">
            {/* Header Section */}
            <section className="about-header">
                <h1>About This Project</h1>
                <p>
                    Understanding the technology behind heart disease prediction
                    and the importance of explainable AI in healthcare.
                </p>
            </section>

            {/* Heart Disease Challenge Section */}
            <section className="about-section">
                <h2>The Heart Disease Challenge</h2>
                <p>
                    Heart disease remains one of the leading causes of death globally.
                    Early detection and risk assessment can significantly improve outcomes
                    by enabling preventive measures and timely interventions.
                </p>
                <p>
                    Traditional risk assessment methods rely on established medical guidelines,
                    but machine learning models can potentially identify subtle patterns and
                    personalized risk factors that might be missed by conventional approaches.
                </p>
            </section>

            {/* Explainable AI Section */}
            <section className="about-section">
                <h2>Our Approach: Explainable AI</h2>
                <p>
                    Many AI systems operate as "black boxes," providing predictions without
                    explaining the reasoning behind them. This lack of transparency is problematic
                    in healthcare, where understanding the "why" behind a diagnosis or risk
                    assessment is crucial for both healthcare providers and patients.
                </p>
                <p>
                    Our application uses Explainable AI (XAI) techniques, particularly:
                </p>
                <ul>
                    <li>
                        <strong>SHAP (SHapley Additive exPlanations)</strong> - A game-theoretic approach
                        to explain the output of any machine learning model by calculating the contribution
                        of each feature to the prediction.
                    </li>
                    <li>
                        <strong>LIME (Local Interpretable Model-agnostic Explanations)</strong> - A technique
                        that explains predictions by approximating the model locally with an interpretable model.
                    </li>
                </ul>
                <p>
                    These methods help demystify AI predictions by showing how different health metrics
                    contribute to your heart disease risk assessment.
                </p>
            </section>

            {/* Dataset Section */}
            <section className="about-section">
                <h2>The Dataset</h2>
                <p>
                    Our model is trained on the UCI Heart Disease dataset, which includes various
                    clinical parameters such as:
                </p>
                <ul>
                    <li>Age and sex</li>
                    <li>Chest pain type</li>
                    <li>Resting blood pressure</li>
                    <li>Serum cholesterol levels</li>
                    <li>Fasting blood sugar</li>
                    <li>Resting electrocardiographic results</li>
                    <li>Maximum heart rate achieved</li>
                    <li>Exercise-induced angina</li>
                    <li>ST depression induced by exercise</li>
                    <li>Number of major vessels colored by fluoroscopy</li>
                    <li>Thalassemia status</li>
                </ul>
                <p>
                    The dataset was collected from real patients and has been widely used
                    in medical research and machine learning applications.
                </p>
            </section>

            {/* Technology Stack Section */}
            <section className="about-section">
                <h2>Technology Stack</h2>
                <p>This application is built using modern web and data science technologies:</p>
                <ul>
                    <li><strong>Frontend:</strong> React.js, JavaScript, HTML/CSS</li>
                    <li><strong>Backend:</strong> FastAPI, Python</li>
                    <li><strong>Machine Learning:</strong> Scikit-learn, XGBoost</li>
                    <li><strong>Explainable AI:</strong> SHAP, LIME</li>
                    <li><strong>Data Processing:</strong> Pandas, NumPy</li>
                    <li><strong>Visualization:</strong> D3.js, Recharts</li>
                </ul>
            </section>

            {/* Disclaimer Section */}
            <section className="about-section disclaimer">
                <h2>Important Disclaimer</h2>
                <p>
                    This application is provided for educational and research purposes only.
                    It is not intended to be a substitute for professional medical advice,
                    diagnosis, or treatment. The predictions and explanations provided by
                    this tool should never replace consultation with qualified healthcare
                    professionals.
                </p>
                <p>
                    Always seek the advice of your physician or other qualified health provider
                    with any questions you may have regarding a medical condition or health objectives.
                </p>
            </section>
        </div>
    );
};

export default About;