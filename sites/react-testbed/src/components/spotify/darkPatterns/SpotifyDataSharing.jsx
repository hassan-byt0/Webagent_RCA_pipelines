import { Modal, Button, Switch, Typography } from "antd";
import { useState } from "react";

const { Title, Text } = Typography;

const SpotifyDataSharing = () => {
  const [isModalVisible, setIsModalVisible] = useState(true);
  const [dataSharing, setDataSharing] = useState(true); // Data sharing enabled by default

  const handleToggle = (checked) => {
    if (!checked) {
      setDataSharing(false);
    } else {
      setDataSharing(true);
    }
  };

  const handleClose = () => {
    if (dataSharing) {
      alert("Thank you for continuing to share your data!");
    }
    setIsModalVisible(false);
  };

  const handleOptOut = () => {
    alert(
      "Are you sure you want to disable data sharing? This will limit your experience. If you wish to proceed, you will need to go to Settings > Privacy."
    );
  };

  return (
    <Modal
      id="spotify-data-sharing-modal"
      aria-labelledby="spotify-data-sharing-title"
      title="Your Data, Your Experience"
      visible={isModalVisible}
      onCancel={handleClose}
      closable={false}
      footer={[
        <Button
          key="close"
          id="spotify-data-sharing-continue-btn"
          type="primary"
          onClick={handleClose}
          aria-label="Continue with data sharing"
        >
          Continue
        </Button>,
      ]}
    >
      <div>
        <Title id="spotify-data-sharing-title" level={4} style={{ color: "#1DB954" }}>
          Improve Your Spotify Experience
        </Title>
        <Text id="spotify-data-sharing-description" style={{ marginBottom: "1rem", display: "block", color: "#555" }}>
          By sharing your data, you help us personalize your playlists,
          recommendations, and ads. This allows you to enjoy a more tailored
          listening experience.
        </Text>
        <div
          id="spotify-data-sharing-toggle-container"
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "1rem",
          }}
        >
          <Text id="spotify-data-sharing-switch-label" style={{ fontWeight: "bold", color: "#333" }}>
            Enable Data Sharing
          </Text>
          <Switch
            id="spotify-data-sharing-switch"
            checked={dataSharing}
            onChange={handleToggle}
            checkedChildren="On"
            unCheckedChildren="Off"
            style={{ backgroundColor: dataSharing ? "#1DB954" : "#555" }}
            aria-label="Enable Data Sharing Toggle"
          />
        </div>
        <Text id="spotify-data-sharing-warning" style={{ fontSize: "0.85rem", color: "#888" }}>
          Disabling data sharing may limit your experience, including fewer
          personalized recommendations, ads, and playlist curations.
        </Text>
      </div>
    </Modal>
  );
};

export default SpotifyDataSharing;
