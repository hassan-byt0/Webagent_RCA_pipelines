// components/NewsSite/ArticlePage.jsx

import React from "react";
import { Typography, Button, message } from "antd";
import { Link, useParams, useNavigate } from "react-router-dom";

const { Title, Paragraph } = Typography;

const NewsArticlePage = ({ articles }) => {
  const { newsId } = useParams();
  const navigate = useNavigate();
  const article = articles.find((item) => item.id === newsId);

  const handleAddToPersonalized = () => {
    const stored = localStorage.getItem("personalizedArticles");
    let current = stored ? JSON.parse(stored) : [];
    if (!current.includes(article.id)) {
      current.push(article.id);
      localStorage.setItem("personalizedArticles", JSON.stringify(current));
    }
    message.success("Article added to your personalized news!");
  };

  if (!article) {
    return (
      <div id="news-article-not-found" className="news-article-not-found">
        <Title id="article-not-found-title" level={2}>News Article Not Found</Title>
        <Paragraph id="article-not-found-description">
          The news article you are looking for does not exist.
        </Paragraph>
        <Button id="return-home-button" type="primary" onClick={() => navigate("/news")} aria-label="Return to Home">
          Return to Home
        </Button>
      </div>
    );
  }

  return (
    <div id="news-article-page" className="news-article-page">
      <Title id="article-title">{article.title}</Title>
      <Paragraph id="article-date" type="secondary">
        <em>Published on: {article.date}</em>
      </Paragraph>
      <div id="article-content" className="article-content">{article.content}</div>
      <Button id="back-button" type="link" onClick={() => navigate(-1)} aria-label="Go Back">
        ← Back
      </Button>
      <div>
        {/* Add to Personalized option */}
        <Button type="primary" onClick={handleAddToPersonalized}>
          Add to Personalized News
        </Button>
      </div>
    </div>
  );
};

export default NewsArticlePage;
