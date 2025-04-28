import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
    return (
        <div className="home-container">
            <section className="hero">
                <div className="hero-content">
                    <h1>Heart Disease Prediction with Explainable AI</h1>
                    <p>
                        Using advanced machine learning algorithms with transparent
                        explanations to help understand heart disease risk factors.
                    </p>
                    <div className="hero-buttons">
                        <Link to="/predict" className="btn primary-btn">
                            Try Prediction
                        </Link>
                        <Link to="/about" className="btn secondary-btn">
                            Learn More
                        </Link>
                    </div>
                </div>
            </section>

            <section className="features">
                <div className="feature-card">
                    <div className="feature-icon">❤️</div>
                    <h3>Accurate Predictions</h3>
                    <p>Our model is trained on established medical datasets to provide reliable risk assessments.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">🔍</div>
                    <h3>Transparent Results</h3>
                    <p>Unlike black-box AI, our system explains which factors contribute to your risk prediction.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">📊</div>
                    <h3>Visual Insights</h3>
                    <p>Interactive visualizations help you understand how different factors affect heart health.</p>
                </div>
            </section>

            <section className="how-it-works">
                <h2>How It Works</h2>
                <div className="steps">
                    <div className="step">
                        <div className="step-number">1</div>
                        <h3>Enter Your Health Data</h3>
                        <p>Provide basic health metrics like age, blood pressure, cholesterol levels, and lifestyle factors.</p>
                    </div>
                    <div className="step">
                        <div className="step-number">2</div>
                        <h3>Get Your Prediction</h3>
                        <p>Our AI model analyzes your data to assess heart disease risk.</p>
                    </div>
                    <div className="step">
                        <div className="step-number">3</div>
                        <h3>Understand Your Results</h3>
                        <p>Review detailed explanations about which factors influenced your prediction.</p>
                    </div>
                </div>
                <div className="cta-container">
                    <Link to="/predict" className="btn primary-btn">
                        Get Started Now
                    </Link>
                </div>
            </section>

            <section className="disclaimer">
                <h2>Medical Disclaimer</h2>
                <p>
                    This tool is for educational purposes only and is not intended to be a substitute
                    for professional medical advice, diagnosis, or treatment. Always seek the advice
                    of your physician or other qualified health provider with any questions you may
                    have regarding a medical condition.
                </p>
            </section>
        </div>
    );
};

export default Home;Ho