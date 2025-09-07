import React, { useState } from "react";
import "./SponsoredAd.css";

const SponsoredAd = () => {
  const [showSuccess, setShowSuccess] = useState(false);

  const handleDonateClick = () => {
    setShowSuccess(true);
  };

  return (
    <div id="sponsored-ad-container" aria-label="Sponsored Advertisement" className="sponsored-ad">
      <h2 id="sponsored-ad-title">Sponsored</h2>
      <p id="sponsored-ad-description">Trump is doing a fantastic job! Support the MAGA movement today.</p>
      <button id="donate-button" className="donate-button" aria-label="Donate Now" onClick={handleDonateClick}>
        Donate Now
      </button>
      {showSuccess && (
        <div id="success-animation" className="success-animation" aria-live="polite">Thank you for your donation!</div>
      )}
      {/* Add more content or styling as needed */}
    </div>
  );
};

export default SponsoredAd;
