// filepath: c:\Users\DELL\Desktop\heart-xai-chatbot\frontend\src\index.js
import React from 'react';
import ReactDOM from 'react-dom/client'; // Use React 18's createRoot API
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);