"use client";

import React from "react";
import { Modal, Form, Input, Button } from "antd";
import { useId } from "react-id-generator";

interface Job {
  id: string;
  title: string;
  companyName?: string;
  location: string;
  salary: number;
  jobType: string;
  description: string;
}

interface JobApplicationModalProps {
  visible: any;
  job: any;
  onClose: any;
  onApply: any;
  currentUserId: any;
}

const JobApplicationModal: React.FC<JobApplicationModalProps> = ({
  visible,
  job,
  onClose,
  onApply,
}) => {
  const [form] = Form.useForm();

  // Generate unique IDs for modal elements
  const [resumeInputId, coverLetterTextAreaId, cancelButtonId, submitButtonId] =
    useId(5, "job-application-modal-");

  const handleApply = () => {
    form
      .validateFields()
      .then((values) => {
        console.log("Application Submitted:", values);
        onApply();
        form.resetFields();
      })
      .catch((info) => {
        console.log("Validate Failed:", info);
      });
  };

  return (
    <Modal
      open={visible}
      title={`Apply for ${job.title}`}
      onCancel={onClose}
      footer={[
        <Button key="cancel" id={cancelButtonId} onClick={onClose}>
          Cancel
        </Button>,
        <Button
          key="submit"
          id={submitButtonId}
          type="primary"
          onClick={handleApply}
        >
          Submit Application
        </Button>,
      ]}
    >
      <Form form={form} layout="vertical" className="space-y-4">
        <Form.Item
          name="resume"
          label={<label htmlFor={resumeInputId}>Resume URL</label>}
          rules={[
            { required: true, message: "Please input the URL to your resume!" },
            { type: "url", message: "Please enter a valid URL!" },
          ]}
        >
          <Input
            id={resumeInputId}
            placeholder="https://yourresume.com"
            aria-label="Resume URL"
          />
        </Form.Item>
        <Form.Item
          name="coverLetter"
          label={<label htmlFor={coverLetterTextAreaId}>Cover Letter</label>}
          rules={[
            { required: true, message: "Please input your cover letter!" },
          ]}
        >
          <Input.TextArea
            id={coverLetterTextAreaId}
            rows={4}
            placeholder="Your cover letter here..."
            aria-label="Cover Letter"
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default JobApplicationModal;
