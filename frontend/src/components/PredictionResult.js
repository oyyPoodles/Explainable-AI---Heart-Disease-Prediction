import React from 'react';
import { Card, Alert, Progress, Divider } from 'antd';
import ExplanationCharts from './ExplanationCharts';

const PredictionResult = ({ predictionData, explanationData, loading }) => {
  if (loading) {
    return <Card loading={true}></Card>;
  }

  if (!predictionData) {
    return null;
  }

  const { prediction, probability } = predictionData;
  const riskLevel = (probability * 100).toFixed(1);
  const isPredictionPositive = prediction === 1;

  const getRiskColor = (risk) => {
    if (risk > 75) return "#f5222d"; // High risk (red)
    if (risk > 50) return "#fa8c16"; // Moderate risk (orange)
    if (risk > 25) return "#faad14"; // Low risk (yellow)
    return "#52c41a"; // Minimal risk (green)
  };

  return (
    <Card title="Heart Disease Prediction Results" className="mt-4">
      {/* Alert Section */}
      <Alert
        message={isPredictionPositive ? "Heart Disease Risk Detected" : "Low Heart Disease Risk"}
        description={
          isPredictionPositive
            ? "Our model has detected potential heart disease risk factors that require attention."
            : "Based on the provided information, you appear to have a lower risk of heart disease."
        }
        type={isPredictionPositive ? "warning" : "success"}
        showIcon
      />

      {/* Risk Score Section */}
      <div className="my-4">
        <h4>Risk Score</h4>
        <Progress
          percent={riskLevel}
          status={isPredictionPositive ? "exception" : "success"}
          strokeColor={getRiskColor(riskLevel)}
        />
        <p className="text-sm text-gray-500">
          Probability of heart disease: {riskLevel}%
        </p>
      </div>

      {/* Explanation Section */}
      <Divider>Why this prediction?</Divider>
      {explanationData ? (
        <ExplanationCharts explanationData={explanationData} />
      ) : (
        <p className="text-sm text-gray-500">
          No explanation data available for this prediction.
        </p>
      )}

      {/* Disclaimer Section */}
      <Divider />
      <div className="text-sm text-gray-500 mt-4">
        <p>
          <strong>Disclaimer:</strong> This prediction is based on a machine learning model and should not
          replace professional medical advice. Please consult with a healthcare provider for proper diagnosis.
        </p>
      </div>
    </Card>
  );
};

export default PredictionResult;