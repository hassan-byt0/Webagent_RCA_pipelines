// src/components/health/Dashboard.jsx

import React from "react";
import { Layout, Card, List, Avatar } from "antd";
import {
  CalendarOutlined,
  FileTextOutlined,
  MessageOutlined,
} from "@ant-design/icons";
import users from "./data/users";

const { Content } = Layout;

const Dashboard = () => {
  const currentUser = users.find((u) => u.id === "1"); // Replace with actual user ID

  return (
    <Content id="dashboard-content" className="dashboard-content" aria-label="User Dashboard Section">
      <h2 id="welcome-message">Welcome, {currentUser.name}</h2>

      <div id="dashboard-cards" className="dashboard-cards">
        <Card
          id="upcoming-appointments-card"
          title="Upcoming Appointments"
          className="dashboard-card"
          bordered={false}
          aria-label="Upcoming Appointments Card"
        >
          <List
            id="appointments-list"
            dataSource={currentUser.appointments}
            renderItem={(appointment) => (
              <List.Item aria-label={`Appointment on ${appointment.date} at ${appointment.time} with ${appointment.department} department and Dr. ${appointment.doctor}`}>
                <List.Item.Meta
                  avatar={<Avatar icon={<CalendarOutlined />} />}
                  title={`${appointment.date} at ${appointment.time}`}
                  description={`${appointment.department} with ${appointment.doctor}`}
                />
              </List.Item>
            )}
            aria-label="List of Upcoming Appointments"
          />
        </Card>

        <Card
          id="recent-medical-records-card"
          title="Recent Medical Records"
          className="dashboard-card"
          bordered={false}
          aria-label="Recent Medical Records Card"
        >
          <List
            id="medical-records-list"
            dataSource={currentUser.medicalRecords.slice(0, 3)} // Show recent 3 records
            renderItem={(record) => (
              <List.Item aria-label={`Medical Record: ${record.title} dated ${record.date} by Dr. ${record.doctor}`}>
                <List.Item.Meta
                  avatar={<Avatar icon={<FileTextOutlined />} />}
                  title={record.title}
                  description={`${record.date} by ${record.doctor}`}
                />
              </List.Item>
            )}
            aria-label="List of Recent Medical Records"
          />
          <div style={{ textAlign: "right", marginTop: "10px" }}>
            <a href="/health/medical-records" aria-label="View All Medical Records">View All Records</a>
          </div>
        </Card>

        <Card
          id="messages-card"
          title="Messages"
          className="dashboard-card"
          bordered={false}
          aria-label="Messages Card"
        >
          <List
            id="messages-list"
            dataSource={currentUser.messages.slice(0, 3)} // Show recent 3 messages
            renderItem={(msg) => (
              <List.Item aria-label={`Message from ${msg.sender}: ${msg.text}`}>
                <List.Item.Meta
                  avatar={<Avatar icon={<MessageOutlined />} />}
                  title={`From: ${msg.sender}`}
                  description={msg.text}
                />
              </List.Item>
            )}
            aria-label="List of Recent Messages"
          />
          <div style={{ textAlign: "right", marginTop: "10px" }}>
            <a href="/health/messages" aria-label="View All Messages">View All Messages</a>
          </div>
        </Card>
      </div>
    </Content>
  );
};

export default Dashboard;
