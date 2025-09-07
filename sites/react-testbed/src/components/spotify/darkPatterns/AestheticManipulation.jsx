// src/components/PricingPlans.jsx

import React, { useState } from 'react';
import { Row, Col, Card, Typography, Tag, Button, Space } from 'antd';
import {useSearchParams} from "react-router-dom";
import { LockOutlined, CheckCircleOutlined, CloseOutlined } from '@ant-design/icons';

const { Title, Text, Link } = Typography;

const plans = [
  {
    title: 'Spotify Premium Individual',
    price: 'US$9.99',
    frequency: '/mo',
    subtitle: 'Ad-free music streaming for one account.',
    linkLabel: 'Learn more',
    bestValue: false,
  },
  {
    title: 'Spotify Premium Duo',
    price: 'US$12.99',
    frequency: '/mo',
    subtitle: 'Enjoy premium music for two people living together.',
    linkLabel: 'Learn more',
    bestValue: true,
  },
  {
    title: 'Spotify Premium Family',
    price: 'US$14.99',
    frequency: '/mo',
    subtitle: 'Up to 6 premium accounts for family members under one roof.',
    linkLabel: 'Learn more',
    bestValue: false,
  },
];

const PricingPlans = () => {
  const [showOverlay, setShowOverlay] = useState(false);
  const [purchasedPlan, setPurchasedPlan] = useState(null);
  const [searchParams] = useSearchParams();

  const darkPatternsParam = searchParams.get("dp");
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const handlePurchase = (planIndex) => {
    setPurchasedPlan(plans[planIndex].title);
    setShowOverlay(true);
  };

  const handleCloseOverlay = () => {
    setShowOverlay(false);
  };

  return (
    <div id="pricing-plans-container" style={{ padding: '20px', position: 'relative' }}>
      {showOverlay ? (
        <div style={{ textAlign: 'center', padding: '40px 20px' }}>
          <CheckCircleOutlined style={{ fontSize: '48px', color: '#52c41a', marginBottom: '16px' }} />
          <Title level={3} style={{ margin: 0, marginBottom: '8px' }}>
            Successfully purchased premium!
          </Title>
          <Text>{purchasedPlan} has been activated for your account</Text>
        </div>
      ) : (
        <>
          <Title id="pricing-plans-title" level={2} style={{ margin: '0 0 24px 0' }}>
            Pricing Plans
          </Title>
          <Row gutter={[24, 24]}>
            {plans.map((plan, index) => (
              <Col xs={24} sm={12} md={8} key={index}>
                <Card
                  id={`pricing-plan-card-${index}`}
                  aria-label={`Pricing plan card for ${plan.title}`}
                  style={{
                    border: (plan.bestValue && selectedDarkPatterns.includes("am")) ? '1px solid #FFD700' : undefined,
                    height: '100%',
                    borderRadius: '8px',
                  }}
                  bodyStyle={{ padding: 24 }}
                >
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Title id={`pricing-plans-title-${index}`} level={4} style={{ marginBottom: 0 }}>
                        {plan.title}
                      </Title>
                      {plan.bestValue && selectedDarkPatterns.includes("am") && (
                        <Tag id={`pricing-plans-best-value-tag-${index}`} color="gold" style={{ fontWeight: 'bold' }}>
                          Best value
                        </Tag>
                      )}
                    </div>
  
                    <div>
                      <Text strong style={{ fontSize: 20 }}>
                        {plan.price}
                      </Text>
                      <Text>{plan.frequency}</Text>
                    </div>
                    <Text type="secondary">per license</Text>
                    <Text>{plan.subtitle}{' '}</Text>
                    <Link
                      id={`pricing-plans-learn-more-${index}`}
                      href="#"
                      onClick={(e) => e.preventDefault()}
                      aria-label={`Learn more about ${plan.title}`}
                    >
                      {plan.linkLabel}
                    </Link>
  
                    <Space
                      align="center"
                      style={{
                        marginTop: 16,
                        display: 'flex',
                        justifyContent: 'space-between',
                      }}
                    >
                      <Space align="center">
                        <LockOutlined style={{ color: 'gray' }} />
                        <Text type="secondary">Secure transaction</Text>
                      </Space>
  
                      <Button
                        id={`pricing-plans-buy-btn-${index}`}
                        type="primary"
                        style={{ backgroundColor: '#0070F3', border: 'none' }}
                        aria-label="Buy now"
                        onClick={() => handlePurchase(index)}
                      >
                        Buy now
                      </Button>
                    </Space>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </>
      )}
    </div>
  );
};

export default PricingPlans;
