// src/pages/CartPage.js
import React from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "./CartContext";
import { List, Button, InputNumber, Typography } from "antd";

const { Title } = Typography;

function CartPage() {
  const navigate = useNavigate();

  const { cart, removeFromCart, updateQuantity, checkout } = useCart();

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleCheckout = () => {
    // Perform checkout logic here
    checkout();
    navigate("/shop/checkout-success");
  };

  return (
    <div style={{ padding: "20px" }}>
      <Title level={2}>Shopping Cart</Title>
      <List
        itemLayout="horizontal"
        dataSource={cart}
        renderItem={(item) => (
          <List.Item
            actions={[
              <InputNumber
                min={1}
                value={item.quantity}
                onChange={(value) => updateQuantity(item.id, value)}
              />,
              <Button
                id={"remove button for: " + item.title}
                onClick={() => removeFromCart(item.id)}
                aria-label={`Remove ${item.title} from cart`}
              >
                Remove
              </Button>,
            ]}
          >
            <List.Item.Meta
              title={item.title}
              description={`$${item.price.toFixed(2)}`}
            />
            <div>Subtotal: ${(item.price * item.quantity).toFixed(2)}</div>
          </List.Item>
        )}
      />
      <Title level={4}>Total: ${total.toFixed(2)}</Title>
      <Button
        id={"checkout-button"}
        type="primary"
        onClick={handleCheckout}
        aria-label="Proceed to Checkout"
      >
        Proceed to Checkout
      </Button>
    </div>
  );
}

export default CartPage;
