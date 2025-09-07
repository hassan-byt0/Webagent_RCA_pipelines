// src/components/PrivacyConsent.jsx

import React, { useState } from 'react';
import { Modal, Typography, Button, Space, Checkbox } from 'antd';

const { Title, Paragraph, Text, Link } = Typography;

const PrivacyConsent = () => {
  const [visible, setVisible] = useState(true);
  const [moreVisible, setMoreVisible] = useState(false);
  const [cookieSettings, setCookieSettings] = useState({
    analytics: true,
    marketing: true,
  });

  const handleAccept = () => {
    setVisible(false);
  };

  const handleMoreOptions = () => {
    setMoreVisible(true);
  };

  const handleMoreClose = () => {
    setMoreVisible(false);
    setVisible(false);
  };

  const handleCookieChange = (e) => {
    const { name, checked } = e.target;
    setCookieSettings(prev => ({ ...prev, [name]: checked }));
  };

  return (
    <>
      <Modal
        id="privacy-consent-modal"
        aria-label="Privacy Consent Modal"
        open={visible}
        onCancel={() => setVisible(false)}
        maskClosable={false} // added to disable closing by clicking outside
        footer={null}
        centered
        width={520}
        closable={false}
        bodyStyle={{
          borderRadius: 12,
          padding: 24,
        }}
        style={{
          top: 50,
        }}
      >
        <Title level={3} style={{ marginBottom: 16 }}>
          We respect your privacy
        </Title>

        <Paragraph>
          Our website uses cookies to create a personalised and optimal user experience
          just for you. By allowing us to track your online activity, we can customise
          content to match your preferences and provide a seamless, enjoyable journey.
        </Paragraph>

        <Paragraph>
          This also allows our{' '}
          <Link href="#" onClick={(e) => e.preventDefault()}>
            partners
          </Link>{' '}
          to provide more tailored services to you. Clicking on &quot;More Information&quot;
          gives you an overview of our partners and insights into their legitimate interest
          in your data. You don&apos;t have to consent, but you may experience less
          personalised content. You can change your settings by following the link below
          and read our{' '}
          <Link href="#" onClick={(e) => e.preventDefault()}>
            Privacy Policy
          </Link>{' '}
          to learn about how we use your data.
        </Paragraph>

        <Paragraph style={{ marginBottom: 0 }}>
          Click &quot;I Accept&quot; to embark on an enhanced digital journey with us.
        </Paragraph>

        <Space
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginTop: 16,
          }}
        >
          <Button id="privacy-more-options-btn" type="text" onClick={handleMoreOptions}>
            More Options
          </Button>
          <Button id="privacy-accept-btn" type="primary" onClick={handleAccept}>
            I Accept
          </Button>
        </Space>
      </Modal>

      <Modal
        id="privacy-settings-modal"
        aria-label="Cookie and Privacy Settings Modal"
        open={moreVisible}
        onCancel={handleMoreClose}
        maskClosable={false} // added to disable closing by clicking outside
        footer={null}
        centered
        width={520}
        bodyStyle={{
          borderRadius: 12,
          padding: 24,
        }}
        style={{
          top: 50,
        }}
      >
        <Title level={3} style={{ marginBottom: 16 }}>
          Cookie & Privacy Settings
        </Title>
        <Paragraph>
          Customize your cookie preferences:
        </Paragraph>
        <Checkbox
          id="analytics-cookies"
          name="analytics"
          checked={cookieSettings.analytics}
          onChange={handleCookieChange}
          style={{ marginBottom: 8 }}
        >
          Enable Analytics Cookies
        </Checkbox>
        <Checkbox
          id="marketing-cookies"
          name="marketing"
          checked={cookieSettings.marketing}
          onChange={handleCookieChange}
          style={{ marginBottom: 8 }}
        >
          Enable Marketing Cookies
        </Checkbox>
        <Space
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            marginTop: 16,
          }}
        >
          <Button id="privacy-save-btn" onClick={handleMoreClose}>
            Save & Close
          </Button>
        </Space>
      </Modal>
    </>
  );
};

export default PrivacyConsent;
