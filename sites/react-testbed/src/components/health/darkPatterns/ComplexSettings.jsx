import React, { useState } from "react";
import { Card, Switch, Typography, Divider, Button, Tooltip } from "antd";

const { Title, Text } = Typography;

const ComplexDataSettings = ({ onClose }) => {
  const [dataSharing, setDataSharing] = useState(true);
  const [activityTracking, setActivityTracking] = useState(true);
  const [locationAccess, setLocationAccess] = useState(true);
  const [visible, setVisible] = useState(true);

  const handleToggle = (option, checked) => {
    switch (option) {
      case "dataSharing":
        setDataSharing(checked);
        break;
      case "activityTracking":
        setActivityTracking(checked);
        break;
      case "locationAccess":
        setLocationAccess(checked);
        break;
      default:
        break;
    }
  };

  return (
    <>
      {visible && (
        <Card
          id="data-settings-card"
          aria-label="Data Privacy and Settings"
          style={{
            backgroundColor: "#f9f9f9",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "1.5rem",
            maxWidth: "600px",
            margin: "2rem auto",
            fontFamily: "Arial, sans-serif",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          }}
        >
          <Title level={4} style={{ color: "#333", marginBottom: "1rem" }}>
            Data Privacy & Settings
          </Title>
          <Text
            style={{
              color: "#555",
              fontSize: "0.9rem",
              marginBottom: "1rem",
              display: "block",
            }}
          >
            Manage your data sharing preferences. Disabling some settings may limit
            your personalized health insights and app features.
          </Text>

          <Divider />

          {/* Data Sharing */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Text
              style={{ fontWeight: "bold", color: "#333" }}
              id="data-sharing-label"
            >
              Enable Data Sharing
            </Text>
            <Switch
              id="data-sharing-switch"
              aria-label="Enable Data Sharing"
              checked={dataSharing}
              onChange={(checked) => handleToggle("dataSharing", checked)}
              checkedChildren="On"
              unCheckedChildren="Off"
              style={{ backgroundColor: dataSharing ? "#4caf50" : "#ccc" }}
            />
          </div>
          <Text style={{ color: "#888", fontSize: "0.85rem", marginTop: "0.5rem" }}>
            Helps us provide personalized insights by sharing anonymized health
            data.
          </Text>

          <Divider />

          {/* Activity Tracking */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Text
              style={{ fontWeight: "bold", color: "#333" }}
              id="activity-tracking-label"
            >
              Activity Tracking
            </Text>
            <Switch
              id="activity-tracking-switch"
              aria-label="Toggle Activity Tracking"
              checked={activityTracking}
              onChange={(checked) => handleToggle("activityTracking", checked)}
              checkedChildren="On"
              unCheckedChildren="Off"
              style={{ backgroundColor: activityTracking ? "#4caf50" : "#ccc" }}
            />
          </div>
          <Text style={{ color: "#888", fontSize: "0.85rem", marginTop: "0.5rem" }}>
            Enables automatic tracking of your steps, workouts, and sleep patterns.
          </Text>

          <Divider />

          {/* Location Access */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Text
              style={{ fontWeight: "bold", color: "#333" }}
              id="location-access-label"
            >
              Location Access
            </Text>
            <Switch
              id="location-access-switch"
              aria-label="Toggle Location Access"
              checked={locationAccess}
              onChange={(checked) => handleToggle("locationAccess", checked)}
              checkedChildren="On"
              unCheckedChildren="Off"
              style={{ backgroundColor: locationAccess ? "#4caf50" : "#ccc" }}
            />
          </div>
          <Text style={{ color: "#888", fontSize: "0.85rem", marginTop: "0.5rem" }}>
            Required for features like location-based health insights and activity
            maps.
          </Text>

          <Divider />

          <Tooltip title="Recommended for the best experience" placement="top">
            <Button
              id="save-settings-button"
              aria-label="Save Settings"
              type="primary"
              style={{
                width: "100%",
                marginTop: "1rem",
                backgroundColor: "#4caf50",
                border: "none",
              }}
              onClick={() => {
                alert("Settings saved successfully!");
                onClose();
              }}
            >
              Save Settings
            </Button>
          </Tooltip>
          <Button
            id="close-settings-btn"
            aria-label="Close Settings Card"
            onClick={() => {
              setVisible(false);
              onClose();
            }}
          >
            Close
          </Button>
        </Card>
      )}
    </>
  );
};

export default ComplexDataSettings;
