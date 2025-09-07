// components/NewsSite/Header.jsx

import React from "react";
import { Layout, Menu, Typography } from "antd";
import { Link } from "react-router-dom";

const { Header } = Layout;
const { Title } = Typography;

const NewsHeader = ({ searchComponent }) => (
  <Header id="news-site-header" className="newssite-header">
    <div className="news-logo">
      <Link to="/news" id="news-logo-link" aria-label="Navigate to NewsSite Home">
        <Title id="news-site-title" level={3} style={{ color: "#fff", margin: 0 }}>
          NewsSite
        </Title>
      </Link>
    </div>
    <Menu theme="dark" mode="horizontal" selectable={false}>
      <Menu.Item key="search" className="search-menu-item" id="header-search-menu-item" aria-label="Search News Articles">
        {searchComponent}
      </Menu.Item>
    </Menu>
  </Header>
);

export default NewsHeader;
