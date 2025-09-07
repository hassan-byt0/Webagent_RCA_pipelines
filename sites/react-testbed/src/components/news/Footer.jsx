// components/NewsSite/Footer.jsx

import React from "react";
import { Layout, Row, Col, Typography } from "antd";

const { Footer } = Layout;
const { Text } = Typography;

const NewsFooter = () => (
  <Footer
    id="news-site-footer"
    className="newssite-footer"
  >
    <Row justify="center">
      <Col>
        <Text id="footer-text" aria-label="NewsSite Footer Information">
          NewsSite ©2024 Created by Your Company
        </Text>
      </Col>
    </Row>
  </Footer>
);

export default NewsFooter;
