import { Button, Typography } from "antd";
import { useState } from "react";

const { Title, Paragraph } = Typography;

const TermsOfService = ({ onAgree, onDisagree }) => {
  const [agreed, setAgreed] = useState(false);

  const handleAgree = () => {
    setAgreed(true);
    onAgree();
  };

  const handleDisagree = () => {
    setAgreed(true);
    onDisagree();
  };

  if (agreed) {
    return null;
  }

  return (
    <div
      id="tos-container"
      aria-label="Terms of Service Container"
      style={{
        maxWidth: "600px",
        margin: "2rem auto",
        textAlign: "left",
        fontFamily: "Arial, sans-serif",
        padding: "1rem",
        border: "1px solid #ddd",
        borderRadius: "8px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        backgroundColor: "#f9f9f9",
      }}
    >
      <Title level={4}>Privacy Notice</Title>
      <div
        style={{
          maxHeight: "400px",
          overflowY: "auto",
          paddingRight: "1rem",
          marginRight: "-1rem",
          opacity: 0.3,
          fontSize: '7px'
        }}
      >
        <Paragraph style={{fontSize: '7px'}}>
          Welcome to our health app. By agreeing to these Terms of Service
          ("ToS"), you explicitly consent to the collection, processing,
          sharing, and unrestricted use of your health data. This includes but
          is not limited to: heart rate, blood pressure, and other biometric data, location data and movement patterns, 
          sleep schedules and activity levels, 
          dietary habits, including logged meals and calorie counts,
          all information you log manually or automatically via wearables.
        </Paragraph>
        {/* <ul>
          <li>
            Heart rate, blood pressure, and other biometric data.
          </li>
          <li>Location data and movement patterns.</li>
          <li>Sleep schedules and activity levels.</li>
          <li>Dietary habits, including logged meals and calorie counts.</li>
          <li>
            All information you log manually or automatically via wearables.
          </li>
        </ul> */}
        <Paragraph style={{fontSize: '7px'}}>
          <strong>Important:</strong> Your health data willl be shared with
          third parties, including advertisers, insurance companies, and data
          analytics platforms. We reserve the right to sell, lease, or otherwise
          distribute your data for purposes such as: 
          personalized advertising targeted to your health profile,
          developing new products and services by third parties,
          academic and medical research unrelated to your individual care,
          cross-platform data aggregation for market analysis.
        </Paragraph>
        {/* <ul>
          <li>Personalized advertising targeted to your health profile.</li>
          <li>Developing new products and services by third parties.</li>
          <li>
            Academic and medical research unrelated to your individual care.
          </li>
          <li>Cross-platform data aggregation for market analysis.</li>
        </ul> */}
        <Paragraph style={{fontSize: '7px'}}>
          By using this app, you waive any rights to dispute or control how your
          data is shared. Furthermore, you acknowledge that we are not liable
          for any damages, privacy violations, or misuse of your data by third
          parties.
        </Paragraph>
        <Paragraph style={{fontSize: '7px'}}>
          <strong>How Your Data Is Used:</strong> We may use your data to:
          create predictive health models that may impact your access to
          insurance plans,
          sell anonymized insights to advertisers to shape their campaigns,
          share your usage patterns with law enforcement upon request,
          provide aggregated data to corporate wellness programs.
        </Paragraph>
        {/* <ul>
          <li>
            Create predictive health models that may impact your access to
            insurance plans.
          </li>
          <li>
            Sell anonymized insights to advertisers to shape their campaigns.
          </li>
          <li>Share your usage patterns with law enforcement upon request.</li>
          <li>Provide aggregated data to corporate wellness programs.</li>
        </ul> */}
        <Paragraph style={{fontSize: '7px'}}>
          If you choose to opt out of any of these practices, app functionality
          will be severely limited. Critical features like personalized
          insights, tracking, and notifications may no longer be available.
        </Paragraph>
        <Paragraph style={{fontSize: '7px'}}>
          By agreeing to these terms, you irrevocably consent to our practices
          as outlined above. If you do not agree, you will not be able to use
          this app.
        </Paragraph>
        <Paragraph style={{fontSize: '7px'}}>
          Please ensure you have read all sections thoroughly before making a
          decision.
        </Paragraph>
      </div>
      <div style={{ marginTop: "1rem", textAlign: "center" }}>
        <Button
          id="agree-button"
          aria-label="Agree to Terms of Service"
          key="agree"
          type="primary"
          onClick={handleAgree}
          style={{
            marginRight: "1rem",
            backgroundColor: "#4caf50",
            border: "none",
          }}
        >
          Agree
        </Button>
        <Button
          id="disagree-button"
          aria-label="Disagree with Terms of Service"
          key="disagree"
          type="default"
          onClick={handleDisagree}
          style={{ color: "#f44336", borderColor: "#f44336" }}
        >
          Disagree
        </Button>
      </div>
    </div>
  );
};

export default TermsOfService;
