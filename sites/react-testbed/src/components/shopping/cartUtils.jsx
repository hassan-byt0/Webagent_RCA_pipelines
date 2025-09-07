// src/utils/cartUtils.js
import { message } from "antd";

export const useAddToCart = (addToCart) => {
  return (product) => {
    addToCart(product);
    message.success(`${product.title} added to cart!`);
  };
};
