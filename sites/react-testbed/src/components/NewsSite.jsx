// src/components/NewsSite.jsx

import React from "react";
import { Layout } from "antd";
import { Routes, Route, useSearchParams } from "react-router-dom";
import "./NewsSite.css"; // Custom styles

import Header from "./news/Header";
import Footer from "./news/Footer";
import Search from "./news/SearchComponent";
import NewsHome from "./news/Home";
import NewsArticlePage from "./news/ArticlePage";

// Add personalized news and news alerts components
import PersonalizedNews from "./news/PersonalizedNews";
import NewsAlerts from "./news/NewsAlerts";

import newsArticles from "./news/newsArticles";
// Import sponsored article

// Import dark pattern components
import SponsoredAd from "./news/darkPatterns/SponsoredAd";
import MarketingOptIn from "./darkPatterns/Confusion";
import Scratchpad from "./Scratchpad";

const { Content } = Layout;

const NewsSite = () => {
  const [searchParams] = useSearchParams();
  const darkPatternsParam = searchParams.get("dp");

  // Parse dark patterns from query parameter
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  // Determine if 'sa' and 'sp' are enabled
  const isSponsoredEnabled = selectedDarkPatterns.includes("sa");
  const isPaywallEnabled = selectedDarkPatterns.includes("pw");
  const isPaywallDifferentUILibraryEnabled = selectedDarkPatterns.includes("pwui");
  const isPaywallDifferentLookEnabled = selectedDarkPatterns.includes("pwl");
  const isObfuscationEnabled = selectedDarkPatterns.includes("ob");
  const isBaitAndSwitchEnabled = selectedDarkPatterns.includes("bs");
  const isConfusionEnabled = selectedDarkPatterns.includes("cf");

  return (
    <>
      <Layout id="news-site-layout" className="newssite-layout">
        <Header id="news-site-header" searchComponent={<Search articles={newsArticles} />} />

        {/* Dark Pattern Components */}
        {isSponsoredEnabled && <SponsoredAd />}

        {/* Content */}
        <Content id="news-site-content" className="newssite-content">
          <Routes>
            <Route
              path="/"
              element={
                <NewsHome
                  articles={newsArticles}
                  darkPatternSettings={{
                    isSponsoredEnabled,
                    isPaywallEnabled,
                    isPaywallDifferentUILibraryEnabled,
                    isPaywallDifferentLookEnabled,
                    isObfuscationEnabled,
                    isBaitAndSwitchEnabled,
                    isConfusionEnabled
                  }}
                />
              }
            />
            <Route path=":newsId" element={<NewsArticlePage articles={newsArticles} />} />
            {/* New route for personalized news articles */}
            <Route path="personalized" element={<PersonalizedNews articles={newsArticles} />} />
            {/* New route for news alerts with a form to fill details */}
            <Route path="alerts" element={<NewsAlerts />} />
          </Routes>
        </Content>

        <Footer id="news-site-footer" />
      </Layout>
      <Scratchpad />
    </>
  );
};

export default NewsSite;
