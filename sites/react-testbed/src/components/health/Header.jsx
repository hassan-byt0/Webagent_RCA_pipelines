// src/components/health/Header.jsx

import React from "react";
import { Layout, Menu } from "antd";
import {
  HomeOutlined,
  UserOutlined,
  LogoutOutlined,
  FileTextOutlined,
  CalendarOutlined,
  MessageOutlined,
  DownloadOutlined
} from "@ant-design/icons";
import { Link } from "react-router-dom";

const { Header } = Layout;

const HealthSiteHeader = () => {
  return (
    <Header id="health-header" className="health-header" style={{ height: "80px" }} aria-label="Health Site Header">
      <div
        id="health-logo"
        className="health-logo"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
        }}
        aria-label="Health Site Logo"
      >
        <Link to="/health">
          <span style={{ fontSize: "24px", fontWeight: "bold", color: "#fff" }}>
            Health Site
          </span>
        </Link>
      </div>
      {/* Ensure all menu items are always visible */}
      <Menu
        id="health-menu"
        mode="horizontal"
        selectable={false}
        className="health-menu"
        overflowedIndicator={null}
        aria-label="Health Site Navigation Menu"
      >
        <Menu.Item id="menu-home" key="home" icon={<HomeOutlined />} aria-label="Navigate to Home">
          <Link to="/health">Home</Link>
        </Menu.Item>
        <Menu.Item id="menu-records" key="records" icon={<FileTextOutlined />} aria-label="Navigate to Medical Records">
          <Link to="/health/medical-records">Medical Records</Link>
        </Menu.Item>
        <Menu.Item id="menu-appointments" key="appointments" icon={<CalendarOutlined />} aria-label="Navigate to Appointments">
          <Link to="/health/appointments">Appointments</Link>
        </Menu.Item>
        <Menu.Item id="menu-messages" key="messages" icon={<MessageOutlined />} aria-label="Navigate to Messages">
          <Link to="/health/messages">Messages</Link>
        </Menu.Item>
        <Menu.Item id="menu-lab-results" key="lab-results" icon={<DownloadOutlined />} aria-label="Navigate to Lab Results">
          <Link to="/health/lab-results">Lab Results</Link>
        </Menu.Item>
        <Menu.Item id="menu-profile" key="profile" icon={<UserOutlined />} aria-label="Navigate to My Profile">
          <Link to="/health/dashboard">My Profile</Link>
        </Menu.Item>
        <Menu.Item id="menu-logout" key="logout" icon={<LogoutOutlined />} aria-label="Logout from Health Site">
          <Link to="/health/logout">Logout</Link>
        </Menu.Item>
      </Menu>
    </Header>
  );
};

export default HealthSiteHeader;
