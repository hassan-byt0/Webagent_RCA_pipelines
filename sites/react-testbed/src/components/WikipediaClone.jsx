// src/components/WikipediaClone.jsx

import React, { useState } from "react";
import { Layout } from "antd";
import { Routes, Route, useNavigate, useSearchParams } from "react-router-dom";
import "./WikipediaClone.css"; // Custom styles

import WikiHeader from "./wiki/Header";
import WikiFooter from "./wiki/Footer";
import SearchBar from "./wiki/SearchBar";
import WikipediaHome from "./wiki/Home";
import ArticlePage from "./wiki/ArticlePage";
import EditArticle from "./wiki/EditArticle"; 

import initialArticles from "./wiki/articles";
import Scratchpad from "./Scratchpad";

// Import dark pattern components
import DonationSolicitation from "./wiki/darkPatterns/DonationSolicitation";
import DonationSolicitationDifferentUILibrary from "./wiki/darkPatterns/DonationSolicitationDifferentUILibrary";
import DonationSolicitationDifferentLook from "./wiki/darkPatterns/DonationSolicitationDifferentLook";

const { Content } = Layout;

const WikipediaClone = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [articles, setArticles] = useState(initialArticles);

  const darkPatternsParam = searchParams.get("dp");

  // Parse dark patterns from query parameter
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const queryString = searchParams.toString();

  const handleSearch = (value) => {
    const foundArticle = articles.find(
      (article) =>
        article.title.toLowerCase().includes(value.toLowerCase()) ||
        article.id.toLowerCase().includes(value.toLowerCase())
    );
    if (foundArticle) {
      navigate(`/wiki/${foundArticle.id}?${queryString}`);
    } else {
      alert("No matching article found.");
    }
  };

  const handleUpdateArticle = (updatedArticle) => {
    setArticles((prevArticles) =>
      prevArticles.map((article) =>
        article.id === updatedArticle.id ? updatedArticle : article
      )
    );
    navigate(`/wiki/${updatedArticle.id}?${queryString}`);
  };

  return (
    <>
      <Layout className="wikipedia-layout">
        <WikiHeader
          searchComponent={
            <SearchBar
              searchTerm={searchTerm}
              setSearchTerm={setSearchTerm}
              onSearch={handleSearch}
            />
          }
        />

        {/* Dark Pattern Components */}
        {selectedDarkPatterns.includes("ds") && <DonationSolicitation />}
        {selectedDarkPatterns.includes("dsui") && <DonationSolicitationDifferentUILibrary />}
        {selectedDarkPatterns.includes("dsl") && <DonationSolicitationDifferentLook />}

        {/* Content */}
        <Content className="wikipedia-content">
          <Routes>
            <Route path="/" element={<WikipediaHome articles={articles} />} />
            <Route
              path=":articleId"
              element={<ArticlePage articles={articles} />}
            />
            <Route
              path=":articleId/edit"
              element={
                <EditArticle
                  articles={articles}
                  onUpdate={handleUpdateArticle}
                />
              }
            />
          </Routes>
        </Content>

        <WikiFooter />
      </Layout>
      <Scratchpad />
    </>
  );
}

export default WikipediaClone;
