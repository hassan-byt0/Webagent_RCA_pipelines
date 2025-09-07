// src/components/AudibleTrialOffer.jsx

import React from 'react';
import { Typography, Button, Row, Col, List } from 'antd';
import { CheckOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

/**
 * A promotional component for an Audible-style 30-day free trial offer.
 */
const AudibleTrialOffer = () => {
  const trialBenefits = [
    'Free membership for 30 days with 1 audiobook + 2 Audible Originals.',
    'After trial, 3 titles each month: 1 audiobook + 2 Audible Originals.',
    'Roll over any unused credits for up to 5 months.',
    'Exclusive audio-guided wellness programs.',
  ];

  // Sample images representing audiobooks (use real URLs in a real app)
  const bookImages = [
    'https://via.placeholder.com/80?text=Book1',
    'https://via.placeholder.com/80?text=Book2',
    'https://via.placeholder.com/80?text=Book3',
    'https://via.placeholder.com/80?text=Book4',
    'https://via.placeholder.com/80?text=Book5',
    'https://via.placeholder.com/80?text=Book6',
  ];

  const handleTrialClick = () => {
    alert('Redirecting to Audible Free Trial signup...');
  };

  return (
    <div style={{ padding: 24, background: '#fff' }}>
      <Row gutter={24} align="middle">
        {/* Left side: text & bullet points */}
        <Col xs={24} md={12}>
          <Title level={3} style={{ marginBottom: 16 }}>
            Start your free 30-day trial
          </Title>
          <List
            dataSource={trialBenefits}
            renderItem={(item) => (
              <List.Item style={{ border: 'none', paddingLeft: 0 }}>
                <CheckOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                {item}
              </List.Item>
            )}
            style={{ marginBottom: 24 }}
          />

          <Button
            type="primary"
            size="large"
            onClick={handleTrialClick}
            style={{
              backgroundColor: '#FF9900',
              borderColor: '#FF9900',
              height: 48,
              fontSize: 16,
              marginBottom: 8,
            }}
            block
          >
            Click to Try Audible Free
          </Button>

          <Text type="secondary">
            $14.95 per month after 30 days. Cancel anytime.
          </Text>
        </Col>

        {/* Right side: Book covers collage */}
        <Col xs={24} md={12}>
          <Row gutter={[8, 8]}>
            {bookImages.map((src, index) => (
              <Col key={index} span={8} style={{ textAlign: 'center' }}>
                <img
                  src={src}
                  alt={`Book cover ${index + 1}`}
                  style={{ width: '80px', height: '80px', objectFit: 'cover' }}
                />
              </Col>
            ))}
          </Row>
        </Col>
      </Row>
    </div>
  );
};

export default AudibleTrialOffer;
