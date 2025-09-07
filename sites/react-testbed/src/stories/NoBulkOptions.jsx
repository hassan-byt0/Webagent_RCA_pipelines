// src/components/PlanAndNotifications.jsx

import React, { useState } from 'react';
import {
  Row,
  Col,
  Card,
  Typography,
  Button,
  Radio,
  List,
  Collapse,
  Switch,
  Space,
} from 'antd';
import { CrownOutlined, DownOutlined, RightOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Panel } = Collapse;

/**
 * Combined UI for "Choose Your Plan" and "What Notifications You Receive".
 */
const PlanAndNotifications = () => {
  // Keep track of which plan is selected: 'monthly' or 'yearly'
  const [plan, setPlan] = useState('yearly');

  // Handlers
  const handlePlanChange = (e) => {
    setPlan(e.target.value);
  };

  const handleUpgrade = () => {
    alert(`Upgrading to the ${plan} plan!`);
  };

  // Notification toggles
  const [commentsPush, setCommentsPush] = useState(true);
  const [commentsEmail, setCommentsEmail] = useState(true);
  const [commentsSMS, setCommentsSMS] = useState(true);

  const [tagsPush, setTagsPush] = useState(true);
  const [tagsEmail, setTagsEmail] = useState(true);
  const [tagsSMS, setTagsSMS] = useState(true);

  const [remindersPush, setRemindersPush] = useState(true);
  const [remindersEmail, setRemindersEmail] = useState(true);
  const [remindersSMS, setRemindersSMS] = useState(true);

  const planFeatures = [
    'Access over 5000+ designs',
    'No watermarks',
    'Ad-free experience',
    'Download, print & send online',
    'Cancel anytime',
  ];

  return (
    <div style={{ padding: 24 }}>
      <Row gutter={32}>
        {/* Left Column: Choose Your Plan */}
        <Col xs={24} md={12}>
          <Title level={3} style={{ marginBottom: 16 }}>
            Choose Your Plan
          </Title>

          <Card style={{ marginBottom: 16, border: 'none' }} bodyStyle={{ padding: 0 }}>
            <Radio.Group onChange={handlePlanChange} value={plan} style={{ width: '100%' }}>
              <Card
                hoverable
                style={{
                  borderColor: plan === 'monthly' ? '#9254de' : '#f0f0f0',
                  marginBottom: 16,
                }}
                onClick={() => setPlan('monthly')}
              >
                <Title level={4} style={{ margin: 0 }}>
                  Monthly
                </Title>
                <Text strong style={{ fontSize: 20 }}>
                  $2.95
                </Text>
                <Text>/mo</Text>
                <br />
                <Text type="secondary">$35.40/year</Text>
              </Card>

              <Card
                hoverable
                style={{
                  borderColor: plan === 'yearly' ? '#9254de' : '#f0f0f0',
                }}
                onClick={() => setPlan('yearly')}
              >
                <Title level={4} style={{ margin: 0 }}>
                  Yearly
                </Title>
                <Text strong style={{ fontSize: 20 }}>
                  $1.95
                </Text>
                <Text>/mo</Text>
                <br />
                <Text type="secondary">$23.40/year &nbsp;</Text>
                <Text style={{ color: '#9254de', fontWeight: 600 }}>Save 33%</Text>
              </Card>
            </Radio.Group>
          </Card>

          <List
            dataSource={planFeatures}
            renderItem={(item) => (
              <List.Item style={{ padding: '4px 0', border: 'none' }}>
                <Text>✓ {item}</Text>
              </List.Item>
            )}
          />
          <Button
            type="primary"
            icon={<CrownOutlined />}
            size="large"
            onClick={handleUpgrade}
            style={{ marginTop: 16, background: '#9254de', borderColor: '#9254de' }}
          >
            Upgrade
          </Button>
        </Col>

        {/* Right Column: Notifications */}
        <Col xs={24} md={12}>
          <Title level={4} style={{ marginBottom: 16 }}>
            What Notifications You Receive
          </Title>
          <Collapse
            defaultActiveKey={['comments']}
            expandIconPosition="end"
            bordered={false}
            style={{ background: '#fff' }}
            expandIcon={({ isActive }) =>
              isActive ? <DownOutlined /> : <RightOutlined />
            }
          >
            {/* COMMENTS */}
            <Panel
              header={
                <>
                  <Text strong>Comments</Text>
                  <Text type="secondary" style={{ marginLeft: 8 }}>
                    Push, Email, SMS
                  </Text>
                </>
              }
              key="comments"
            >
              <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
                These are notifications for comments on your posts and replies to your
                comments.
              </Text>
              <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
                Where you receive these notifications
              </Text>

              <Space
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 8,
                }}
              >
                <Text>Push</Text>
                <Switch
                  checked={commentsPush}
                  onChange={(checked) => setCommentsPush(checked)}
                />
              </Space>
              <Space
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 8,
                }}
              >
                <Text>Email</Text>
                <Switch
                  checked={commentsEmail}
                  onChange={(checked) => setCommentsEmail(checked)}
                />
              </Space>
              <Space style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text>SMS</Text>
                <Switch
                  checked={commentsSMS}
                  onChange={(checked) => setCommentsSMS(checked)}
                />
              </Space>
            </Panel>

            {/* TAGS */}
            <Panel
              header={
                <>
                  <Text strong>Tags</Text>
                  <Text type="secondary" style={{ marginLeft: 8 }}>
                    Push, Email, SMS
                  </Text>
                </>
              }
              key="tags"
            >
              <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
                Notifications when someone tags you.
              </Text>
              <Space
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 8,
                }}
              >
                <Text>Push</Text>
                <Switch
                  checked={tagsPush}
                  onChange={(checked) => setTagsPush(checked)}
                />
              </Space>
              <Space
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 8,
                }}
              >
                <Text>Email</Text>
                <Switch
                  checked={tagsEmail}
                  onChange={(checked) => setTagsEmail(checked)}
                />
              </Space>
              <Space style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text>SMS</Text>
                <Switch
                  checked={tagsSMS}
                  onChange={(checked) => setTagsSMS(checked)}
                />
              </Space>
            </Panel>

            {/* REMINDERS */}
            <Panel
              header={
                <>
                  <Text strong>Reminders</Text>
                  <Text type="secondary" style={{ marginLeft: 8 }}>
                    Push, Email, SMS
                  </Text>
                </>
              }
              key="reminders"
            >
              <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
                Notifications for important reminders (events, tasks, deadlines).
              </Text>
              <Space
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 8,
                }}
              >
                <Text>Push</Text>
                <Switch
                  checked={remindersPush}
                  onChange={(checked) => setRemindersPush(checked)}
                />
              </Space>
              <Space
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: 8,
                }}
              >
                <Text>Email</Text>
                <Switch
                  checked={remindersEmail}
                  onChange={(checked) => setRemindersEmail(checked)}
                />
              </Space>
              <Space style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text>SMS</Text>
                <Switch
                  checked={remindersSMS}
                  onChange={(checked) => setRemindersSMS(checked)}
                />
              </Space>
            </Panel>
          </Collapse>
        </Col>
      </Row>
    </div>
  );
};

export default PlanAndNotifications;
