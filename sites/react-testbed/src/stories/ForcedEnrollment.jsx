// src/components/RealRealLogin.jsx

import React from 'react';
import { Row, Col, Card, Typography, Form, Input, Checkbox, Button } from 'antd';
import { FacebookFilled } from '@ant-design/icons';

const { Title, Text, Link } = Typography;

const RealRealLogin = () => {
  const onFinish = (values) => {
    console.log('Form Values:', values);
    alert('Logging in...');
    // Replace with your actual login logic
  };

  return (
    <div style={{ backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
      <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
        {/* Background images/placeholder on left/right */}
        <Col
          xs={0}
          md={8}
          style={{
            backgroundImage: 'url(https://via.placeholder.com/400x800?text=Model+Left)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            minHeight: '100vh',
          }}
        />
        <Col xs={24} md={8}>
          <Card style={{ margin: '0 auto', maxWidth: 360 }}>
            {/* Brand + tagline */}
            <div style={{ textAlign: 'center', marginBottom: 24 }}>
              <Title level={3} style={{ marginBottom: 0 }}>
                The RealReal
              </Title>
              <Text type="secondary">Authenticated Luxury Consignment</Text>
            </div>

            <Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>
              MEMBER SIGN IN
            </Title>

            {/* AntD Form */}
            <Form layout="vertical" onFinish={onFinish}>
              <Form.Item
                label="Email"
                name="email"
                rules={[{ required: true, message: 'Please enter your email' }]}
              >
                <Input placeholder="Email" />
              </Form.Item>

              <Form.Item
                label="Password"
                name="password"
                rules={[{ required: true, message: 'Please enter your password' }]}
              >
                <Input.Password placeholder="Password" />
              </Form.Item>

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 16,
                }}
              >
                <Form.Item name="remember" valuePropName="checked" noStyle>
                  <Checkbox>Remember Me</Checkbox>
                </Form.Item>
                <Link href="#">Forgot Password?</Link>
              </div>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  block
                  style={{
                    backgroundColor: '#333',
                    borderColor: '#333',
                    marginBottom: 16,
                  }}
                >
                  LOG IN
                </Button>
              </Form.Item>

              <div style={{ textAlign: 'center', marginBottom: 16 }}>OR</div>

              <Form.Item>
                <Button
                  icon={<FacebookFilled />}
                  block
                  style={{
                    backgroundColor: '#4267B2',
                    borderColor: '#4267B2',
                    color: '#fff',
                    marginBottom: 16,
                  }}
                  onClick={() => alert('Continue with Facebook')}
                >
                  CONTINUE WITH FACEBOOK
                </Button>
              </Form.Item>

              <div style={{ textAlign: 'center' }}>
                <Text type="secondary">Not a member? </Text>
                <Link href="#">Sign Up</Link>
                <Text type="secondary"> | New Consignor? </Text>
                <Link href="#">Start here</Link>
              </div>
            </Form>
          </Card>
        </Col>
        <Col
          xs={0}
          md={8}
          style={{
            backgroundImage: 'url(https://via.placeholder.com/400x800?text=Model+Right)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            minHeight: '100vh',
          }}
        />
      </Row>
    </div>
  );
};

export default RealRealLogin;
