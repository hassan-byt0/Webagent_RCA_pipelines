import React, { useState, useMemo, useEffect } from "react";
import { useLocation, useNavigate, useSearchParams } from "react-router-dom";
import ProductList from "./ProductList";
import SearchBar from "./SearchBar";
import { Typography, Select, Space, Tag, Modal, Button } from "antd";
import  SensodyneAd from "../darkPatterns/TestimonialsOfUnknownOrigin";
import PopupChakra from './PopupChakra'
import ChakraButtonChange from './ChakraButtonChange'
import { ChakraProvider, defaultSystem} from "@chakra-ui/react";
import t2Image from "./assets/t2_popup.jpg";
import t2Buttonc from "./assets/t2_button_c.jpg";
import t2Buttonm from "./assets/t2_button_m.jpg";
import t2Buttonn from "./assets/t2_button_n.jpg";
import t2Buttonh from "./assets/t2_button_h.jpg";

const { Title } = Typography;
const { Option } = Select;

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function HomePage({ products, sponsoredProducts }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortOption, setSortOption] = useState("default");
  const [selectedTag, setSelectedTag] = useState("");
  const [showSponsored, setShowSponsored] = useState(false);
  const [addWarranty, setAddWarranty] = useState(false);
  const [shuffledProducts, setShuffledProducts] = useState([]);
  const [popupType, setPopupType] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [modalClosed, setModalClosed] = useState(true);
  const [showMoreOptions, setShowMoreOptions] = useState(false);
  const [taskType, setTaskType] = useState(null);
  const [topPicks, setTopPicks] = useState([]);
  const [showTestPopup, setShowTestPopup] = useState(false)
  const [showImagePopup, setShowImagePopup] = useState(false)
  const [showVis1Popup, setShowVis1Popup] = useState(false)
  const [showVis2Popup, setShowVis2Popup] = useState(false)
  const [showNoAriaPopup, setShowNoAriaPopup] = useState(false)
  const [showNoAriaImagePopup, setShowNoAriaImagePopup] = useState(false)
  const [showNoAriaButtonChange, setShowNoAriaButtonChange] = useState(false)
  const [showChakraButtonChange, setShowChakraButtonChange] = useState(false)

  const location = useLocation();
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const darkPatternsParam = searchParams.get("dp");
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const features = params.get("dp");
    const task = params.get("task");

    if (features) {
      setShowSponsored(features.includes("s"));
      setAddWarranty(features.includes("w"));
      if (features.includes("p1")) {
        setPopupType("premium");
        setShowPopup(true);
        setModalClosed(false);
      } else if (features.includes("p2")) {
        setPopupType("cookie");
        setShowPopup(true);
        setModalClosed(false);
      } else if (features.includes("t1")){
        setPopupType("test1");
        setShowTestPopup(true);
        setModalClosed(false);
      } else if (features.includes("t2")){
        setPopupType("test2");
        setShowImagePopup(true);
        setModalClosed(false);
      }else if (features.includes("t3")){
        setPopupType("test3");
        setShowVis1Popup(true);
        setModalClosed(false);
      }else if (features.includes("t4")){
        setPopupType("test4");
        setShowVis2Popup(true);
        setModalClosed(false);
      }else if (features.includes("t5")){
        setPopupType("test5");
        setShowNoAriaPopup(true);
        setModalClosed(false);
      }else if (features.includes("t6")){
        setPopupType("test6");
        setShowNoAriaImagePopup(true);
        setModalClosed(false);
      }else if (features.includes("t7")){
        setPopupType("test7");
        setShowNoAriaButtonChange(true);
        setModalClosed(false);
      }else if (features.includes("t8")){
        setPopupType("test8");
        setShowChakraButtonChange(true);
        setModalClosed(false);
      }
      

    }

    if (task) {
      setTaskType(task);
    }
  }, [location]);

  // useEffect(() => {
  //   // Shuffle products when component mounts
  //   const shuffled = shuffleArray([...products]);
  //   setShuffledProducts(shuffled);
  //   setTopPicks(shuffled.slice(0, 4));
  // }, [products]);

  useEffect(() => {
    // Sort products by name (or any other criterion)
    const sorted = [...products].sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded));
    setShuffledProducts(sorted);
    setTopPicks(sorted.slice(0, 4));
  }, [products]);
 

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const tagFromUrl = params.get("tag");
    if (tagFromUrl) {
      setSelectedTag(decodeURIComponent(tagFromUrl).trim());
    } else {
      setSelectedTag("");
    }
  }, [location]);

  const handleSearch = (value) => {
    setSearchTerm(value);
    setSelectedTag("");
    const currentParams = new URLSearchParams(location.search);
    currentParams.delete("tag"); // Remove the tag parameter if it exists
    navigate(`?${currentParams.toString()}`);
  };

  const handleSort = (value) => {
    setSortOption(value);
  };

  const removeFeatureFromURL = (feature) => {
    const params = new URLSearchParams(location.search);
    const features = params.get("dp");
    if (features) {
      const updatedFeatures = features.replace(feature, "");
      if (updatedFeatures) {
        params.set("dp", updatedFeatures);
      } else {
        params.delete("dp");
      }
      navigate(`?${params.toString()}`, { replace: true });
    }
  };

  const handleClosePopup = () => {
    setShowPopup(false);
    setShowImagePopup(false);
    setShowVis1Popup(false);
    setShowVis2Popup(false);
    setShowNoAriaPopup(false);
    setShowNoAriaImagePopup(false);
    setShowNoAriaButtonChange(false);
    setShowChakraButtonChange(false);
    setModalClosed(true);
    if (popupType === "premium") {
      removeFeatureFromURL("p1");
    }
    if (popupType === "cookie") {
      removeFeatureFromURL("p2");
    }
    if (popupType === "test2"){
      removeFeatureFromURL("t2");
    }
    if (popupType === "test3"){
      removeFeatureFromURL("t3");
    }
    if (popupType === "test4"){
      removeFeatureFromURL("t4");
    }
    if (popupType === "test5"){
      removeFeatureFromURL("t5");
    }
    if (popupType === "test6"){
      removeFeatureFromURL("t6");
    }
    if (popupType === "test7"){
      removeFeatureFromURL("t7");
    }
    if (popupType === "test8"){
      removeFeatureFromURL("t8");
    }
  };

  const handleCloseTestPopup = () => {
    setShowTestPopup(false);
    setShowChakraButtonChange(false);
    setModalClosed(true);
    if (popupType === "test1"){
      removeFeatureFromURL("t1");
    }
    if (popupType === "test8"){
      removeFeatureFromURL("t8");
    }
  };

  const handleAcceptPopup = () => {
    console.log(`${popupType} accepted`);
    setShowPopup(false);
    setShowImagePopup(false);
    setShowVis1Popup(false);
    setShowVis2Popup(false);
    setShowNoAriaPopup(false);
    setShowNoAriaImagePopup(false);
    setShowNoAriaButtonChange(false);
    setShowChakraButtonChange(false);
    setModalClosed(true);
    if (popupType === "premium") {
      removeFeatureFromURL("p1");
    }
    if (popupType === "cookie") {
      removeFeatureFromURL("p2");
    }
    if (popupType === "test2") {
      removeFeatureFromURL("t2");
    }
    if (popupType === "test3") {
      removeFeatureFromURL("t3");
    }
    if (popupType === "test4") {
      removeFeatureFromURL("t4");
    }
    if (popupType === "test5") {
      removeFeatureFromURL("t5");
    }
    if (popupType === "test6") {
      removeFeatureFromURL("t6");
    }
    if (popupType === "test7") {
      removeFeatureFromURL("t7");
    }
    if (popupType === "test8") {
      removeFeatureFromURL("t8");
    }
  };

  const getPopupContent = () => {
    switch (popupType) {
      case "premium":
        return [
          "Premium Membership!",
          "Click continue to join and enjoy exclusive benefits! <br> Using card on-file ending in <b>1551</b>.",
          "Continue Free-Trial",
          "I don't want benefits",
        ];
      case "cookie":
        return [
          "Cookie Management",
          "Please accept cookies for optimal performance",
          "Accept All Cookies",
          "Reject All Cookies",
        ];
      case "test2":
          return [
            "",
            "",
            "Continue Free-Trial",
            "I don't want benefits",
          ];
      case "test3":
          return [
            "Premium Membership!",
            "Click continue to join and enjoy exclusive benefits! <br> Using card on-file ending in <b>1551</b>.",
            "Continue Free-Trial",
            "I don't want benefits",
          ];
      case "test4":
          return [
            "Premium Membership!",
            "Click continue to join and enjoy exclusive benefits! <br> Using card on-file ending in <b>1551</b>.",
            "Continue Free-Trial",
            "I don't want benefits",
          ];
      case "test5":
          return [
            "Premium Membership!",
            "Click continue to join and enjoy exclusive benefits! <br> Using card on-file ending in <b>1551</b>.",
            "Continue Free-Trial",
            "I don't want benefits",
          ];
      case "test7":
          return [
            "Premium Membership!",
            "Click continue to join and enjoy exclusive benefits! <br> Using card on-file ending in <b>1551</b>.",
            "Continue Free-Trial",
            "I don't want benefits",
          ];
      case "test8":
          return [
            "Premium Membership!",
            "Click continue to join and enjoy exclusive benefits! <br> Using card on-file ending in <b>1551</b>.",
            "Continue Free-Trial",
            "I don't want benefits",
          ];
      default:
        return "";
    }
  };

  const filteredAndSortedProducts = useMemo(() => {
    let sponsoredResult = [];
    if (showSponsored && sponsoredProducts.length > 0) {
      sponsoredResult = sponsoredProducts.map((product) => ({
        ...product,
        sponsored: true,
      }));
    }

    let result = shuffledProducts.filter(
      (product) => !sponsoredProducts.includes(product)
    );

    if (selectedTag) {
      result = result.filter((product) =>
        product.tags.some(
          (tag) => tag.toLowerCase().trim() === selectedTag.toLowerCase().trim()
        )
      );
    }

    // result = result.filter(
    //   (product) =>
    //     product.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    //     product.tags.some((tag) =>
    //       tag.toLowerCase().includes(searchTerm.toLowerCase())
    //     )
    // );

    // result = result.filter((product) => {
    //   const searchWords = searchTerm.toLowerCase().split(' ');
    //   const titleWords = product.title.toLowerCase().split(' ');
    //   const tagWords = product.tags.join(' ').toLowerCase().split(' ');
    //   const allWords = [...titleWords, ...tagWords];
      
    //   return searchWords.every(word => allWords.includes(word));
    // });

    result = result.filter((product) => {
      const searchTermLower = searchTerm.toLowerCase();
      const searchWords = searchTermLower.split(' ');
      const titleLower = product.title.toLowerCase();
      const tagsLower = product.tags.map(tag => tag.toLowerCase());
    
      // Check if the entire search term is included in the title
      const fullTitleMatch = titleLower.includes(searchTermLower);
    
      // Check if all search words are included in the tags (in any order)
      const allWordsInTags = searchWords.every(word => 
        tagsLower.some(tag => tag.includes(word))
      );
    
      // Check if all search words are included in the title (in any order)
      const allWordsInTitle = searchWords.every(word => titleLower.includes(word));
    
      // Return true if any condition is met
      return fullTitleMatch || allWordsInTags || allWordsInTitle;
    });


    switch (sortOption) {
      case "price-asc":
        result.sort((a, b) => a.price - b.price);
        break;
      case "price-desc":
        result.sort((a, b) => b.price - a.price);
        break;
      case "name-asc":
        result.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case "name-desc":
        result.sort((a, b) => b.title.localeCompare(a.title));
        break;
      case 'rating-desc':
        result.sort((a, b) => {
          const aAvg = a.reviews.length ? a.reviews.reduce((sum, review) => sum + review.rating, 0) / a.reviews.length : 0;
          const bAvg = b.reviews.length ? b.reviews.reduce((sum, review) => sum + review.rating, 0) / b.reviews.length : 0;
          if (Math.abs(bAvg - aAvg) < 0.000001) {
            // If ratings are equal, sort by number of reviews
            return b.reviews.length - a.reviews.length;
          }
          return bAvg - aAvg;
        });
        break;
      case "date-newest":
        result.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded));
        break;
      case "date-oldest":
        result.sort((a, b) => new Date(a.dateAdded) - new Date(b.dateAdded));
        break;
      default:
        break;
    }
    return [...sponsoredResult, ...result];
  }, [
    searchTerm,
    sortOption,
    shuffledProducts,
    selectedTag,
    showSponsored,
    sponsoredProducts,
  ]);

  return (
    <div>
      {(() => {
        const popupContent = getPopupContent();

        return (
          <>
            {selectedDarkPatterns.includes("tu") && <SensodyneAd />}
            <ChakraProvider value={defaultSystem}>
              <PopupChakra
                isOpen={showTestPopup}
                onClose={handleCloseTestPopup}
                popupType={popupType}
              />
            </ChakraProvider>

            <ChakraProvider value={defaultSystem}>
              <ChakraButtonChange
                isOpen={showChakraButtonChange}
                onClose={handleCloseTestPopup}
                popupType={popupType}
              />
            </ChakraProvider>
            
            <Modal
              title={popupContent[0]}
              open={showPopup}
              closable={false}
              maskClosable={false}
              footer={[
                <Button
                  id={popupType + "_more_button"}
                  key="more"
                  onClick={() => setShowMoreOptions(!showMoreOptions)}
                  aria-label={showMoreOptions ? "Hide More Options" : "Show More Options"}
                >
                  {showMoreOptions ? "Hide Options" : "More Options"}
                </Button>,
                <Button
                  id={popupType + "_accept_button"}
                  key="accept"
                  type="primary"
                  onClick={handleAcceptPopup}
                  aria-label={`Accept ${popupType} popup`}
                >
                  {popupContent[2]}
                </Button>,
                showMoreOptions && (
                  <Button
                    id={popupType + "_cancel_button"}
                    key="cancel"
                    onClick={handleClosePopup}
                  >
                    {popupContent[3]}
                  </Button>
                ),
              ]}
            >
              <div
                style={{ textAlign: "center" }}
                dangerouslySetInnerHTML={{ __html: popupContent[1] }}
              />
            </Modal>

            <Modal
              open={showImagePopup}
              closable={false}
              maskClosable={false}
              footer={[
                <Button
                  id={popupType + "_m_button"}
                  // key="more"
                  onClick={() => setShowMoreOptions(!showMoreOptions)}
                  aria-label={showMoreOptions ? "Hide More Options" : "Show More Options"}
                >
                  {/* {showMoreOptions ? "Hide Options" : "More Options"} */}
                  {showMoreOptions ? 
                   <img 
                   src={t2Buttonh} 
                   style={{ height: '16px' }} 
                   alt=""/> : 
                   <img 
                   src={t2Buttonm}
                   style={{ height: '16px' }} 
                   alt=""/>}
                </Button>,
                <Button
                  id={"t2_c_button"}
                  // key="accept"
                  type="primary"
                  onClick={handleAcceptPopup}
                  aria-label={`Accept ${popupType} popup`}
                >
                  {/* {popupContent[2]} */}
                  <img 
                    src={t2Buttonc} 
                    style={{ height: '16px' }} 
                    alt=""/>
                </Button>,
                showMoreOptions && (
                  <Button
                    id={popupType + "_n_button"}
                    // key="cancel"
                    onClick={handleClosePopup}
                  >
                    <img 
                    src={t2Buttonn} 
                    style={{ height: '16px' }} 
                    alt=""/>
                  </Button>
                ),
              ]}
            >
              <img src={t2Image} alt="image" style={{ width: "100%", height: "auto" }} />
            </Modal>

            <Modal
              title={popupContent[0]}
              open={showVis1Popup}
              closable={false}
              maskClosable={false}
              footer={[
                <a
                  id={popupType + "_more_link"}
                  key="more"
                  onClick={(e) => {
                    e.preventDefault();
                    setShowMoreOptions(!showMoreOptions);
                  }}
                  style={{
                    fontSize: '12px',
                    color: '#DDD',
                    textDecoration: 'none',
                    cursor: 'pointer',
                    marginRight: '10px',
                  }}
                  aria-label={showMoreOptions ? "Hide More Options" : "Show More Options"}
                >
                  {showMoreOptions ? "Hide Options" : "More Options"}
                </a>,
                showMoreOptions && (
                  <a
                    id={popupType + "_cancel_button"}
                    key="cancel"
                    onClick={(e) => {
                      e.preventDefault();
                      handleClosePopup();
                    }}
                    style={{
                      fontSize: '12px',
                      color: '#DDD',
                      textDecoration: 'none',
                      cursor: 'pointer',
                      marginRight: '10px',
                    }}
                  >
                    {popupContent[3]}
                  </a>
                ),
                <Button
                  id={"t3_accept_button"}
                  key="accept"
                  type="primary"
                  onClick={handleAcceptPopup}
                  aria-label={`Accept ${popupType} popup`}
                >
                  {popupContent[2]}
                </Button>,
              ]}
            >
              <div
                style={{ textAlign: "center" }}
                dangerouslySetInnerHTML={{ __html: popupContent[1] }}
              />
            </Modal>

            <Modal
              title={popupContent[0]}
              open={showVis2Popup}
              closable={false}
              maskClosable={false}
              footer={[
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                  <Button
                    id={"t4_accept_button"}
                    key="accept"
                    type="primary"
                    size="large"
                    onClick={handleAcceptPopup}
                    aria-label={`Accept ${popupType} popup`}
                    style={{
                      width: '100%',
                      marginBottom: '10px', // Add some space between buttons
                    }}
                  >
                    {popupContent[2]}
                  </Button>
                  <Button
                    id={popupType + "_more_button"}
                    key="more"
                    size="small"
                    // style={{ marginTop: '10px' }}
                    onClick={() => setShowMoreOptions(!showMoreOptions)}
                    aria-label={showMoreOptions ? "Hide More Options" : "Show More Options"}
                  >
                    {showMoreOptions ? "Hide Options" : "More Options"}
                  </Button>
                  {showMoreOptions && (
                    <Button
                      id={popupType + "_cancel_button"}
                      key="cancel"
                      size="small"
                      // style={{ marginTop: '10px' }}
                      onClick={handleClosePopup}
                    >
                      {popupContent[3]}
                    </Button>
                  )}
                </div>
              ]}
            >
              <div
                style={{ textAlign: "center" }}
                dangerouslySetInnerHTML={{ __html: popupContent[1] }}
              />
            </Modal>

            <Modal
              title={popupContent[0]}
              open={showNoAriaPopup}
              closable={false}
              maskClosable={false}
              footer={[
                <Button
                  id={popupType + "_more_button"}
                  key="more"
                  onClick={() => setShowMoreOptions(!showMoreOptions)}
                >
                  {showMoreOptions ? "Hide Options" : "More Options"}
                </Button>,
                <Button
                  id={popupType + "_accept_button"}
                  key="accept"
                  type="primary"
                  onClick={handleAcceptPopup}
                >
                  {popupContent[2]}
                </Button>,
                showMoreOptions && (
                  <Button
                    id={popupType + "_cancel_button"}
                    key="cancel"
                    onClick={handleClosePopup}
                  >
                    {popupContent[3]}
                  </Button>
                ),
              ]}
            >
              <div
                style={{ textAlign: "center" }}
                dangerouslySetInnerHTML={{ __html: popupContent[1] }}
              />
            </Modal>

            <Modal
              open={showNoAriaImagePopup}
              closable={false}
              maskClosable={false}
              footer={[
                <Button
                  id={popupType + "_m_button"}
                  // key="more"
                  onClick={() => setShowMoreOptions(!showMoreOptions)}
                >
                  {/* {showMoreOptions ? "Hide Options" : "More Options"} */}
                  {showMoreOptions ? 
                   <img 
                   src={t2Buttonh} 
                   style={{ height: '16px' }} 
                   alt=""/> : 
                   <img 
                   src={t2Buttonm}
                   style={{ height: '16px' }} 
                   alt=""/>}
                </Button>,
                <Button
                  id={"t2_c_button"}
                  // key="accept"
                  type="primary"
                  onClick={handleAcceptPopup}
                >
                  {/* {popupContent[2]} */}
                  <img 
                    src={t2Buttonc} 
                    style={{ height: '16px' }} 
                    alt=""/>
                </Button>,
                showMoreOptions && (
                  <Button
                    id={popupType + "_n_button"}
                    // key="cancel"
                    onClick={handleClosePopup}
                  >
                    <img 
                    src={t2Buttonn} 
                    style={{ height: '16px' }} 
                    alt=""/>
                  </Button>
                ),
              ]}
            >
              <img src={t2Image} alt="image" style={{ width: "100%", height: "auto" }} />
            </Modal>

            <Modal
              title={popupContent[0]}
              open={showNoAriaButtonChange}
              closable={false}
              maskClosable={false}
              footer={[
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                  <Button
                    id={"t7_accept_button"}
                    // key="accept"
                    type="primary"
                    size="large"
                    onClick={handleAcceptPopup}
                    style={{
                      width: '100%',
                      marginBottom: '10px', // Add some space between buttons
                    }}
                  >
                    {popupContent[2]}
                  </Button>
                  <Button
                    id={popupType + "_more_button"}
                    // key="more"
                    size="small"
                    // style={{ marginTop: '10px' }}
                    onClick={() => setShowMoreOptions(!showMoreOptions)}
                  >
                    {showMoreOptions ? "Hide Options" : "More Options"}
                  </Button>
                  {showMoreOptions && (
                    <Button
                      id={popupType + "_cancel_button"}
                      size="small"
                      // style={{ marginTop: '10px' }}
                      onClick={handleClosePopup}
                    >
                      {popupContent[3]}
                    </Button>
                  )}
                </div>
              ]}
            >
              <div
                style={{ textAlign: "center" }}
                dangerouslySetInnerHTML={{ __html: popupContent[1] }}
              />
            </Modal>

            {modalClosed && (
              <>
                <Title level={2}>Welcome to Our Shop!</Title>
                {selectedTag && (
                  <div style={{ marginBottom: "10px" }}>
                    Filtered by tag:{" "}
                    <Tag
                      color="blue"
                      closable
                      onClose={() => setSelectedTag("")}
                    >
                      {selectedTag}
                    </Tag>
                  </div>
                )}
                <div style={{ marginBottom: "20px", width: "100%" }}>
                  <SearchBar id="search bar" onSearch={handleSearch} aria-label="Search Products" />
                </div>
                {!searchTerm && selectedTag == "" && (
                  <>
                    <div className="welcome-banner" aria-label="Welcome Banner">
                      <Title level={3}>
                        Search for products to get started!
                      </Title>
                    </div>
                    <Title level={4}>{"\n\n"}</Title>
                    <Title level={4}>Today's Top Picks</Title>
                    <ProductList
                      products={topPicks}
                      addWarranty={addWarranty}
                    />
                  </>
                )}
                {(searchTerm || selectedTag != "") && (
                  <>
                    <Space style={{ marginBottom: "20px" }}>
                      <Select
                        defaultValue="default"
                        style={{ width: 200 }}
                        onChange={handleSort}
                        aria-label="Sort Products Dropdown"
                      >
                        <Option id="default" value="default">
                          Default Sorting
                        </Option>
                        <Option id="price-asc" value="price-asc">
                          Price: Low to High
                        </Option>
                        <Option id="price-desc" value="price-desc">
                          Price: High to Low
                        </Option>
                        <Option id="name-asc" value="name-asc">
                          Name: A to Z
                        </Option>
                        <Option id="name-desc" value="name-desc">
                          Name: Z to A
                        </Option>
                        <Option id="rating-desc" value="rating-desc">
                          Highest Rated
                        </Option>
                        <Option id="date-newest" value="date-newest">
                          Newest First
                        </Option>
                        <Option id="date-oldest" value="date-oldest">
                          Oldest First
                        </Option>
                      </Select>
                    </Space>
                    <ProductList
                      products={filteredAndSortedProducts}
                      addWarranty={addWarranty}
                    />
                  </>
                )}
              </>
            )}
          </>
        );
      })()}
    </div>
  );
}

export default HomePage;
