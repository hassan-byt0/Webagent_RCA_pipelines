"use client";

import React, { useEffect, useState } from "react";
import { Form, Input, Button, message } from "antd";
import { useParams, useRouter } from "next/navigation";
import users, { User } from "../data/users";
import { useId } from "react-id-generator";

interface FormValues {
  name: string;
  title: string;
  about: string;
  location: string;
  salary?: number;
  jobType?: string;
}

const EditProfile: React.FC = () => {
  const params = useParams();
  const router = useRouter();
  const { userId } = params;

  const [form] = Form.useForm();
  const [user, setUser] = useState<User | undefined>(
    users.find((u) => u.id === userId && u.isCurrentUser)
  );

  // Generate unique IDs
  const [
    nameInputId,
    titleInputId,
    aboutTextAreaId,
    locationInputId,
    salaryInputId,
    jobTypeInputId,
    saveButtonId,
    cancelButtonId,
  ] = useId(8, "edit-profile-");

  useEffect(() => {
    if (!user) {
      message.error("Access denied.");
      router.back();
    } else {
      form.setFieldsValue({
        name: user.name,
        title: user.title,
        about: user.about,
        location: user.location,
        salary: user.salary,
        jobType: user.jobType,
      });
    }
  }, [user, form, router]);

  const onFinish = (values: FormValues) => {
    if (user) {
      user.name = values.name;
      user.title = values.title;
      user.about = values.about;
      user.location = values.location;
      user.salary =
        values.salary !== undefined
          ? parseInt(values.salary.toString(), 10)
          : user.salary;
      user.jobType = values.jobType || user.jobType;
      setUser({ ...user });

      message.success("Profile updated successfully!");
      router.push(`/linkedin/user/${user.id}`);
    }
  };

  if (!user) return null;

  return (
    <div className="p-4 max-w-md mx-auto">
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        className="bg-white p-6 rounded-lg shadow-md space-y-4"
      >
        <h2 className="text-xl font-semibold mb-4">Edit Profile</h2>
        <Form.Item
          label={<label htmlFor={nameInputId}>Full Name</label>}
          name="name"
          rules={[{ required: true, message: "Please enter your name" }]}
        >
          <Input id={nameInputId} aria-label="Full Name" />
        </Form.Item>
        <Form.Item
          label={<label htmlFor={titleInputId}>Title</label>}
          name="title"
          rules={[{ required: true, message: "Please enter your title" }]}
        >
          <Input id={titleInputId} aria-label="Title" />
        </Form.Item>
        <Form.Item
          label={<label htmlFor={aboutTextAreaId}>About</label>}
          name="about"
          rules={[{ required: true, message: "Please enter your bio" }]}
        >
          <Input.TextArea id={aboutTextAreaId} rows={4} aria-label="About" />
        </Form.Item>
        <Form.Item
          label={<label htmlFor={locationInputId}>Location</label>}
          name="location"
          rules={[{ required: true, message: "Please enter your location" }]}
        >
          <Input id={locationInputId} aria-label="Location" />
        </Form.Item>
        <Form.Item label="Salary" name="salary">
          <Input id={salaryInputId} type="number" aria-label="Salary" />
        </Form.Item>
        <Form.Item label="Job Type" name="jobType">
          <Input id={jobTypeInputId} aria-label="Job Type" />
        </Form.Item>
        <div className="flex justify-end space-x-2">
          <Button
            id={saveButtonId}
            type="primary"
            htmlType="submit"
            aria-label="Save Changes Button"
          >
            Save Changes
          </Button>
          <Button
            id={cancelButtonId}
            type="default"
            onClick={() => router.back()}
            aria-label="Cancel Button"
          >
            Cancel
          </Button>
        </div>
      </Form>
    </div>
  );
};

export default EditProfile;
