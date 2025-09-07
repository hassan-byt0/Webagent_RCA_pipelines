// src/components/GmailUpgradePrompt.jsx

import React, { useState } from 'react';
import { Modal, Typography, Button, Space, Image } from 'antd';

const { Title, Paragraph, Link, Text } = Typography;

const PWAConfirmShaming = () => {
  const [visible, setVisible] = useState(true);

  const handleCancel = () => {
    setVisible(false);
  };

  const handleAccept = () => {
    setVisible(false);
  };

  return (
    <Modal
      id="pwa-confirm-shaming-modal"
      aria-label="PWA Confirm Shaming Modal"
      open={visible}
      onCancel={() => setVisible(false)}
      footer={null}
      centered
      width={520}
      closable={false}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
        <Image
          id="pwa-logo-image"
          aria-label="PWA Logo Image"
          src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.mindinventory.com%2Fblog%2Fwp-content%2Fuploads%2F2022%2F10%2Fpwa-framework.png&f=1&nofb=1&ipt=6a2698d819a8bae1879a32883196868e02e8194ed51f7870c8ddfdaa39c64d74&ipo=images"
          width={50}
          height={50}
          preview={false}
          style={{ marginRight: 16 }}
        />
        <Title level={4} style={{ margin: 0 }}>
          Switch to a Progressive Web App for faster performance
        </Title>
      </div>

      <Paragraph>
        The official PWA provides a quicker, smoother, and more responsive experience.
        We’ll send you a link to install it on your device.
      </Paragraph>

      <Space style={{ display: 'flex', justifyContent: 'space-between', marginTop: 24 }}>
        <Button
          id="pwa-decline-btn"
          aria-label="Decline PWA Upgrade"
          type="text"
          onClick={handleCancel}
        >
          I DON'T WANT FASTER WEB
        </Button>
        <Button
          id="pwa-accept-btn"
          aria-label="Accept PWA Upgrade"
          type="primary"
          onClick={handleAccept}
        >
          YES, I WANT IT
        </Button>
      </Space>
    </Modal>
  );
};

export default PWAConfirmShaming;
