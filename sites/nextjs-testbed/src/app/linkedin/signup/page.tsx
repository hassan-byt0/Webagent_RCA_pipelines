"use client";

import React, { useState, useEffect, Suspense } from "react";
import { Card, Input, Button, Checkbox } from "antd";
import { useSearchParams, usePathname } from "next/navigation";

const SignUpContent = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [subscribeNewsletter, setSubscribeNewsletter] = useState(false);
  const [shareData, setShareData] = useState(false);

  const searchParams = useSearchParams();
  const darkPatternParam = searchParams.get("dp");
  const usePreselection = darkPatternParam?.includes("ps");

  useEffect(() => {
    if (usePreselection) {
      setSubscribeNewsletter(true);
      setShareData(true);
    }
  }, [usePreselection]);

  const handleSignUp = () => {
    console.log("User signed up with:", {
      email,
      password,
      subscribeNewsletter,
      shareData,
    });
    if (typeof window !== "undefined") {
      // Navigate to home page after sign up
      window.location.href = "/linkedin"; // Replace with the actual home page path
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card 
        id="signup-card" 
        className="w-full max-w-md p-6 bg-white rounded-lg shadow-lg" 
        aria-label="Sign Up Form Card"
      >
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Sign Up</h2>
        <p className="text-gray-600 mb-6">
          Create your account to get started.
        </p>

        <div className="mb-4">
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mb-2"
            id="signup-email-input"
            aria-label="Email Address"
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mb-4"
            id="signup-password-input"
            aria-label="Password"
          />

          <div className="mt-3">
            <Checkbox
              checked={subscribeNewsletter}
              onChange={(e) => setSubscribeNewsletter(e.target.checked)}
              id="signup-newsletter-checkbox"
              aria-label="Subscribe to Newsletter"
            >
              Receive our newsletter
            </Checkbox>
          </div>
          <div className="mt-2">
            <Checkbox
              checked={shareData}
              onChange={(e) => setShareData(e.target.checked)}
              id="signup-sharedata-checkbox"
              aria-label="Share Data with Trusted Partners"
            >
              Share my data with trusted partners
            </Checkbox>
          </div>
        </div>

        <div className="flex justify-end mt-4">
          <Button 
            type="primary" 
            onClick={handleSignUp}
            id="signup-submit-button"
            aria-label="Submit Sign Up Form"
          >
            Sign Up
          </Button>
        </div>
      </Card>
    </div>
  );
};

const SearchParamsWrapper: React.FC = () => {
  const searchParams = useSearchParams();
  const pathname = usePathname();

  useEffect(() => {
    const isReloaded = searchParams.get("reloaded") === "true";
    if (!isReloaded) {
      const newSearchParams = new URLSearchParams(
        searchParams as unknown as URLSearchParams
      );
      newSearchParams.set("reloaded", "true");
      window.location.href = `${pathname}?${newSearchParams.toString()}`;
    }
  }, [searchParams, pathname]);

  return <SignUpContent />;
};

const SignUpPage: React.FC = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchParamsWrapper />
    </Suspense>
  );
};

export default SignUpPage;
