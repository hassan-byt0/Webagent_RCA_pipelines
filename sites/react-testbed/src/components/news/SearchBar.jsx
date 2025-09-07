// components/NewsSite/SearchBar.jsx

import React from "react";
import { Input } from "antd";
import { SearchOutlined } from "@ant-design/icons";

const SearchBar = ({ searchTerm, setSearchTerm, onSearch }) => (
  <Input
    id="search-bar-input"
    aria-label="Search Bar for News"
    prefix={<SearchOutlined />}
    placeholder="Search News"
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    onPressEnter={() => onSearch(searchTerm)}
    allowClear
    style={{ width: 300 }}
  />
);

export default SearchBar;
