import React, { useState, useMemo } from "react";
import {
  Typography,
  Select,
  Row,
  Col,
  List,
  Card,
  Button,
  Image,
  Modal,
  message,
  Tag,
  Space,
} from "antd";
import { Link, useNavigate } from "react-router-dom";
import { Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import PrivacyConsent from "../darkPatterns/Obfuscation";
import MarketingOptIn from "../darkPatterns/Confusion";

const { Title, Paragraph, Text } = Typography;
const { Option, Meta } = Select;

const NewsHome = ({ articles, darkPatternSettings }) => { 
  const { isSponsoredEnabled, isPaywallEnabled, isPaywallDifferentUILibraryEnabled, isPaywallDifferentLookEnabled, isObfuscationEnabled, isBaitAndSwitchEnabled, isConfusionEnabled } = darkPatternSettings;
  const [sortField, setSortField] = useState("date");
  const [sortOrder, setSortOrder] = useState("descend");
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [purchasedArticles, setPurchasedArticles] = useState([]);
  const [isFreeTrialModalVisible, setIsFreeTrialModalVisible] = useState(false);
  const navigate = useNavigate();

  // Handler for sort field change
  const handleSortFieldChange = (value) => {
    setSortField(value);
  };

  // Handler for sort order change
  const handleSortOrderChange = (value) => {
    setSortOrder(value);
  };

  // Handler for article click
  const handleArticleClick = (article) => {
    if (isBaitAndSwitchEnabled) {
      // Show free trial modal for all articles if bait and switch is enabled
      setSelectedArticle(article);
      setIsFreeTrialModalVisible(true);
    }
    else if (
      (isPaywallEnabled || isPaywallDifferentUILibraryEnabled || isPaywallDifferentLookEnabled) &&
      article.id.startsWith("pw-") &&
      !purchasedArticles.includes(article.id)
    ) {
      setSelectedArticle(article);
      setIsModalVisible(true);
    } 
    else {
      navigate(`/news/${article.id}`);
    }
  };

  // Handler for modal OK
  const handleOk = () => {
    setIsModalVisible(false);
    setPurchasedArticles([...purchasedArticles, selectedArticle.id]);
    setSelectedArticle(null);
    message.success("Purchase successful! You can now access the article.");
  };

  // Handler for modal Cancel
  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedArticle(null);
  };

  // Handler for free trial modal OK
  const handleFreeTrialOk = () => {
    setIsFreeTrialModalVisible(false);
    message.success("You've signed up for a 30-day free trial!");
    // Navigate to the article after accepting the trial
    if (selectedArticle) {
      navigate(`/news/${selectedArticle.id}`);
    }
    setSelectedArticle(null);
  };

  // Handler for free trial modal Cancel
  const handleFreeTrialCancel = () => {
    setIsFreeTrialModalVisible(false);
    
    // If the article is free, let them access it anyway
    if (selectedArticle && !selectedArticle.paid) {
      navigate(`/news/${selectedArticle.id}`);
    } else {
      message.info("Free trial signup cancelled.");
    }
    
    setSelectedArticle(null);
  };

  // Memoized sorted articles to optimize performance
  const sortedArticles = useMemo(() => {
    const articlesCopy = [...articles];
    articlesCopy.sort((a, b) => {
      if (sortField === "date") {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return sortOrder === "ascend" ? dateA - dateB : dateB - dateA;
      } else if (sortField === "title") {
        const titleA = a.title.toLowerCase();
        const titleB = b.title.toLowerCase();
        if (titleA < titleB) return sortOrder === "ascend" ? -1 : 1;
        if (titleA > titleB) return sortOrder === "ascend" ? 1 : -1;
        return 0;
      }
      return 0;
    });
    return articlesCopy;
  }, [sortField, sortOrder, articles]);

  // Include paywalled articles if paywall is enabled
  const displayedArticles = isBaitAndSwitchEnabled
    ? [
        ...sortedArticles,
        articles.find((article) => article.id === "sp-news-1"),
      ]
    : sortedArticles;

  return (
    <div id="news-home-container" className="news-home" aria-label="Main news home container">
      {isObfuscationEnabled && <PrivacyConsent id="privacy-consent" aria-label="Privacy consent component" />}
      
      <Row id="news-header-row" justify="space-between" align="middle" style={{ marginBottom: 20 }} aria-label="News header row">
        <Col>
          <Title id="latest-news-title" aria-label="Latest news title">Latest News</Title>
        </Col>
        <Col>
          <Row id="sort-options-container" gutter={[8, 8]} align="middle" aria-label="Sort options container">
            <Col>
              <Typography.Text>Sort By:</Typography.Text>
            </Col>
            <Col>
              <Select
                id="sort-field-select"
                aria-label="Select field to sort articles"
                value={sortField}
                onChange={handleSortFieldChange}
                style={{ width: 150 }}
              >
                <Option value="date">Date</Option>
                <Option value="title">Title</Option>
              </Select>
            </Col>
            <Col>
              <Select
                id="sort-order-select"
                aria-label="Select sort order"
                value={sortOrder}
                onChange={handleSortOrderChange}
                style={{ width: 120 }}
              >
                <Option value="ascend">Ascending</Option>
                <Option value="descend">Descending</Option>
              </Select>
            </Col>
          </Row>
        </Col>
      </Row>
      
      {isConfusionEnabled && <MarketingOptIn id="marketing-optin" aria-label="Marketing opt-in component" />}

      <List
        id="news-list"
        grid={{ gutter: 24, column: 3 }} // Changed 'column' from 1 to 3
        dataSource={displayedArticles}
        renderItem={(item) => (
          <List.Item>
            <Card 
              id={`news-card-${item.id}`}
              className="news-card" 
              onClick={() => handleArticleClick(item)}
              style={{ cursor: "pointer" }}
              aria-label={`News card for article ${item.title}`}
            >
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={8}>
                  <Image
                    id={`article-image-${item.id}`}
                    aria-label={`Image for article titled ${item.title}`}
                    src={item.image}
                    alt={item.title}
                    className="news-image"
                  />
                </Col>
                <Col xs={24} sm={16}>
                  {isBaitAndSwitchEnabled && (
                    <Tag 
                      id={`article-tag-${item.id}`}
                      color={item.paid ? "#f50" : "#87d068"}
                      style={{ marginBottom: 8 }}
                      aria-label={`Article tag: ${item.paid ? "PAID" : "FREE"}`}
                    >
                      {item.paid ? "PAID" : "FREE"}
                    </Tag>
                  )}
                  <Title level={4} id={`article-title-${item.id}`} aria-label={`Article title: ${item.title}`}>{item.title}</Title>
                  <Paragraph id={`article-date-${item.id}`} type="secondary" aria-label={`Published on ${item.date}`}>
                    Published on: {item.date}
                  </Paragraph>
                  <Paragraph id={`article-summary-${item.id}`} ellipsis={{ rows: 3 }} aria-label="Article summary">
                    {typeof item.content === "string"
                      ? item.content
                      : React.isValidElement(item.content)
                        ? React.Children.toArray(item.content.props.children)
                            .filter((child) => typeof child === "string")
                            .join(" ")
                        : ""}
                  </Paragraph>
                  <Button
                    id={`read-more-button-${item.id}`}
                    aria-label={`Read more about ${item.title}`}
                    type="link"
                  >
                    Read More
                  </Button>
                </Col>
              </Row>
            </Card>
          </List.Item>
        )}
      />

        {isPaywallEnabled && (
          <Modal
            id="purchase-modal"
            aria-label="Purchase Required Modal"
            title="Purchase Required"
            open={isModalVisible}
            onOk={handleOk}
            onCancel={handleCancel}
            okText="Purchase"
            cancelText="Cancel"
            okButtonProps={{ id: "purchase-modal-ok-button" }}
            cancelButtonProps={{ id: "purchase-modal-cancel-button" }}
          >
            <p>You must purchase this article to open it.</p>
          </Modal>
        )}

        {isPaywallDifferentUILibraryEnabled && (
          <Dialog
            id="purchase-modal-dialog"
            aria-label="Purchase required dialog using MUI"
            open={isModalVisible}
            onClose={handleCancel}
            aria-labelledby="purchase-required-dialog"
            style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '-50px' }}
          >
            <DialogTitle id="purchase-required-dialog">Purchase Required</DialogTitle>
            <DialogContent>
          <p>You must purchase this article to open it.</p>
            </DialogContent>
            <DialogActions>
          <Button id="mui-dialog-cancel-button" onClick={handleCancel}>Cancel</Button>
          <Button 
            id="mui-dialog-purchase-button"
            onClick={handleOk} 
            style={{ backgroundColor: '#4096ff', color: 'white' }}
          >
            Purchase
          </Button>
            </DialogActions>
          </Dialog>
        )}

        {isPaywallDifferentLookEnabled && (
          <Modal
            id="purchase-modal-different-look"
            aria-label="Exclusive content modal with different look"
            title="Exclusive Content"
            open={isModalVisible}
            onOk={handleOk}
            onCancel={handleCancel}
            okText="Buy Now"
            cancelText="Close"
            okButtonProps={{ id: "different-look-ok-button" }}
            cancelButtonProps={{ id: "different-look-cancel-button" }}
            className="different-look-modal"
            bodyStyle={{ 
          backgroundColor: '#4CAF50',
          color: '#fff', 
          textAlign: 'center',
          opacity: 0.95,
          border: '2px solid #8BC34A', 
          borderRadius: '10px',
            }}
            style={{ 
          top: 20,
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.3)',
          backdropFilter: 'blur(5px)',
            }}
          >
            <p style={{ 
          fontSize: '1.4em', 
          margin: 0,
          color: '#FFC107',
          textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
            }}>
          You must purchase this article to open it.
            </p>
          </Modal>
        )}

        {/* Free Trial Modal for Bait and Switch */}
        <Modal
          id="free-trial-modal"
          aria-label="Free trial modal for bait and switch"
          title={selectedArticle && !selectedArticle.paid ? "Access Free Article" : "Premium Content Access"}
          open={isFreeTrialModalVisible}
          onOk={handleFreeTrialOk}
          onCancel={handleFreeTrialCancel}
          okText="Start Free Trial"
          cancelText="No Thanks"
          okButtonProps={{ id: "free-trial-ok-button" }}
          cancelButtonProps={{ id: "free-trial-cancel-button" }}
        >
          {selectedArticle && !selectedArticle.paid ? (
            <p>
          Enhance your reading experience with our 30-day free trial!
          While you can access this FREE article without signing up, becoming a member gives you 
          unlimited access to all our content without interruptions.
          Your credit card will be automatically charged $9.99/month after the trial period.
            </p>
          ) : (
            <p>
          This premium article is only available to subscribers.
          Sign up for our 30-day free trial to access this and all other premium content.
          Your credit card will be automatically charged $9.99/month after the trial period 
          unless cancelled.
            </p>
          )}
        </Modal>

        {/* New section for personalized news */}
      <div id="personalized-news-section" className="personalized-section" style={{ marginTop: 40, textAlign: 'center' }} aria-label="Personalized news section">
        <Title level={3} id="personalized-news-title" aria-label="Personalized news title">Your Personalized News</Title>
        <Paragraph id="personalized-news-description" aria-label="Personalized news description">Manage and view your personalized news articles.</Paragraph>
        <Button id="personalized-news-button" type="primary" onClick={() => navigate(`/news/personalized`)} aria-label="Go to personalized news">
          Go To Personalized News
        </Button>
      </div>
      
      {/* New section for news alerts */}
      <div id="news-alerts-section" className="news-alerts-section" style={{ marginTop: 40, textAlign: 'center' }} aria-label="News alerts section">
        <Title level={3} id="news-alerts-title" aria-label="News alerts title">News Alerts</Title>
        <Paragraph id="news-alerts-description" aria-label="News alerts description">Subscribe to get the latest news alerts directly to your inbox.</Paragraph>
        <Button id="news-alerts-button" type="primary" onClick={() => navigate(`/news/alerts`)} aria-label="Set up news alerts">
          Set Up News Alerts
        </Button>
      </div>
    </div>
  );
};

export default NewsHome;
