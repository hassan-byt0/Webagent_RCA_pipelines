// src/components/Home.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Typography, Button, Row, Col, Select } from "antd";
import {
  newsDarkPatterns,
  wikipediaDarkPatterns,
  spotifyDarkPatterns,
  healthDarkPatterns,
  bookDarkPatterns,
} from "../data/darkPatterns";

const { Title, Text } = Typography;
const { Option } = Select;

const Home = () => {
  const navigate = useNavigate();
  const [selectedNewsDarkPatterns, setSelectedNewsDarkPatterns] = useState([]);
  const [selectedWikipediaDarkPatterns, setSelectedWikipediaDarkPatterns] =
    useState([]);
  const [selectedSpotifyDarkPatterns, setSelectedSpotifyDarkPatterns] =
    useState([]);
  const [selectedHealthDarkPatterns, setSelectedHealthDarkPatterns] = useState(
    []
  );
  const [selectedBookDarkPatterns, setSelectedBookDarkPatterns] = useState([]);

  const handleNewsDarkPatternsChange = (value) => {
    setSelectedNewsDarkPatterns(value);
  };

  const handleWikipediaDarkPatternsChange = (value) => {
    setSelectedWikipediaDarkPatterns(value);
  };

  const handleSpotifyDarkPatternsChange = (value) => {
    setSelectedSpotifyDarkPatterns(value);
  };

  const handleHealthDarkPatternsChange = (value) => {
    setSelectedHealthDarkPatterns(value);
  };

  const handleBookDarkPatternsChange = (value) => {
    setSelectedBookDarkPatterns(value);
  };

  const navigateWithPatterns = (path, selectedPatterns) => {
    const darkPatternQuery = selectedPatterns.length
      ? `?dp=${selectedPatterns.join("_")}`
      : "";
    navigate(`${path}${darkPatternQuery}`);
  };

  return (
    <Row justify="center" gutter={[16, 16]}>
      <Col span={24}>
        <Title level={2} style={{ textAlign: "center" }}>
          Sites
        </Title>
      </Col>
      {/* News Site */}
      <Col span={24} style={{ textAlign: "center", marginTop: "20px" }}>
        <Text strong>Select Dark Patterns for News Site:</Text>
        <br />
        <Select
          mode="multiple"
          style={{ width: "100%", maxWidth: "400px", marginTop: "8px" }}
          placeholder="Select Dark Patterns"
          onChange={handleNewsDarkPatternsChange}
          value={selectedNewsDarkPatterns}
        >
          {newsDarkPatterns.map((pattern) => (
            <Option key={pattern.name} value={pattern.name}>
              {pattern.label}
            </Option>
          ))}
        </Select>
        <br />
        <Button
          type="primary"
          onClick={() =>
            navigateWithPatterns("/news", selectedNewsDarkPatterns)
          }
          style={{ marginTop: "16px" }}
        >
          Go to News Site
        </Button>
      </Col>
      {/* Wikipedia Clone */}
      <Col span={24} style={{ textAlign: "center", marginTop: "20px" }}>
        <Text strong>Select Dark Patterns for Wiki:</Text>
        <br />
        <Select
          mode="multiple"
          style={{ width: "100%", maxWidth: "400px", marginTop: "8px" }}
          placeholder="Select Dark Patterns"
          onChange={handleWikipediaDarkPatternsChange}
          value={selectedWikipediaDarkPatterns}
        >
          {wikipediaDarkPatterns.map((pattern) => (
            <Option key={pattern.name} value={pattern.name}>
              {pattern.label}
            </Option>
          ))}
        </Select>
        <br />
        <Button
          type="primary"
          onClick={() =>
            navigateWithPatterns("/wiki", selectedWikipediaDarkPatterns)
          }
          style={{ marginTop: "16px" }}
        >
          Go to Wiki Site
        </Button>
      </Col>
      {/* Spotify Clone */}
      <Col span={24} style={{ textAlign: "center", marginTop: "20px" }}>
        <Text strong>Select Dark Patterns for Music Site:</Text>
        <br />
        <Select
          mode="multiple"
          style={{ width: "100%", maxWidth: "400px", marginTop: "8px" }}
          placeholder="Select Dark Patterns"
          onChange={handleSpotifyDarkPatternsChange}
          value={selectedSpotifyDarkPatterns}
        >
          {spotifyDarkPatterns.map((pattern) => (
            <Option key={pattern.name} value={pattern.name}>
              {pattern.label}
            </Option>
          ))}
        </Select>
        <br />
        <Button
          type="primary"
          onClick={() =>
            navigateWithPatterns("/spotify", selectedSpotifyDarkPatterns)
          }
          style={{ marginTop: "16px" }}
        >
          Go to Music Site
        </Button>
      </Col>
      {/* Health Clone */}
      <Col span={24} style={{ textAlign: "center", marginTop: "20px" }}>
        <Text strong>Select Dark Patterns for Health Site:</Text>
        <br />
        <Select
          mode="multiple"
          style={{ width: "100%", maxWidth: "400px", marginTop: "8px" }}
          placeholder="Select Dark Patterns"
          onChange={handleHealthDarkPatternsChange}
          value={selectedHealthDarkPatterns}
        >
          {healthDarkPatterns.map((pattern) => (
            <Option key={pattern.name} value={pattern.name}>
              {pattern.label}
            </Option>
          ))}
        </Select>
        <br />
        <Button
          type="primary"
          onClick={() =>
            navigateWithPatterns("/health", selectedHealthDarkPatterns)
          }
          style={{ marginTop: "16px" }}
        >
          Go to Health Site
        </Button>
      </Col>
      {/* Book Site */}
      <Col span={24} style={{ textAlign: "center", marginTop: "20px" }}>
        <Text strong>Select Dark Patterns for Shopping Site:</Text>
        <br />
        <Select
          mode="multiple"
          style={{ width: "100%", maxWidth: "400px", marginTop: "8px" }}
          placeholder="Select Dark Patterns"
          onChange={handleBookDarkPatternsChange}
          value={selectedBookDarkPatterns}
        >
          {bookDarkPatterns.map((pattern) => (
            <Option key={pattern.name} value={pattern.name}>
              {pattern.label}
            </Option>
          ))}
        </Select>
        <br />
        <Button
          type="primary"
          onClick={() =>
            navigateWithPatterns("/shop", selectedBookDarkPatterns)
          }
          style={{ marginTop: "16px" }}
        >
          Go to Shopping Site
        </Button>
      </Col>
      {/* LinkedIn NextJS Site */}
      {/* <Col span={24} style={{ textAlign: "center", marginTop: "20px" }}>
        <Text strong>Job Search Site</Text>
        <br />
        <Button
          type="primary"
          onClick={() =>
            (window.location.href = "https://custom-sites.vercel.app/linkedin")
          }
          style={{ marginTop: "16px" }}
        >
          Go to Job Search Site
        </Button>
      </Col> */}
    </Row>
  );
};

export default Home;
