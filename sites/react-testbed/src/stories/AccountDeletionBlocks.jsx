// src/components/ConfirmPrimeCancellation.jsx

import React from 'react';
import {
  Typography,
  Steps,
  Button,
  Card,
  Alert,
  Space,
  List,
} from 'antd';

const { Title, Paragraph, Text, Link } = Typography;

const ConfirmPrimeCancellation = () => {
  const handleRemindMeLater = () => {
    alert('Remind me later chosen!');
  };

  const handleKeepMembership = () => {
    alert('Keeping membership chosen!');
  };

  const handlePause = () => {
    alert('Pausing membership on March 02, 2023.');
  };

  const handleEndLater = () => {
    alert('Membership will end on March 02, 2023.');
  };

  const handleEndNow = () => {
    alert('Membership will end immediately, refund issued.');
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 24 }}>
      {/* Progress indicator */}
      <Steps
        current={2} // for example, step 2 of 3
        items={[
          { title: 'Review' },
          { title: 'Confirm' },
          { title: 'Done' },
        ]}
        style={{ marginBottom: 24 }}
      />

      {/* Main Title */}
      <Title level={3} style={{ marginBottom: 8 }}>
        We’re sorry to see you go. Please confirm the cancellation of your membership.
      </Title>

      <Paragraph style={{ marginBottom: 24 }}>
        You could also consider the following:
      </Paragraph>

      {/* Alternative actions */}
      <Space style={{ marginBottom: 32 }} direction="vertical">
        <Space>
          <Button
            type="default"
            onClick={handleRemindMeLater}
            style={{
              backgroundColor: '#ffbb00',
              borderColor: '#ffbb00',
              color: '#000',
            }}
          >
            Remind Me Later
          </Button>
          <Text>Remind me three days before my membership renews.</Text>
        </Space>
        <Space>
          <Button
            type="default"
            onClick={handleKeepMembership}
            style={{
              backgroundColor: '#ffbb00',
              borderColor: '#ffbb00',
              color: '#000',
            }}
          >
            Keep My Membership
          </Button>
          <Text>
            You will continue enjoying all the benefits of Prime.{' '}
            <Link href="#">View everything included in Prime.</Link>
          </Text>
        </Space>
      </Space>

      {/* Pause your Prime membership */}
      <Title level={4}>Pause your Prime membership:</Title>
      <Card style={{ marginBottom: 24 }}>
        <Alert
          message="Items tied to your Prime membership will be affected if you pause your membership."
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
        <List
          dataSource={[
            'By pausing, you will no longer be eligible for your unclaimed Prime exclusive offers.',
          ]}
          renderItem={(item) => <List.Item>{item}</List.Item>}
          style={{ marginBottom: 16 }}
        />
        <Paragraph>
          Your benefits access will continue until <Text strong>March 02, 2023</Text>.
          After that date, your billing and benefits will be paused, and you will no
          longer be charged for your Prime membership. Use the quick-resume function
          anytime to regain access to your Prime benefits.{' '}
          <Link href="#">Learn More</Link>.
        </Paragraph>
        <Button
          type="default"
          onClick={handlePause}
          style={{
            backgroundColor: '#ffbb00',
            borderColor: '#ffbb00',
            color: '#000',
          }}
        >
          Pause on March 02, 2023
        </Button>
      </Card>

      {/* Cancel your Prime membership */}
      <Title level={4}>Cancel your Prime membership:</Title>
      <Card>
        <Alert
          message="Items tied to your Prime membership will be affected if you cancel your membership."
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
        <List
          dataSource={[
            'By cancelling, you will no longer be eligible for your unclaimed Prime exclusive offers.',
          ]}
          renderItem={(item) => <List.Item>{item}</List.Item>}
          style={{ marginBottom: 16 }}
        />

        <Paragraph>
          Your benefits will continue until <Text strong>March 02, 2023</Text>, after
          which your card will not be charged.{' '}
          <Link href="#">Learn More</Link>.
        </Paragraph>

        <Space direction="vertical">
          <Button
            type="default"
            onClick={handleEndLater}
            style={{
              backgroundColor: '#ffbb00',
              borderColor: '#ffbb00',
              color: '#000',
              marginBottom: 8,
            }}
          >
            End on March 02, 2023
          </Button>

          <Text type="secondary" style={{ textAlign: 'center', display: 'block' }}>
            OR
          </Text>

          <Paragraph style={{ marginTop: 0 }}>
            Your benefits will end immediately and you will be refunded{' '}
            <Text strong>$16.31</Text> for the remaining period of your membership.
          </Paragraph>

          <Button
            type="default"
            onClick={handleEndNow}
            style={{
              backgroundColor: '#ffbb00',
              borderColor: '#ffbb00',
              color: '#000',
            }}
          >
            End Now
          </Button>
        </Space>
      </Card>
    </div>
  );
};

export default ConfirmPrimeCancellation;
