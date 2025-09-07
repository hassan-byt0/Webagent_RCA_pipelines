// src/components/Navbar.js
import React from "react";
import { Menu, Badge } from "antd";
import { LinkWithQuery } from "./LinkWithQuery";
import { ShoppingCartOutlined } from "@ant-design/icons";
import { useCart } from "./CartContext";

function Navbar() {
  const { cart } = useCart();
  const cartItemCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <Menu
      mode="horizontal"
      style={{ display: "flex", fontSize: "120%", padding: "5px" }}
    >
      <Menu.Item id="home button" key="home" aria-label="Navigate to Home">
        <LinkWithQuery to="/shop">Home</LinkWithQuery>
      </Menu.Item>
      <Menu.Item
        key="cart"
        style={{ marginLeft: "auto" }}
        aria-label="View Shopping Cart"
      >
        <LinkWithQuery to="cart">
          <Badge count={cartItemCount}>
            <ShoppingCartOutlined id={"add-to-cart-button"} style={{ fontSize: "200%" }} aria-label="Shopping Cart Icon" />
            {/* <ShoppingCartOutlined style={{ fontSize: '30px' }} /> */}
          </Badge>
        </LinkWithQuery>
      </Menu.Item>
    </Menu>
  );
}

export default Navbar;
