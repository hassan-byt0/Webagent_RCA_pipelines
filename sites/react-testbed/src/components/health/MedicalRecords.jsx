// src/components/health/MedicalRecords.jsx

import React from "react";
import { Layout, Card } from "antd";
import users from "./data/users";

const { Content } = Layout;

const MedicalRecords = () => {
  const currentUser = users.find((u) => u.id === "1"); // Replace with actual user ID

  if (!currentUser) {
    return (
      <Content id="medical-records-content" className="medical-records-content" aria-label="Medical Records Section">
        <h2>User not found.</h2>
      </Content>
    );
  }

  const { medicalRecords } = currentUser;

  if (!medicalRecords || medicalRecords.length === 0) {
    return (
      <Content id="medical-records-content" className="medical-records-content" aria-label="Medical Records Section">
        <h2 id="medical-records-header">My Medical Records</h2>
        <p>No medical records found.</p>
      </Content>
    );
  }

  return (
    <Content id="medical-records-content" className="medical-records-content" aria-label="Medical Records Section">
      <h2 id="medical-records-header">My Medical Records</h2>

      {medicalRecords.map((record) => (
        <Card id={`record-card-${record.id}`} title={record.title} className="record-card" key={record.id} aria-label={`Medical Record: ${record.title}`}>
          <p>
            <strong>Date:</strong> {record.date}
          </p>
          <p>
            <strong>Doctor:</strong> {record.doctor}
          </p>
          <p>
            <strong>Notes:</strong> {record.notes}
          </p>
        </Card>
      ))}
    </Content>
  );
};

export default MedicalRecords;
