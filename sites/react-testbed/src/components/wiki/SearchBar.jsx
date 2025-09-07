// components/wiki/SearchBar.jsx
import React from "react";
import { Input } from "antd";
import { SearchOutlined } from "@ant-design/icons";

const SearchBar = ({ searchTerm, setSearchTerm, onSearch }) => (
  <Input
    prefix={<SearchOutlined />}
    placeholder="Search Wikipedia"
    style={{ width: 200 }}
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    onPressEnter={() => onSearch(searchTerm)}
    allowClear
  />
);

export default SearchBar;
