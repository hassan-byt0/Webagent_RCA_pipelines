// src/components/PersonalizedAdsModal.jsx

import React, { useState } from 'react';
import { Modal, Typography, Button, Space } from 'antd';

const { Title, Paragraph, Text, Link } = Typography;

/**
 * A modal that replicates the "Allow personalized ads?" prompt.
 */
const PersonalizedAdsModal = () => {
  const [open, setOpen] = useState(true);
  const [showExtraOptions, setShowExtraOptions] = useState(false); // new state for extra options

  const handleAccept = () => {
    setOpen(false);
  };

  const handleReview = () => {
    setShowExtraOptions(true); // show extra options instead of closing modal
  };

  // Close modal if user clicks outside or on the "X"
  const handleCancel = () => {
    setOpen(false);
    setShowExtraOptions(false); // reset extra options if modal is closed
  };

  const handleClose = () => {
    setOpen(false);
    setShowExtraOptions(false);
  };

  return (
    <Modal
      id="personalized-ads-modal"
      aria-labelledby="personalized-ads-modal-title"
      open={open}
      onCancel={handleCancel}
      footer={null}
      centered
      closable={false}  // remove the built-in close "X"
    >
      { !showExtraOptions ? (
        <>
          <Title id="personalized-ads-modal-title" level={4} style={{ marginBottom: 16 }}>
            Allow personalized ads?
          </Title>

          <Paragraph>
            Spotify does not charge users and relies on advertising as a revenue source.
          </Paragraph>
          <Paragraph>
            By clicking <Text strong>“Accept and continue”</Text>, you are allowing Spotify to
            personalize the ads you see based on your activity on the app and data received
            from third parties in accordance with our{' '}
            <Link id="personalized-ads-privacy-link" href="#" onClick={(e) => e.preventDefault()}>
              Privacy Policy
            </Link>{' '}
            and{' '}
            <Link id="personalized-ads-cookie-link" href="#" onClick={(e) => e.preventDefault()}>
              Cookie Policy
            </Link>.
          </Paragraph>
          <Paragraph>
            Your consent is not required in order to use Spotify and can be withdrawn at any time.
            Non-personalized ads will still be shown to users who opt out. You will find further
            information and how you can manage your consent under{' '}
            <Text italic>“Review Settings”</Text>.
          </Paragraph>

          <Space direction="vertical" style={{ width: '100%', marginTop: 16 }}>
            <Button
              id="personalized-ads-accept-btn"
              type="primary"
              block
              style={{
                backgroundColor: '#FE2C55',
                borderColor: '#FE2C55',
              }}
              onClick={handleAccept}
              aria-label="Accept personalized ads"
            >
              Accept and continue
            </Button>
            <Button
              id="personalized-ads-review-btn"
              type="text"
              block
              onClick={handleReview}
              aria-label="Review settings for ads"
            >
              Review Settings
            </Button>
          </Space>
        </>
      ) : (
        // New extra options content displayed upon reviewing settings
        <div id="personalized-ads-review-section" aria-label="Review Settings Section">
          <Title level={4} style={{ marginBottom: 16 }}>Review Settings - Ad Personalization Options</Title>
          <Paragraph>Select your ad personalization preference:</Paragraph>
          <Space direction="vertical" style={{ width: '100%', marginTop: 16 }}>
            <Button
              id="personalized-ads-enable-btn"
              type="default"
              block
              onClick={handleClose}
              aria-label="Enable personalized ads"
            >
              Enable Personalized Ads
            </Button>
            <Button
              id="personalized-ads-disable-btn"
              type="default"
              block
              onClick={handleClose}
              aria-label="Disable personalized ads"
            >
              Disable Personalized Ads
            </Button>
            <Button
              id="personalized-ads-back-btn"
              type="text"
              block
              onClick={() => setShowExtraOptions(false)}
              aria-label="Back to main options"
            >
              Back
            </Button>
          </Space>
        </div>
      )}
    </Modal>
  );
};

export default PersonalizedAdsModal;
