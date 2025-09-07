"use client";

import React from "react";
import { Menu } from "antd";
import Link from "next/link";
import { useId } from "react-id-generator";

const LinkedInFooter: React.FC = () => {
  // Generate unique IDs
  const [footerId, menuId, aboutId, contactId, privacyId] = useId(
    5,
    "linkedin-footer-"
  );

  const menuItems = [
    {
      key: "about",
      label: (
        <Link id={aboutId} href="/linkedin/about" aria-label="About Page">
          About
        </Link>
      ),
    },
    {
      key: "contact",
      label: (
        <Link id={contactId} href="/linkedin/contact" aria-label="Contact Page">
          Contact
        </Link>
      ),
    },
    {
      key: "privacy",
      label: (
        <Link id={privacyId} href="/linkedin/privacy" aria-label="Privacy Policy">
          Privacy
        </Link>
      ),
    },
  ];

  return (
    <footer id={footerId} className="bg-gray-800 text-white p-4">
      <Menu
        id={menuId}
        mode="horizontal"
        selectable={false}
        className="bg-gray-800 text-white border-none"
        items={menuItems}
      />
    </footer>
  );
};

export default LinkedInFooter;
