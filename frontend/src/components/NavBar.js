import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
    const location = useLocation();
    
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <h1>Heart Disease AI</h1>
            </div>
            <div className="navbar-links">
                <Link 
                    to="/" 
                    className={location.pathname === '/' ? 'active' : ''}
                >
                    Home
                </Link>
                <Link 
                    to="/predict" 
                    className={location.pathname === '/predict' ? 'active' : ''}
                >
                    Predict
                </Link>
                <Link 
                    to="/about" 
                    className={location.pathname === '/about' ? 'active' : ''}
                >
                    About
                </Link>
            </div>
        </nav>
    );
};

export default NavBar;