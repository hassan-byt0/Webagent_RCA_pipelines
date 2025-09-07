"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { Input, Button } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import { useRouter } from "next/navigation";
import { useId } from "react-id-generator";

function appendPattern(path: string): string {
  if (typeof window !== "undefined") {
    const stored = localStorage.getItem("selectedPattern");
    if (stored) {
      const separator = path.includes("?") ? "&" : "?";
      return `${path}${separator}dp=${stored}`;
    }
  }
  return path;
}

const LinkedInHeader: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [hasSignedUp, setHasSignedUp] = useState<boolean>(false);
  const [hasSyncedPattern, setHasSyncedPattern] = useState<boolean>(false);
  const [hideSignupButton, setHideSignupButton] = useState<boolean>(false);
  const router = useRouter();

  // Generate unique IDs for header elements
  const [
    headerId,
    logoLinkId,
    searchInputId,
    searchButtonId,
    homeLinkId,
    applicationsLinkId,
    meLinkId,
    signUpButtonId,
  ] = useId(8, "linkedin-header-");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const signedUp = localStorage.getItem("signedUp");
      if (signedUp === "true") {
        setHasSignedUp(true);
      }

      const hideButton = localStorage.getItem("hideSignupButton");
      if (hideButton === "true") {
        setHideSignupButton(true);
      }

      const currentUrl = new URL(window.location.href);
      const urlPattern = currentUrl.searchParams.get("dp");
      const storedPattern = localStorage.getItem("selectedPattern");

      if (urlPattern) {
        if (storedPattern !== urlPattern) {
          localStorage.setItem("selectedPattern", urlPattern);
        }
      } else if (storedPattern) {
        currentUrl.searchParams.set("dp", storedPattern);
        router.replace(currentUrl.toString());
      }

      setHasSyncedPattern(true);
    } else {
      setHasSyncedPattern(true);
    }
  }, [router]);

  const handleSearch = () => {
    if (searchQuery.trim() && typeof window !== "undefined") {
      const storedPattern = localStorage.getItem("selectedPattern");
      const queryParams = new URLSearchParams({ q: searchQuery });
      if (storedPattern) {
        queryParams.set("dp", storedPattern);
      }
      router.push(`/linkedin/search?${queryParams.toString()}`);
    }
  };

  const handleSignUpClick = () => {
    // Hide the sign-up button immediately
    setHideSignupButton(true);
    // Persist the hide state
    localStorage.setItem("hideSignupButton", "true");
    // Navigate to the signup page
    router.push("/linkedin/signup");
  };

  if (!hasSyncedPattern) {
    // Initial render before pattern sync; just return a stable header
    return (
      <header
        id={headerId}
        className="flex items-center bg-blue-700 text-white p-4"
      >
        <div className="flex items-center">
          <Link id={logoLinkId} href="/linkedin">
            <Image
              src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG8.png"
              alt="LinkedIn Logo"
              className="h-8 w-auto"
              width={30}
              height={30}
              unoptimized
            />
          </Link>
        </div>
        <div className="flex items-center space-x-2 mx-4 flex-1">
          <Input
            id={searchInputId}
            className="flex-1 bg-white text-black"
            placeholder="Search..."
            prefix={<SearchOutlined className="text-gray-500" />}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <Button id={searchButtonId} type="primary" onClick={handleSearch}>
            Search
          </Button>
        </div>
        <div className="flex items-center space-x-4 ml-auto">
          <Link
            id={homeLinkId}
            href="/linkedin"
            className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-1 px-3 rounded-lg transition"
          >
            Home
          </Link>
          <Link
            id={applicationsLinkId}
            href="/linkedin/applications"
            className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-1 px-3 rounded-lg transition"
          >
            My Applications
          </Link>
          <Link
            id={meLinkId}
            href="/linkedin/user/1"
            className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-1 px-3 rounded-lg transition"
          >
            Me
          </Link>
          {!hasSignedUp && !hideSignupButton && (
            <button
              id={signUpButtonId}
              onClick={handleSignUpClick}
              className="bg-yellow-500 text-black font-bold py-1 px-4 rounded-lg hover:bg-yellow-600 transition"
            >
              Sign Up
            </button>
          )}
        </div>
      </header>
    );
  }

  return (
    <header
      id={headerId}
      className="flex items-center bg-blue-700 text-white p-4"
    >
      <div className="flex items-center">
        <Link id={logoLinkId} href={appendPattern("/linkedin")}>
          <Image
            src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG8.png"
            alt="LinkedIn Logo"
            className="h-8 w-auto"
            width={30}
            height={30}
            unoptimized
          />
        </Link>
      </div>

      <div className="flex items-center space-x-2 mx-4 flex-1">
        <Input
          id={searchInputId}
          className="flex-1 bg-white text-black"
          placeholder="Search for people, jobs, companies..."
          prefix={<SearchOutlined className="text-gray-500" />}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onPressEnter={handleSearch}
          aria-label="Search Input"
        />
        <Button id={searchButtonId} type="primary" onClick={handleSearch} aria-label="Search Button">
          Search
        </Button>
      </div>

      <div className="flex items-center space-x-4 ml-auto">
        <Link
          id={homeLinkId}
          href={appendPattern("/linkedin")}
          className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-1 px-3 rounded-lg transition"
        >
          Home
        </Link>
        <Link
          id={applicationsLinkId}
          href={appendPattern("/linkedin/applications")}
          className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-1 px-3 rounded-lg transition"
        >
          My Applications
        </Link>
        <Link
          id={meLinkId}
          href={appendPattern("/linkedin/user/1")}
          className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-1 px-3 rounded-lg transition"
        >
          Me
        </Link>
        {!hasSignedUp && !hideSignupButton && (
          <button
            id={signUpButtonId}
            onClick={handleSignUpClick}
            className="bg-yellow-500 text-black font-bold py-1 px-4 rounded-lg hover:bg-yellow-600 transition"
            aria-label="Sign Up Button"
          >
            Sign Up
          </button>
        )}
      </div>
    </header>
  );
};

export default LinkedInHeader;
