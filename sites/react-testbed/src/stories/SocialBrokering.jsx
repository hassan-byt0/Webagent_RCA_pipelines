// src/components/DeleteAccountConfirmation.jsx

import React from 'react';
import { Typography, Button } from 'antd';

const { Paragraph, Text } = Typography;

/**
 * Displays the confirmation text and bullet points for deleting an account,
 * followed by a "Continue" button.
 */
const DeleteAccountConfirmation = () => {
  const bulletPoints = [
    'You will no longer be able to log in to TikTok with that account.',
    'You will lose access to any videos you have posted.',
    'You will not be able to get a refund on any items you have purchased.',
    'Information that is not stored in your account, such as chat messages, may still be visible to others.',
    'Your account will be deactivated for 30 days. During deactivation, your account won’t be visible to the public. After 30 days, your account will then be deleted permanently.',
    'Do you want to continue?',
  ];

  const handleContinue = () => {
    alert('Continuing account deletion...');
    // Replace with your actual deletion logic
  };

  return (
    <div style={{ maxWidth: 400, margin: '0 auto', padding: 16 }}>
      <Paragraph>If you delete your account:</Paragraph>
      <ul>
        {bulletPoints.map((item, index) => (
          <li key={index} style={{ marginBottom: 8 }}>
            <Text>{item}</Text>
          </li>
        ))}
      </ul>
      <Button
        type="primary"
        onClick={handleContinue}
        style={{
          backgroundColor: '#FE2C55',
          borderColor: '#FE2C55',
          marginTop: 16,
          width: '100%',
        }}
      >
        Continue
      </Button>
    </div>
  );
};

export default DeleteAccountConfirmation;
