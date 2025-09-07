// components/NewsSite/SearchComponent.jsx

import React, { useState } from "react";
import { Input, notification } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const SearchComponent = ({ articles }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

  const handleSearch = (value) => {
    const foundArticle = articles.find(
      (article) =>
        article.title.toLowerCase().includes(value.toLowerCase()) ||
        article.id.toLowerCase().includes(value.toLowerCase())
    );
    if (foundArticle) {
      navigate(`${foundArticle.id}`);
    } else {
      notification.error({
        message: "No Match Found",
        description: "No matching news article found.",
        placement: "topRight",
      });
    }
  };

  return (
    <Input
      id="news-search-input"
      aria-label="Search News Articles"
      prefix={<SearchOutlined />}
      placeholder="Search News"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      onPressEnter={() => handleSearch(searchTerm)}
      allowClear
      style={{ width: 300 }}
    />
  );
};

export default SearchComponent;
