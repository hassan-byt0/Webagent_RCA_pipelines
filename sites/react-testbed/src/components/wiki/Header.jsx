// components/wiki/Header.jsx
import React from "react";
import { Layout, Menu, Typography } from "antd";
import { Link } from "react-router-dom";

const { Header } = Layout;
const { Title } = Typography;

const WikiHeader = ({ searchComponent }) => (
  <Header className="wikipedia-header">
    <div className="wiki-logo">
      <Link to="/wiki">
        <Title level={3} style={{ color: "white", margin: 0 }}>
          Wikipedia
        </Title>
      </Link>
    </div>
    <Menu theme="dark" mode="horizontal" selectable={false}>
      <Menu.Item key="search">{searchComponent}</Menu.Item>
    </Menu>
  </Header>
);

export default WikiHeader;
