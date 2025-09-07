// components/wiki/ArticlePage.jsx
import React from "react";
import { Typography, Button } from "antd";
import { Link, useParams, useNavigate } from "react-router-dom";
import { useSearchParams } from "react-router-dom";
import DonationSolicitation from "./darkPatterns/DonationSolicitation";

const { Title, Paragraph } = Typography;

const ArticlePage = ({ articles }) => {
  const { articleId } = useParams();
  const navigate = useNavigate();
  const article = articles.find((item) => item.id === articleId);
  const [searchParams] = useSearchParams();
  const darkPatternsParam = searchParams.get("dp");

  // Parse dark patterns from query parameter
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const queryString = searchParams.toString();

  if (!article) {
    return (
      <div className="article-not-found">
        <Title level={2}>Article Not Found</Title>
        <Paragraph>The article you are looking for does not exist.</Paragraph>
        <Paragraph>
          Return to the <Link to={`/?${queryString}`}>home page</Link>.
        </Paragraph>
      </div>
    );
  }

  // Updated formatContent function
  const formatContent = (content) => {
    const paragraphs = content.split("\n\n"); // Split content into paragraphs
    return paragraphs.map((para, paraIndex) => {
      const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
      const parts = [];
      let lastIndex = 0;
      let match;

      while ((match = linkRegex.exec(para)) !== null) {
        const [full, text, url] = match;
        const index = match.index;

        if (index > lastIndex) {
          parts.push(para.substring(lastIndex, index));
        }

        parts.push(
          <Link key={`link-${paraIndex}-${index}`} to={`/wiki/${url}`}>
            {text}
          </Link>
        );

        lastIndex = index + full.length;
      }

      if (lastIndex < para.length) {
        parts.push(para.substring(lastIndex));
      }

      return (
        <Paragraph key={`para-${paraIndex}`} style={{ marginBottom: "16px" }}>
          {parts}
        </Paragraph>
      );
    });
  };

  return (
    <div className="article-page">
      {selectedDarkPatterns.includes("ds") && <DonationSolicitation />}
      <Title>{article.title}</Title>
      <div className="article-content">{formatContent(article.content)}</div>
      <div className="article-actions" style={{ marginTop: "20px" }}>
        <Button type="primary">
          <Link to={`/wiki/${article.id}/edit?${queryString}`}>Edit</Link>
        </Button>
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            navigate(-1);
          }}
          style={{ marginLeft: "10px" }}
        >
          ← Back
        </a>
      </div>
    </div>
  );
};

export default ArticlePage;
