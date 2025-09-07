import React from "react";
import { Typography, List } from "antd";
import { useCart } from "./CartContext";

const { Title } = Typography;

function CheckoutSuccess() {
  const { purchasedItems } = useCart();
  return (
    <div style={{ textAlign: "center", padding: "50px" }} aria-label="Checkout Success Message">
      <Title>Success!</Title>
      <p>Your order has been placed successfully.</p>
      {purchasedItems.length === 0 ? (
        <p>No items purchased.</p>
      ) : (
        <List
          itemLayout="horizontal"
          dataSource={purchasedItems}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                title={item.name}
                description={`Quantity: ${item.quantity}, Price: $${item.price}`}
              />
            </List.Item>
          )}
        />
      )}
    </div>
  );
}

export default CheckoutSuccess;
