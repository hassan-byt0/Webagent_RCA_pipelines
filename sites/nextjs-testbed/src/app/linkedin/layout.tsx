"use client";

import React, { ReactNode } from "react";
import LinkedInHeader from "./components/Header";
import LinkedInSidebar from "./components/Sidebar";
import { PostsProvider } from "./context/PostsContext";
import Scratchpad from "./components/Scratchpad";

// If you have dark patterns components, you can leave them out until you reach checkpoint 7.
export const meta = {
  title: "LinkedIn Clone",
  description: "A LinkedIn-like experience using Next.js, TS, and Tailwind.",
};

interface LinkedInLayoutProps {
  children: ReactNode;
}

const LinkedInLayout: React.FC<LinkedInLayoutProps> = ({ children }) => {
  return (
    <PostsProvider>
      <div className="min-h-screen flex flex-col bg-gray-100">
        <LinkedInHeader />
        <div className="flex flex-1">
          <LinkedInSidebar />
          <main className="flex-1 p-4">{children}</main>
        </div>
      </div>
      <Scratchpad />
    </PostsProvider>
  );
};

export default LinkedInLayout;
