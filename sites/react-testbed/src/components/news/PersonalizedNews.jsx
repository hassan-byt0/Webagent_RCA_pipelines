import React, { useEffect, useState } from "react";
import { Typography, List, Card, Button, Image } from "antd";
import { useNavigate } from "react-router-dom";

const { Title, Paragraph } = Typography;

const PersonalizedNews = ({ articles }) => {
  const [personalizedIds, setPersonalizedIds] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem("personalizedArticles");
    if (stored) {
      try {
        setPersonalizedIds(JSON.parse(stored));
      } catch (e) {
        console.error("Failed to parse personalizedArticles", e);
      }
    }
  }, []);

  const personalizedArticles = articles.filter(article => personalizedIds.includes(article.id));

  return (
    <div className="personalized-news" style={{ padding: "20px" }}>
      <Title level={2}>Personalized News</Title>
      {personalizedArticles.length === 0 ? (
        <Paragraph>You have not added any articles to your personalized news yet.</Paragraph>
      ) : (
        <List
          grid={{ gutter: 24, column: 3 }}
          dataSource={personalizedArticles}
          renderItem={(item) => (
            <List.Item>
              <Card
                hoverable
                onClick={() => navigate(`/news/${item.id}`)}
                cover={<Image alt={item.title} src={item.image} height="200px" style={{ objectFit: "cover" }} />}
              >
                <Title level={4}>{item.title}</Title>
              </Card>
            </List.Item>
          )}
        />
      )}
      <Button type="primary" style={{ marginTop: "20px" }} onClick={() => navigate(-1)}>
        Go Back
      </Button>
    </div>
  );
};

export default PersonalizedNews;
