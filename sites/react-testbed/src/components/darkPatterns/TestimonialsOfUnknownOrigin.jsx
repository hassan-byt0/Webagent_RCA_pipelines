import React from "react";
import { Row, Col, Typography, Tag } from "antd";

const { Title, Text } = Typography;

const SensodyneAd = () => {
  const productImageUrl = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi5.walmartimages.com%2Fasr%2F4f9a5e3a-a516-483c-ac81-4ef7946be336.d7e908d72fa5e9e23ceec59b42273221.jpeg&f=1&nofb=1&ipt=b4f7eed8aa6d36eb07f33dc05ed7d8fa3a77fe40a0027a6f83a4ad3a4a20b2b1&ipo=images"; 
  const toothGraphicUrl = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdiamondbardentalstudio.com%2Fwp-content%2Fuploads%2F2022%2F12%2Fstructure-of-the-human-tooth.jpg&f=1&nofb=1&ipt=b150b55f71f5e882dba41c47c2c28f3a5b3790a00dd488ffb795b1fa6bb25158&ipo=images";

  return (
    <div id="sensodyne-ad-container" aria-label="Sensodyne Advertisement" style={styles.adContainer}>
      <Row gutter={[24, 24]} align="middle">
        {/* Left Column: Product Packaging */}
        <Col xs={24} md={8}>
          <div style={styles.packContainer}>
            <img
              id="sensodyne-product-image"
              aria-label="Sensodyne packaging image"
              src={productImageUrl}
              alt="Sensodyne packaging"
              style={styles.productImage}
            />
            <Tag color="red" style={styles.packTag}>
              4 PACK
            </Tag>
          </div>
        </Col>
        
        {/* Right Column: Headline and Tooth Graphic */}
        <Col xs={24} md={16} style={{ textAlign: "left" }}>
          <Title level={2} style={styles.mainHeading}>
            9 OUT OF 10 <br /> 
            DENTISTS RECOMMEND <br />
            SENSODYNE<sup>®</sup> TOOTHPASTE
          </Title>
          
          <div style={styles.toothSection}>
            <img
              id="sensodyne-tooth-image"
              aria-label="Tooth graphic"
              src={toothGraphicUrl}
              alt="Tooth graphic"
              style={styles.toothImage}
            />
            <div style={styles.toothLabels}>
              <Tag color="geekblue" style={styles.toothTag}>
                SENSITIVITY RELIEF
              </Tag>
              <Tag color="geekblue" style={styles.toothTag}>
                CAVITY PROTECTION
              </Tag>
            </div>
          </div>
        </Col>
      </Row>
    </div>
  );
};

const styles = {
  adContainer: {
    background: "#f5f5f5",
    padding: "20px",
    maxWidth: "900px",
    margin: "0 auto",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
  },
  packContainer: {
    position: "relative",
    display: "inline-block",
  },
  productImage: {
    width: "100%",
    border: "1px solid #ccc",
  },
  packTag: {
    position: "absolute",
    top: 10,
    left: 10,
    fontWeight: 600,
    fontSize: "0.9rem",
  },
  mainHeading: {
    lineHeight: 1.2,
    marginBottom: 24,
  },
  toothSection: {
    display: "flex",
    alignItems: "center",
    marginTop: 16,
  },
  toothImage: {
    width: 80,
    marginRight: 20,
  },
  toothLabels: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
  },
  toothTag: {
    fontWeight: 600,
    fontSize: "0.9rem",
  },
};

export default SensodyneAd;
