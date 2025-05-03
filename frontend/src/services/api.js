import axios from 'axios';

// Use environment variable if available, fallback to localhost
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Create a reusable axios client
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Predict heart disease risk
export const predictHeartDisease = async (patientData) => {
  try {
    const response = await apiClient.post('/predict', patientData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Failed to get prediction');
  }
};

// Get explanation for prediction
export const getExplanation = async (patientData) => {
  try {
    const response = await apiClient.post('/explain', patientData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Failed to get explanation');
  }
};

// Centralized error handling
const handleApiError = (error, defaultMessage) => {
  console.error("API error:", error.response?.data || error.message);
  const errorMessage = error.response?.data?.detail || defaultMessage;
  throw new Error(errorMessage);
};

// Optional: handle global errors with interceptors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log the error or perform global error handling here
    console.error("Global API error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;