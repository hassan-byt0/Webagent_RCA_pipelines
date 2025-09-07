// ProductList.js
import React from "react";
import { Row, Col } from "antd";
import ProductCard from "./ProductCard";

function ProductList({ products, addWarranty }) {
  return (
    <Row gutter={[16, 16]} aria-label="Product List">
      {products.map((product) => (
        <Col key={product.id} xs={24} sm={12} md={8} lg={6} aria-label={`Product ${product.title}`}>
          <ProductCard product={product} addWarranty={addWarranty} />
        </Col>
      ))}
    </Row>
  );
}

export default ProductList;
