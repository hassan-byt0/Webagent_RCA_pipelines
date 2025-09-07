// ProductCard.js
import React from "react";
import { Card, Button, Tag, Rate, Typography } from "antd";
import { useNavigate } from "react-router-dom";
import { useCart } from "./CartContext";
import { LinkWithQuery } from "./LinkWithQuery";
// import { useAddToCart } from '../utils/cartUtils';

const { Title, Text } = Typography;

function ProductCard({ product, addWarranty }) {
  const { addToCart } = useCart();
  const navigate = useNavigate();
  const averageRating =
    product.reviews.reduce((sum, review) => sum + review.rating, 0) /
    product.reviews.length;
  const roundedRating = isNaN(averageRating)
    ? "No reviews"
    : averageRating.toFixed(1);

  // const handleAddToCart = useAddToCart(addToCart)
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

  const handleTagClick = (e, tag) => {
    e.preventDefault(); // This prevents the card link from activating
    navigate(`/shop/?tag= ${encodeURIComponent(tag.trim())}`);
  };

  return (
    <LinkWithQuery
      to={`product/${product.id}`}
      style={{ textDecoration: "none" }}
    >
      <Card
        id={"product_card_" + product.id}
        hoverable
        cover={<img alt={product.title} src={product.image} aria-label={`${product.title} image`} />}
        actions={[
          <Button
            id={"add_to_cart_" + product.id}
            type="primary"
            onClick={(e) => {
              e.preventDefault();
              handleAddToCart(product);
            }}
            aria-label={`Add ${product.title} to cart`}
          >
            Add to Cart
          </Button>,
        ]}
        aria-label={`Product card for ${product.title}`}
      >
        {product.sponsored && <div style={{ color: "green" }}>Sponsored</div>}

        <Card.Meta
          title={
            <LinkWithQuery to={`product/${product.id}`} aria-label={`View details for ${product.title}`}>
              {product.title}
            </LinkWithQuery>
          }
          description={
            <>
              <Title level={5} aria-label={`Price: $${product.price.toFixed(2)}`}>
                PRICE: ${product.price.toFixed(2)}
              </Title>
              <div>
                {product.tags.map((tag, index) => (
                  <Tag
                    key={index}
                    onClick={(e) => handleTagClick(e, tag)}
                    style={{ cursor: "pointer" }}
                    aria-label={`Filter by tag ${tag}`}
                  >
                    {tag}
                  </Tag>
                ))}
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  marginTop: "10px",
                }}
              >
                <Rate
                  disabled
                  defaultValue={averageRating}
                  allowHalf
                  aria-label={`Product Rating: ${roundedRating} out of 5`}
                />
                <Text style={{ marginLeft: "10px" }}>{roundedRating}</Text>
              </div>
            </>
          }
          aria-label={`Product details for ${product.title}`}
        />
      </Card>
    </LinkWithQuery>
  );
}

export default ProductCard;
