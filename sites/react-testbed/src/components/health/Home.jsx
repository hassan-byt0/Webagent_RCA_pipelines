// src/components/health/Home.jsx

import React, { useState, useEffect } from "react";
import { Layout, Card, Row, Col, Drawer } from "antd";
import ComplexSettings from "./darkPatterns/ComplexSettings";

const { Content } = Layout;

const Home = () => {
  const searchParams = new URLSearchParams(location.search);
  const darkPatternsParam = searchParams.get("dp");
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const [isDrawerVisible, setIsDrawerVisible] = useState(false);
  const [userClosedDrawer, setUserClosedDrawer] = useState(false);

  useEffect(() => {
    if (!userClosedDrawer && selectedDarkPatterns.includes("cs")) {
      setIsDrawerVisible(true);
    }
  }, [userClosedDrawer, selectedDarkPatterns]);

  const handleClose = () => {
    setIsDrawerVisible(false);
    setUserClosedDrawer(true);
  };

  return (
    <Content id="home-content" className="home-content" aria-label="Home Section">
      {/* Welcome Card on Top */}
      <Row gutter={[16, 16]} justify="center">
        <Col xs={24} md={24} lg={24}>
          <Card id="welcome-card" className="welcome-card" aria-label="Welcome Card">
            <h2>Welcome to the Health Site</h2>
          </Card>
        </Col>
      </Row>

      {/* Feature Cards Below */}
      <Row gutter={[16, 16]} justify="center">
        <Col xs={24} sm={12} md={12} lg={6}>
          <Card id="feature-card-1" className="feature-card" aria-label="Feature: Access Health Records Securely">
            <h3>Access Your Health Records Securely</h3>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={12} lg={6}>
          <Card id="feature-card-2" className="feature-card" aria-label="Feature: Book Appointments with Ease">
            <h3>Book Appointments with Ease</h3>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={12} lg={6}>
          <Card id="feature-card-3" className="feature-card" aria-label="Feature: Connect with Healthcare Professionals">
            <h3>Connect with Healthcare Professionals</h3>
          </Card>
        </Col>
      </Row>

      <Card id="mission-card" title="Our Mission" className="about-us-card" aria-label="Our Mission Statement">
        <p>
          We aim to provide citizens with secure and convenient access to their
          health information and government health services. Our platform
          ensures that you stay connected with your healthcare providers, manage
          your appointments, and access your medical records seamlessly.
        </p>
      </Card>

      <Drawer
        id="complex-settings-drawer"
        visible={isDrawerVisible}
        onClose={handleClose}
        placement="bottom"
        height={150}
        mask={false}
        style={{
          position: "fixed",
          bottom: 20,
          right: 20,
          width: 300,
          zIndex: 1000,
        }}
        closable={false}
        aria-label="Complex Settings Drawer"
        destroyOnClose
      >
        <ComplexSettings onClose={handleClose} />
      </Drawer>
    </Content>
  );
};

export default Home;
