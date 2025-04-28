import React from 'react';
import { Card, Tabs, Empty } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const { TabPane } = Tabs;

const ExplanationCharts = ({ explanationData }) => {
  if (!explanationData) {
    return <Empty description="No explanation data available" />;
  }

  const { shap_values, feature_importance, lime_explanation } = explanationData;
  
  // Transform SHAP values for visualization
  const shapData = Object.entries(shap_values).map(([feature, value]) => ({
    feature,
    impact: Math.abs(value),
    value,
    direction: value >= 0 ? 'Increases Risk' : 'Decreases Risk'
  })).sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

  // Transform feature importance values
  const importanceData = Object.entries(feature_importance)
    .map(([feature, value]) => ({ feature, importance: value }))
    .sort((a, b) => b.importance - a.importance);

  return (
    <Card className="mt-4">
      <Tabs defaultActiveKey="1">
        <TabPane tab="SHAP Values" key="1">
          <div className="my-4">
            <p>SHAP values show how each feature contributed to this specific prediction:</p>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={shapData}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 150, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="feature" />
                <Tooltip 
                  formatter={(value, name, props) => {
                    return [`Impact: ${Math.abs(value).toFixed(4)}`, props.payload.direction];
                  }}
                />
                <Legend />
                <Bar 
                  dataKey="value" 
                  fill={(entry) => entry.value >= 0 ? "#ff4d4f" : "#52c41a"} 
                  name="Impact on Prediction" 
                />
              </BarChart>
            </ResponsiveContainer>
            <ul className="mt-4 text-sm">
              <li><span className="text-red-500">■</span> Red bars show features that increased the risk</li>
              <li><span className="text-green-500">■</span> Green bars show features that decreased the risk</li>
            </ul>
          </div>
        </TabPane>
        
        <TabPane tab="Feature Importance" key="2">
          <div className="my-4">
            <p>Feature importance shows which factors generally matter most in heart disease prediction:</p>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={importanceData}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 150, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="feature" />
                <Tooltip />
                <Bar dataKey="importance" fill="#1890ff" name="Importance" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </TabPane>
        
        <TabPane tab="LIME Explanation" key="3">
          <div className="my-4">
            <p>LIME explains the model by perturbing the input and observing changes:</p>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={lime_explanation}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 150, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="feature" />
                <Tooltip />
                <Bar 
                  dataKey="weight" 
                  fill={(entry) => entry.weight >= 0 ? "#ff4d4f" : "#52c41a"} 
                  name="Feature Weight" 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </TabPane>
      </Tabs>
    </Card>
  );
};

export default ExplanationCharts;