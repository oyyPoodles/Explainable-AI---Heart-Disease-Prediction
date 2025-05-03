import React from 'react';
import { Card, Tabs, Empty } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const { TabPane } = Tabs;

const ExplanationCharts = ({ explanationData }) => {
  if (!explanationData) {
    return <Empty description="No explanation data available" />;
  }

  const { shap_values, feature_importance, lime_explanation } = explanationData;

  // Helper function to transform data for visualization
  const transformData = (data, key, valueKey, additionalFields = {}) =>
    Object.entries(data).map(([feature, value]) => ({
      feature,
      [valueKey]: value,
      ...additionalFields,
    }));

  // Transform SHAP values for visualization
  const shapData = transformData(shap_values, 'feature', 'value', {
    impact: (value) => Math.abs(value),
    direction: (value) => (value >= 0 ? 'Increases Risk' : 'Decreases Risk'),
  }).sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

  // Transform feature importance values
  const importanceData = transformData(feature_importance, 'feature', 'importance').sort(
    (a, b) => b.importance - a.importance
  );

  // Render a bar chart
  const renderBarChart = (data, dataKey, fillColor, tooltipFormatter, yAxisKey = 'feature') => (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 150, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" />
        <YAxis type="category" dataKey={yAxisKey} />
        <Tooltip formatter={tooltipFormatter} />
        <Legend />
        <Bar dataKey={dataKey} fill={fillColor} />
      </BarChart>
    </ResponsiveContainer>
  );

  return (
    <Card className="mt-4">
      <Tabs defaultActiveKey="1">
        <TabPane tab="SHAP Values" key="1">
          <div className="my-4">
            <p>SHAP values show how each feature contributed to this specific prediction:</p>
            {renderBarChart(
              shapData,
              'value',
              (entry) => (entry.value >= 0 ? '#ff4d4f' : '#52c41a'),
              (value, name, props) => [`Impact: ${Math.abs(value).toFixed(4)}`, props.payload.direction]
            )}
            <ul className="mt-4 text-sm">
              <li>
                <span className="text-red-500">■</span> Red bars show features that increased the risk
              </li>
              <li>
                <span className="text-green-500">■</span> Green bars show features that decreased the risk
              </li>
            </ul>
          </div>
        </TabPane>

        <TabPane tab="Feature Importance" key="2">
          <div className="my-4">
            <p>Feature importance shows which factors generally matter most in heart disease prediction:</p>
            {renderBarChart(importanceData, 'importance', '#1890ff', (value) => [`Importance: ${value.toFixed(4)}`])}
          </div>
        </TabPane>

        <TabPane tab="LIME Explanation" key="3">
          <div className="my-4">
            <p>LIME explains the model by perturbing the input and observing changes:</p>
            {renderBarChart(
              lime_explanation,
              'weight',
              (entry) => (entry.weight >= 0 ? '#ff4d4f' : '#52c41a'),
              (value) => [`Weight: ${value.toFixed(4)}`]
            )}
          </div>
        </TabPane>
      </Tabs>
    </Card>
  );
};

export default ExplanationCharts;