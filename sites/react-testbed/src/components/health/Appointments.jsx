// src/components/health/Appointments.jsx

import React, { useState } from "react";
import { Layout, List, Avatar, Button, message, Modal, Form, Select } from "antd";
import users from "./data/users";
import doctors from "./data/doctors";
import { CalendarOutlined } from "@ant-design/icons";
import { doc } from "prettier";

const { Content } = Layout;

const Appointments = () => {
  const currentUser = users.find((u) => u.id === "1"); // Replace with actual user ID
  const [appointments, setAppointments] = useState(currentUser.appointments);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const handleCancelAppointment = (appointmentId) => {
    const updatedAppointments = appointments.filter(
      (appointment) => appointment.id !== appointmentId
    );
    setAppointments(updatedAppointments);
    message.success("Appointment canceled successfully.");
  };

  const openScheduleModal = () => {
    setIsModalVisible(true);
  };

  const handleScheduleOk = () => {
    form.validateFields().then((values) => {
      const doctor = doctors.find((doc) => doc.id === values.doctor);
      const [day, time] = values.slot.split("|");
      const newAppointment = {
        id: `a-${Date.now()}`,
        date: day, // For simplicity, using day as date placeholder
        time,
        department: doctor.specialty,
        doctor: doctor.name,
      };
      setAppointments([...appointments, newAppointment]);
      message.success("Appointment scheduled successfully.");
      setIsModalVisible(false);
      form.resetFields();
    });
  };

  const handleScheduleCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <Content id="appointments-content" className="appointments-content" aria-label="Appointments Section">
      <h2 id="appointments-header">My Appointments</h2>
      
      <Button id="open-schedule-modal" type="primary" onClick={openScheduleModal} style={{ marginBottom: "20px" }}>
        Schedule Appointment
      </Button>

      <List
        id="appointments-list"
        dataSource={appointments}
        style={{ width: "100%", padding: "0 20px" }}
        renderItem={(appointment) => (
          <List.Item
            actions={[
              <Button
                id={`cancel-appointment-${appointment.id}`}
                type="danger"
                onClick={() => handleCancelAppointment(appointment.id)}
                aria-label={`Cancel appointment on ${appointment.date} at ${appointment.time}`}
              >
                Cancel
              </Button>,
            ]}
            aria-label={`Appointment on ${appointment.date} at ${appointment.time} with ${appointment.department} department and Dr. ${appointment.doctor}`}
          >
            <List.Item.Meta
              avatar={<Avatar icon={<CalendarOutlined />} />}
              title={`${appointment.date} at ${appointment.time}`}
              description={`${appointment.department} with ${appointment.doctor}`}
            />
          </List.Item>
        )}
        aria-label="List of Appointments"
      />

      <Modal title="Schedule Appointment" visible={isModalVisible} onOk={handleScheduleOk} onCancel={handleScheduleCancel}>
        <Form form={form} layout="vertical">
          <Form.Item
            name="doctor"
            label="Doctor"
            rules={[{ required: true, message: "Select a doctor" }]}
          >
            <Select placeholder="Select a doctor">
              {doctors.map((doc) => (
                <Select.Option id={doc.name} key={doc.id} value={doc.id}>
                  {doc.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prevValues, currentValues) => prevValues.doctor !== currentValues.doctor}>
            {({ getFieldValue }) => {
              const selectedDoctorId = getFieldValue("doctor");
              const selectedDoctor = doctors.find((doc) => doc.id === selectedDoctorId);
              return selectedDoctor ? (
                <Form.Item
                  name="slot"
                  label="Available Slot"
                  rules={[{ required: true, message: "Select a time slot" }]}
                >
                  <Select placeholder="Select a time slot">
                    {selectedDoctor.schedule.map((s, index) => {
                      const value = `${s.day}|${s.time}`;
                      return (
                        <Select.Option id= {`${selectedDoctor.name}_${s.day}`} key={index} value={value}>
                          {`${s.day}: ${s.time}`}
                        </Select.Option>
                      );
                    })}
                  </Select>
                </Form.Item>
              ) : null;
            }}
          </Form.Item>
        </Form>
      </Modal>
    </Content>
  );
};

export default Appointments;
