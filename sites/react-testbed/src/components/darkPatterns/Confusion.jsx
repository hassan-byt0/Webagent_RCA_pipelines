import React, { useState, useEffect } from 'react';
import { Checkbox, Modal, Button, Typography } from 'antd';

const { Text } = Typography;

/**
 * A marketing opt-in checkbox with intentionally confusing copy
 */
const MarketingOptIn = () => {
  const [checked, setChecked] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);

  // Auto-show modal on component mount
  useEffect(() => {
    setIsModalVisible(true);
  }, []);

  const handleChange = (e) => {
    setChecked(e.target.checked);
  };

  // Bring back the OK button with an onClick handler
  const handleOk = () => {
    setIsModalVisible(false);
  };

  return (
    <div>
      <Modal
        title="Marketing Opt-In"
        visible={isModalVisible}
        footer={[<Button key="ok" type="primary" onClick={handleOk}>OK</Button>]}
        closable={false} // Removed the X (close) button
      >
        <Checkbox
          id="marketing-optin-checkbox"
          aria-label="Marketing Opt-in Checkbox"
          checked={checked}
          onChange={handleChange}
        >
          <Text>
            Do not check this box if you wish to be contacted via email about product updates,
            upgrades, special offers and pricing
          </Text>
        </Checkbox>
      </Modal>
    </div>
  );
};

export default MarketingOptIn;
