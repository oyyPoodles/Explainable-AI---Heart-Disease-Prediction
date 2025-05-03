import React from 'react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                {/* About Section */}
                <div className="footer-section">
                    <h3>Heart Disease XAI Chatbot</h3>
                    <p>
                        An explainable AI application for heart disease prediction.
                        This project demonstrates the use of machine learning with
                        transparent, explainable predictions.
                    </p>
                </div>

                {/* References Section */}
                <div className="footer-section">
                    <h3>References</h3>
                    <ul>
                        <li>
                            <a
                                href="https://www.heart.org/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="footer-link"
                            >
                                American Heart Association
                            </a>
                        </li>
                        <li>
                            <a
                                href="https://www.who.int/health-topics/cardiovascular-diseases"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="footer-link"
                            >
                                WHO - Cardiovascular Diseases
                            </a>
                        </li>
                    </ul>
                </div>

                {/* Disclaimer Section */}
                <div className="footer-section">
                    <h3>Disclaimer</h3>
                    <p>
                        This application is for educational purposes only.
                        It should not be used for medical diagnosis or treatment.
                        Always consult with healthcare professionals.
                    </p>
                </div>
            </div>

            {/* Footer Bottom Section */}
            <div className="footer-bottom">
                <p>&copy; {new Date().getFullYear()} Heart Disease XAI Project. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;