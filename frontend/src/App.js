// filepath: c:\Users\DELL\Desktop\heart-xai-chatbot\frontend\src\App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom'; // Remove BrowserRouter here
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Predict from './pages/Predict';
import About from './pages/About';
import './App.css';

function App() {
  return (
    <div className="app">
      {/* Navigation Bar */}
      <NavBar />

      {/* Main Content */}
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;