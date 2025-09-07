// src/components/ReviewForm.js
import React, { useState } from "react";
import { Form, Input, Radio, Button } from "antd";

// const { TextArea } = Input;

function ReviewForm({ onSubmit }) {
  const [form] = Form.useForm();

  const handleSubmit = (values) => {
    onSubmit({
      ...values,
      username: "Web_Agent",
      id: Date.now(), // Use timestamp as a simple unique id
      date: new Date().toISOString(),
    });
    form.resetFields();
  };

  return (
    <Form form={form} onFinish={handleSubmit} layout="vertical">
      <Form.Item
        name="rating"
        // label="Rating"
        rules={[{ required: true, message: "Please select a rating" }]}
      >
        <Radio.Group aria-label="Rating Selection">
          {[1, 2, 3, 4, 5].map((star) => (
            <Radio key={star} value={star} id={`review-star-${star}`}>
              {star} Star{star > 1 ? "s" : ""}
            </Radio>
          ))}
        </Radio.Group>
      </Form.Item>
      <Form.Item
        name="comment"
        // label="Your Review"
        rules={[{ required: true, message: "Please write your review" }]}
      >
        <Input
          id="review-textbox"
          placeholder="Type your review here"
          aria-label="Review Textbox"
        />
      </Form.Item>
      <Form.Item>
        <Button
          id="submit-review-button"
          type="primary"
          htmlType="submit"
          aria-label="Submit Review"
        >
          Submit Review
        </Button>
      </Form.Item>
    </Form>
  );
}

export default ReviewForm;
