import React from "react";
import { Form, Input, Button, Select, message } from "antd";
import { useNavigate } from "react-router-dom";

const { Option } = Select;

const NewsAlerts = () => {
  const navigate = useNavigate();

  const onFinish = (values) => {
    // Minimal implementation: Display a success message.
    message.success("News alert settings saved!");
  };

  return (
    <div style={{ maxWidth: 400, margin: "40px auto", padding: "20px", border: "1px solid #f0f0f0", borderRadius: "4px" }}>
      <h2>Set Up News Alerts</h2>
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item
          label="Email"
          name="email"
          rules={[
            { required: true, message: "Please input your email!" },
            { type: "email", message: "Please enter a valid email!" },
          ]}
        >
          <Input placeholder="your.email@example.com" />
        </Form.Item>
        <Form.Item label="Alert Frequency" name="frequency" rules={[{ required: true, message: "Select an alert frequency" }]}>
          <Select placeholder="Select frequency">
            <Option value="daily">Daily</Option>
            <Option value="weekly">Weekly</Option>
            <Option value="monthly">Monthly</Option>
          </Select>
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save Alerts
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate(-1)}>
            Cancel
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default NewsAlerts;
