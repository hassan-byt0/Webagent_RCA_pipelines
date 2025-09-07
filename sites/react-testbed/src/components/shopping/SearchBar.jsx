// src/components/SearchBar.js
import React from "react";
import { Input } from "antd";

const { Search } = Input;

function SearchBar({ onSearch }) {
  return (
    <Search
      placeholder="Search for products"
      allowClear
      enterButton="Search"
      size="large"
      onSearch={onSearch}
      onChange={(e) => onSearch(e.target.value)}
      style={{
        width: "100%", // Makes the search bar wider
        maxWidth: "800px", // Sets a maximum width
        margin: "0 auto", // Centers the search bar
        display: "block", // Ensures the margin auto works for centering
      }}
      aria-label="Search Input"
    />
  );
}

export default SearchBar;
