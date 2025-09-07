// src/components/CompleteProfile.jsx

import React from 'react';
import { Row, Col, Card, Typography, Button } from 'antd';
import { CameraOutlined, UserOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

/**
 * A component that shows two "cards" for profile completion steps.
 */
const InteractiveHook = () => {
  return (
    <div style={{ padding: 16 }}>
      <Title level={4}>Complete your profile</Title>
      <Text type="secondary" style={{ display: 'block', marginBottom: 24 }}>
        0/3 completed
      </Text>

      <Row gutter={16}>
        {/* First card: Add profile photo */}
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card hoverable style={{ textAlign: 'center' }}>
            <CameraOutlined style={{ fontSize: 36, marginBottom: 8 }} />
            <Title level={5}>Add profile photo</Title>
            <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
              Which photo represents you?
            </Text>
            <Button
              type="primary"
              style={{ backgroundColor: '#FE2C55', borderColor: '#FE2C55' }}
            >
              Add
            </Button>
          </Card>
        </Col>

        {/* Second card: Include your name */}
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card hoverable style={{ textAlign: 'center' }}>
            <UserOutlined style={{ fontSize: 36, marginBottom: 8 }} />
            <Title level={5}>Include your name</Title>
            <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
              What should people call you?
            </Text>
            <Button
              type="primary"
              style={{ backgroundColor: '#FE2C55', borderColor: '#FE2C55' }}
            >
              Add
            </Button>
          </Card>
        </Col>

        {/* You could add a third or more cards if desired */}
      </Row>
    </div>
  );
};

export default InteractiveHook;
