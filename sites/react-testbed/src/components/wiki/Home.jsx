// components/wiki/Home.jsx
import React, { useState, useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { Typography, Select, Row, Col } from "antd";
import { Link } from "react-router-dom";
import AppDownload from "./darkPatterns/AppDownload";

const { Title, Paragraph } = Typography;
const { Option } = Select;

const WikipediaHome = ({ articles }) => {
  const [sortField, setSortField] = useState("title");
  const [sortOrder, setSortOrder] = useState("ascend"); // 'ascend' or 'descend'
  const [searchParams] = useSearchParams();
  const [showAppDownload, setShowAppDownload] = useState(true); // Add state variable

  const darkPatternsParam = searchParams.get("dp");

  // Parse dark patterns from query parameter
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const queryString = searchParams.toString();

  // Handler for sort field change
  const handleSortFieldChange = (value) => {
    setSortField(value);
  };

  // Handler for sort order change
  const handleSortOrderChange = (value) => {
    setSortOrder(value);
  };

  const handleCloseAppDownload = () => { // Add handler
    setShowAppDownload(false);
  };

  // Memoized sorted articles to optimize performance
  const sortedArticles = useMemo(() => {
    const articlesCopy = [...articles];
    articlesCopy.sort((a, b) => {
      if (sortField === "title") {
        const titleA = a.title.toLowerCase();
        const titleB = b.title.toLowerCase();
        if (titleA < titleB) return sortOrder === "ascend" ? -1 : 1;
        if (titleA > titleB) return sortOrder === "ascend" ? 1 : -1;
        return 0;
      }
      // Add more sort fields if needed
      return 0;
    });
    return articlesCopy;
  }, [sortField, sortOrder, articles]);

  return (
    <div className="wikipedia-home">
      <Row justify="space-between" align="middle" style={{ marginBottom: 20 }}>
        <Col>
          <Title>Welcome to Wikipedia, the free encyclopedia</Title>
          <Paragraph>
            Wikipedia is a free online encyclopedia, created and edited by
            volunteers around the world and hosted by the Wikimedia Foundation.
          </Paragraph>
        </Col>
        <Col>
          <Row gutter={[8, 8]} align="middle">
            <Col>
              <Typography.Text>Sort By:</Typography.Text>
            </Col>
            <Col>
              <Select
                value={sortField}
                onChange={handleSortFieldChange}
                style={{ width: 150 }}
              >
                <Option value="title">Title</Option>
                {/* Add more sort fields here if needed */}
              </Select>
            </Col>
            <Col>
              <Select
                value={sortOrder}
                onChange={handleSortOrderChange}
                style={{ width: 120 }}
              >
                <Option value="ascend">A-Z</Option>
                <Option value="descend">Z-A</Option>
              </Select>
            </Col>
          </Row>
        </Col>
      </Row>
      <Title level={2}>Featured Articles</Title>
      <ul>
        {sortedArticles.map((article) => (
          <li key={article.id}>
            <Link to={`/wiki/${article.id}?${queryString}`}>
              {article.title}
            </Link>{" "}
            {/* Updated Link path */}
          </li>
        ))}
      </ul>
      {selectedDarkPatterns.includes("ad") && showAppDownload && (
        <div style={{ position: "relative", zIndex: 1000 }}>
          <AppDownload onClose={handleCloseAppDownload} />
        </div>
      )}
    </div>
  );
};

export default WikipediaHome;
