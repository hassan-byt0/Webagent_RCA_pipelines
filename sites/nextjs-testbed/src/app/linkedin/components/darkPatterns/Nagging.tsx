"use client";

import React from "react";
import { Modal, Button } from "antd";

interface NaggingProps {
  visible: boolean;
  onContinue: () => void;
  onSkip: () => void;
}

const Nagging: React.FC<NaggingProps> = ({ visible, onContinue, onSkip }) => {
  return (
    <Modal
      open={visible}
      title="LinkedIn works best when you're connected to more people"
      onCancel={onSkip}
      aria-labelledby="linkedin-modal-title"
      aria-describedby="linkedin-modal-description"
      footer={[
        <Button
          key="skip"
          id="skip-button"
          onClick={onSkip}
          aria-label="Skip this step"
        >
          Skip
        </Button>,
        <Button
          key="continue"
          id="continue-button"
          type="primary"
          onClick={onContinue}
          aria-label="Continue to the next step"
        >
          Continue
        </Button>,
      ]}
    >
      <p id="linkedin-modal-description">Are you sure you want to skip this step?</p>
    </Modal>
  );
};

export default Nagging;
