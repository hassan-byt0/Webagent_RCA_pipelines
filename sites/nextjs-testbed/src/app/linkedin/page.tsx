// app/linkedin/page.tsx
"use client";
import React, { Suspense } from "react";
import Feed from "./components/Feed";

const LinkedInHome: React.FC = () => {
  return (
    <Suspense fallback={<div id="feed-loading">Loading feed...</div>}>
      <Feed aria-label="LinkedIn Feed" />
    </Suspense>
  );
};

export default LinkedInHome;
