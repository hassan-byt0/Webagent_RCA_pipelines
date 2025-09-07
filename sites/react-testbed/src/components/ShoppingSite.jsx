import "./App.css";

// App.js
import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import Navbar from "./shopping/Navbar";
import HomePage from "./shopping/HomePage";
import CartPage from "./shopping/CartPage";
import ProductDetail from "./shopping/ProductDetail";
import { CartProvider } from "./shopping/CartContext";
import CheckoutSuccess from "./shopping/CheckoutSuccess";
import sampleProducts from "./shopping/sampleProducts";
import sponsoredProducts from "./shopping/sponsoredProducts";
import Scratchpad from "./Scratchpad";

function App() {
  const [addWarranty, setAddWarranty] = useState(false);
  const [showSponsored, setShowSponsored] = useState(false);
  const AppRoutes = () => {
    const location = useLocation();

    useEffect(() => {
      const params = new URLSearchParams(location.search);
      const features = params.get("dp");
      if (features) {
        setShowSponsored(features.includes("s"));
        setAddWarranty(features.includes("w"));
      }
    }, [location]);

    return (
      <Routes>
        <Route
          path=""
          element={
            <HomePage
              products={sampleProducts}
              sponsoredProducts={sponsoredProducts}
            />
          }
        />
        <Route path="cart" element={<CartPage />} />
        <Route
          path="product/:id"
          element={
            <ProductDetail
              products={sampleProducts}
              addWarranty={addWarranty}
              showSponsored={showSponsored}
              sponsoredProducts={sponsoredProducts}
            />
          }
        />
        <Route path="checkout-success" element={<CheckoutSuccess />} />
      </Routes>
    );
  };

  return (
    <>
      <CartProvider>
        <Navbar />
        <AppRoutes />
      </CartProvider>
      <Scratchpad />
    </>
  );
}

export default App;
