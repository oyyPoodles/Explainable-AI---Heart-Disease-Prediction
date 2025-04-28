import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const predictHeartDisease = async (patientData) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, patientData);
    return response.data;
  } catch (error) {
    console.error("Error predicting heart disease:", error);
    throw error;
  }
};

export const getExplanation = async (patientData) => {
  try {
    const response = await axios.post(`${API_URL}/explain`, patientData);
    return response.data;
  } catch (error) {
    console.error("Error getting explanation:", error);
    throw error;
  }
};