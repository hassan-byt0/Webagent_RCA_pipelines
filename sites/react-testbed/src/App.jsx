// src/App.jsx

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Layout, Typography } from "antd";
import { SneakingProvider } from "./context/SneakingContext";
import Home from "./components/Home";

// Import base components directly here
import WikipediaClone from "./components/WikipediaClone";
import NewsSite from "./components/NewsSite";
import SpotifyClone from "./components/SpotifyClone";
import HealthClone from "./components/HealthClone";
import ShoppingSite from "./components/ShoppingSite";
import { Analytics } from "@vercel/analytics/react"

const { Content } = Layout;
const { Title } = Typography;

/**
 * Array of base components with their corresponding paths and component references.
 */
const baseComponents = [
  { name: "WikipediaClone", path: "wiki", component: WikipediaClone },
  { name: "NewsSite", path: "news", component: NewsSite },
  { name: "SpotifyClone", path: "spotify", component: SpotifyClone },
  { name: "HealthClone", path: "health", component: HealthClone },
  { name: "ShoppingSite", path: "shop", component: ShoppingSite },
];

const App = () => {
  return (
    <React.Fragment>
      <Router>
        <SneakingProvider>
          <Layout style={{ padding: "2rem", minHeight: "100vh" }}>
            <Content>
              <Routes>
                {/* Home Route */}
                <Route path="/" element={<Home />} />

                {/* Default Routes with Dark Patterns */}
                {baseComponents.map((baseComp) => (
                  <Route
                    key={`${baseComp.name}-default`}
                    path={`/${baseComp.path}/*`}
                    element={<baseComp.component />}
                  />
                ))}

                {/* Catch-All Route */}
                <Route
                  path="*"
                  element={
                    <Title
                      level={4}
                      type="danger"
                      style={{ textAlign: "center" }}
                    >
                      404 - Page Not Found
                    </Title>
                  }
                />
              </Routes>
            </Content>
          </Layout>
        </SneakingProvider>
      </Router>
      <Analytics />
    </React.Fragment>
  );
};

export default App;
