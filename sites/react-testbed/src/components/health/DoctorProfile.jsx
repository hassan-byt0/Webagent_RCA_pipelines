// src/components/health/DoctorProfile.jsx

import React from "react";
import { useParams } from "react-router-dom";
import { Layout, Avatar, Card, List } from "antd";
import doctors from "./data/doctors";

const { Content } = Layout;

const DoctorProfile = () => {
  const { doctorId } = useParams();
  const doctor = doctors.find((d) => d.id === doctorId);

  if (!doctor) {
    return <Content>Doctor not found.</Content>;
  }

  return (
    <Content id="doctor-profile-content" className="doctor-profile-content" aria-label="Doctor Profile Section">
      <Card id="doctor-profile-card" className="doctor-profile-card" aria-label={`Profile of Dr. ${doctor.name}`}>
        <Avatar id="doctor-avatar" size={100} src={doctor.avatar} aria-label={`Avatar of Dr. ${doctor.name}`} />
        <h2 id="doctor-name">{doctor.name}</h2>
        <h3 id="doctor-specialty">{doctor.specialty}</h3>
        <List
          id="doctor-schedule-list"
          header={<div>Schedule</div>}
          dataSource={doctor.schedule}
          renderItem={(item) => (
            <List.Item aria-label={`Schedule for ${item.day}: ${item.time}`}>
              {item.day}: {item.time}
            </List.Item>
          )}
          aria-label="Doctor's Schedule List"
        />
      </Card>
    </Content>
  );
};

export default DoctorProfile;
