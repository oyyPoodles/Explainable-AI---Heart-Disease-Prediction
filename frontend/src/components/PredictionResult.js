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
  const riskLevel = probability * 100;
  const isPredictionPositive = prediction === 1;

  return (
    <Card title="Heart Disease Prediction Results" className="mt-4">
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
      
      <div className="my-4">
        <h4>Risk Score</h4>
        <Progress 
          percent={riskLevel.toFixed(1)} 
          status={isPredictionPositive ? "exception" : "success"}
          strokeColor={
            riskLevel > 75 ? "#f5222d" : 
            riskLevel > 50 ? "#fa8c16" : 
            riskLevel > 25 ? "#faad14" : "#52c41a"
          }
        />
        <p className="text-sm text-gray-500">
          Probability of heart disease: {(probability * 100).toFixed(1)}%
        </p>
      </div>

      <Divider>Why this prediction?</Divider>
      
      {explanationData && <ExplanationCharts explanationData={explanationData} />}
      
      <Divider />
      
      <div className="text-sm text-gray-500 mt-4">
        <p><strong>Disclaimer:</strong> This prediction is based on a machine learning model and should not
        replace professional medical advice. Please consult with a healthcare provider for proper diagnosis.</p>
      </div>
    </Card>
  );
};

export default PredictionResult;