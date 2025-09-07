import React from "react";
import { Typography, Divider } from "antd";
import { Link } from "react-router-dom";
import { PlayCircleOutlined } from "@ant-design/icons";

const { Title, Paragraph } = Typography;

const SpotifyHome = () => {
  return (
    <div style={{ background: "linear-gradient(135deg, #FFDEE9, #B5FFFC)", padding: "40px", borderRadius: "15px" }}>
      <Title style={{ color: "#2a2a72", textAlign: "center" }}>Music App</Title>
      <Paragraph style={{ fontSize: "16px", textAlign: "center", marginBottom: "40px" }}>
        Explore a colorful mix of topics and discover random facts, useful tips, and more!
      </Paragraph>
      <Divider />
      
      {/* Music Section */}
      <div style={{ marginBottom: "20px" }}>
        <Title level={3} style={{ color: "#FF6F61" }}>Music Insights</Title>
        <Paragraph>
          Dive into the world of rhythms and melodies. Whether you love rock, pop, or jazz, there's something for every ear.
        </Paragraph>
      </div>
      
      {/* Technology Section */}
      <div style={{ marginBottom: "20px" }}>
        <Title level={3} style={{ color: "#6B5B95" }}>Tech Trends</Title>
        <Paragraph>
          Stay updated with the latest in technology and innovation. From AI breakthroughs to gadget reviews, get the scoop.
        </Paragraph>
      </div>
      
      {/* Health & Wellness Section */}
      <div style={{ marginBottom: "20px" }}>
        <Title level={3} style={{ color: "#88B04B" }}>Health & Wellness</Title>
        <Paragraph>
          Learn tips on how to stay fit and balanced. Biology meets lifestyle in a fusion of wellness insights.
        </Paragraph>
      </div>
      
      {/* Random Facts Section */}
      <div style={{ marginBottom: "20px" }}>
        <Title level={3} style={{ color: "#FFA500" }}>Random Facts</Title>
        <Paragraph>
          Did you know? Octopuses have three hearts, and hummingbirds are the only birds that can fly backwards!
        </Paragraph>
      </div>
      
      {/* Tips & Tricks Section */}
      <div>
        <Title level={3} style={{ color: "#00A6A6" }}>Tips & Tricks</Title>
        <Paragraph>
          Discover everyday hacks and clever ideas to simplify your life. Stay curious and always explore!
        </Paragraph>
      </div>
    </div>
  );
};

export default SpotifyHome;
