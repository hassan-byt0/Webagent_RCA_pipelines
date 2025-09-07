import React, { createContext, useState, useContext, useEffect } from "react";

export const CartContext = createContext();
import { notification } from "antd";

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    const savedCart = localStorage.getItem("cart");
    return savedCart ? JSON.parse(savedCart) : [];
  });

  const [purchasedItems, setPurchasedItems] = useState(() => {
    const savedPurchasedItems = localStorage.getItem("purchasedItems");
    return savedPurchasedItems ? JSON.parse(savedPurchasedItems) : [];
  });

  const showNotification = (message) => {
    notification.success({
      message: "Success",
      description: message,
      placement: "bottomRight",
      duration: 2,
      'aria-label': 'Success Notification',
    });
  };

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    localStorage.setItem("purchasedItems", JSON.stringify(purchasedItems));
  }, [purchasedItems]);

  const addToCart = (product) => {
    showNotification("Item added to cart");
    setCart((prevCart) => {
      const existingItem = prevCart.find((item) => item.id === product.id);
      if (existingItem) {
        return prevCart.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prevCart, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== productId));
  };

  const updateQuantity = (productId, quantity) => {
    setCart((prevCart) =>
      prevCart.map((item) =>
        item.id === productId ? { ...item, quantity: quantity } : item
      )
    );
  };

  const checkout = () => {
    setPurchasedItems(cart);
    setCart([]);
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        checkout,
        purchasedItems,
        notification,
        showNotification,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => React.useContext(CartContext);
