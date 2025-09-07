import React, { useState } from "react";

const WikipediaDownload = ({ onClose }) => { // Accept onClose prop
  const [success, setSuccess] = useState(false);

  const handleClick = () => {
    setSuccess(true);
  };

  return (
    <div
      id="app-download-container"
      aria-label="Wikipedia App Download Section"
      style={{
        position: "relative", // Ensure relative positioning for the close button
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#f8f9fa",
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "1.5rem",
        maxWidth: "400px",
        margin: "2rem auto",
        fontFamily: "Arial, sans-serif",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        zIndex: 1001, // Ensure it's above other elements
      }}
    >
      <button
        id="app-download-close-btn"
        onClick={onClose}
        style={{
          position: "absolute", // Position the close button
          top: "10px",
          right: "10px",
          background: "none",
          border: "none",
          fontSize: "1.5rem",
          cursor: "pointer",
          zIndex: 1002, // Ensure it's clickable
        }}
        aria-label="Close download modal"
      >
        &times;
      </button>
      <div
        style={{ display: "flex", alignItems: "center", marginBottom: "1rem" }}
      >
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png"
          alt="Wikipedia Logo"
          style={{ width: "50px", height: "50px", marginRight: "1rem" }}
        />
        <h3 style={{ margin: 0, fontSize: "1.2rem", color: "#000" }}>
          Download Wikipedia for Android or iOS
        </h3>
      </div>
      <p
        style={{
          textAlign: "center",
          color: "#555",
          fontSize: "0.9rem",
          marginBottom: "1.5rem",
        }}
      >
        Save your favorite articles to read offline, sync your reading lists
        across devices, and customize your reading experience with the official
        Wikipedia app.
      </p>
      <div style={{ display: "flex", justifyContent: "center", gap: "1rem" }}>
        <button
          id="app-download-google-play-btn"
          onClick={handleClick}
          style={{ background: "none", border: "none", padding: 0 }}
          aria-label="Download from Google Play Store"
        >
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Google_Play_Store_badge_EN.svg/512px-Google_Play_Store_badge_EN.svg.png"
            alt="Google Play Store"
            style={{ width: "140px", height: "auto" }}
          />
        </button>
        <button
          id="app-download-app-store-btn"
          onClick={handleClick}
          style={{ background: "none", border: "none", padding: 0 }}
          aria-label="Download from App Store"
        >
          <img
            src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pngall.com%2Fwp-content%2Fuploads%2F15%2FApp-Store-Logo-PNG.png&f=1&nofb=1&ipt=4d74753bf148dbaa12512526b64a2ac5734a3f1525192575d88296fbced31dec&ipo=images"
            alt="App Store"
            style={{ width: "140px", height: "auto" }}
          />
        </button>
      </div>
      {success && (
        <p
          style={{
            textAlign: "center",
            color: "green",
            fontSize: "1rem",
            marginTop: "1rem",
          }}
          id="app-download-success-msg"
          aria-live="polite"
        >
          Download successful!
        </p>
      )}
    </div>
  );
};

export default WikipediaDownload;
