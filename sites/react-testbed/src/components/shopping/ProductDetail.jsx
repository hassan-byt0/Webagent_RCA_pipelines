// src/components/ProductDetail.js
import React, { useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import { Card, Rate, List, Typography, Button, Divider } from "antd";
import { useCart } from "./CartContext";
// import { useAddToCart } from '../utils/cartUtils';
import ReviewForm from "./ReviewForm";

const { Title, Text } = Typography;

function ProductDetail({
  products,
  addWarranty,
  showSponsored,
  sponsoredProducts,
}) {
  const { id } = useParams();
  const { addToCart } = useCart();
  const handleAddToCart = () => {
    console.log(addWarranty);
    addToCart(product);
    if (addWarranty) {
      addToCart({
        id: `${product.id}-warranty`,
        title: `${product.title} Warranty`,
        price: product.price * 0.05,
      });
    }
  };
  const [newReviews, setNewReviews] = useState([]);
  let product = products.find((p) => p.id === parseInt(id));

  if (showSponsored && !product) {
    product = sponsoredProducts.find((p) => p.id === parseInt(id));
  }

  const allReviews = useMemo(() => {
    if (!product) return [];
    return [...product.reviews, ...newReviews];
  }, [product, newReviews]);

  const averageRating = useMemo(() => {
    if (allReviews.length === 0) return 0;
    return (
      allReviews.reduce((sum, review) => sum + review.rating, 0) /
      allReviews.length
    );
  }, [allReviews]);

  const roundedRating = averageRating.toFixed(1);

  const handleNewReview = (newReview) => {
    setNewReviews((prevReviews) => [...prevReviews, newReview]);
  };

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <Card
        cover={
          <img
            alt={product.title}
            src={product.image}
            style={{ maxWidth: "300px", margin: "auto" }}
            aria-label={`${product.title} image`}
          />
        }
      >
        <Title level={2}>{product.title}</Title>
        <Title level={4}>${product.price.toFixed(2)}</Title>
        <div style={{ padding: "20px" }}>
          <Button
            id={"add_to_cart_" + product.id}
            type="primary"
            size="large"
            onClick={() => handleAddToCart(product)}
            aria-label={`Add ${product.title} to cart`}
          >
            Add to Cart
          </Button>
        </div>
        <Title level={4}>Description</Title>
        <Text>{product.description}</Text>
        <div style={{ marginTop: "20px" }}>
          <Title level={4}>Reviews</Title>
          <div
            style={{ display: "flex", alignItems: "center", marginTop: "10px" }}
          >
            <Rate
              disabled
              defaultValue={averageRating}
              allowHalf
              aria-label={`Average Rating: ${roundedRating} out of 5`}
            />
            <Text style={{ marginLeft: "10px" }}>{roundedRating}</Text>
            <Text style={{ marginLeft: "10px" }}>
              ({product.reviews.length} reviews)
            </Text>
          </div>
          <List
            itemLayout="horizontal"
            dataSource={allReviews}
            renderItem={(review) => (
              <List.Item>
                <List.Item.Meta
                  title={
                    <>
                      <Text strong>
                        {review.username}: {review.title}
                      </Text>{" "}
                      <Rate
                        disabled
                        defaultValue={review.rating}
                        aria-label={`Rating by ${review.username}: ${review.rating} out of 5`}
                      />
                    </>
                  }
                  description={review.comment}
                />
              </List.Item>
            )}
          />
          <Divider />
          <Title level={4}>Write a Review</Title>
          <ReviewForm onSubmit={handleNewReview} />
        </div>
      </Card>
    </div>
  );
}

export default ProductDetail;
