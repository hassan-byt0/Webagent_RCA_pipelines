// src/components/SuggestAccountSettings.jsx

import React, { useState } from 'react';
import { Typography, Switch, Space } from 'antd';

const { Title, Text, Link } = Typography;

const SuggestAccountSettings = () => {
  // Switch states
  const [contacts, setContacts] = useState(true);
  const [facebookFriends, setFacebookFriends] = useState(true);
  const [mutualConnections, setMutualConnections] = useState(true);
  const [sharedLinks, setSharedLinks] = useState(true);

  // Handlers
  const handleContactsToggle = (checked) => {
    setContacts(checked);
  };

  const handleFacebookToggle = (checked) => {
    setFacebookFriends(checked);
  };

  const handleMutualToggle = (checked) => {
    setMutualConnections(checked);
  };

  const handleSharedLinksToggle = (checked) => {
    setSharedLinks(checked);
  };

  return (
    <div style={{ padding: 16, maxWidth: 600, margin: '0 auto' }}>
      {/* Header */}
      <Space style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <Title level={4} style={{ marginBottom: 0 }}>
          Suggest your account to others
        </Title>
        {/* 
          If you want an info icon or back arrow, add them here.
          For example: 
          <Space>
            <LeftOutlined onClick={() => console.log('Go Back')} />
            <QuestionCircleOutlined onClick={() => console.log('Show info')} />
          </Space>
        */}
      </Space>

      {/* Contacts */}
      <Space
        direction="vertical"
        style={{ width: '100%', marginBottom: 24, padding: '12px 0', borderBottom: '1px solid #f0f0f0' }}
      >
        <Space style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Text strong>Contacts</Text>
          <Switch checked={contacts} onChange={handleContactsToggle} />
        </Space>
        <Text type="secondary" style={{ fontSize: '0.875rem' }}>
          When switched on, your account will be suggested to your contacts.
          You haven't added a phone number.{' '}
          <Link href="#" onClick={(e) => e.preventDefault()}>
            Add a phone number
          </Link>{' '}
          for this setting.
        </Text>
      </Space>

      {/* Facebook friends */}
      <Space
        direction="vertical"
        style={{ width: '100%', marginBottom: 24, padding: '12px 0', borderBottom: '1px solid #f0f0f0' }}
      >
        <Space style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Text strong>Facebook friends</Text>
          <Switch checked={facebookFriends} onChange={handleFacebookToggle} />
        </Space>
        <Text type="secondary" style={{ fontSize: '0.875rem' }}>
          When switched on, your account will be suggested to your Facebook friends.
          You haven't connected to Facebook.{' '}
          <Link href="#" onClick={(e) => e.preventDefault()}>
            Connect a Facebook account
          </Link>{' '}
          for this setting.
        </Text>
      </Space>

      {/* Users with mutual connections */}
      <Space
        direction="vertical"
        style={{ width: '100%', marginBottom: 24, padding: '12px 0', borderBottom: '1px solid #f0f0f0' }}
      >
        <Space style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Text strong>Users with mutual connections</Text>
          <Switch checked={mutualConnections} onChange={handleMutualToggle} />
        </Space>
        <Text type="secondary" style={{ fontSize: '0.875rem' }}>
          When switched on, your account will be suggested to users with mutual connections.
        </Text>
      </Space>

      {/* Users who open or send shared links */}
      <Space
        direction="vertical"
        style={{ width: '100%', marginBottom: 8, padding: '12px 0' }}
      >
        <Space style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Text strong>Users who open or send shared links</Text>
          <Switch checked={sharedLinks} onChange={handleSharedLinksToggle} />
        </Space>
        <Text type="secondary" style={{ fontSize: '0.875rem' }}>
          When switched on, your account will be suggested to users when you open a shared link
          or when other users open your shared link.
        </Text>
      </Space>
    </div>
  );
};

export default SuggestAccountSettings;
