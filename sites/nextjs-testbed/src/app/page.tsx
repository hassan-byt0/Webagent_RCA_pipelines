"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  // Update patterns to real names
  const patterns = ["nagging", "preselection", "disguised ads"];
  const [selectedPattern, setSelectedPattern] = useState<string>("");
  const router = useRouter();

  const handleApplyPattern = () => {
    if (selectedPattern) {
      // Use the corresponding route identifier
      let dp = "";
      if (selectedPattern === "nagging") dp = "na";
      else if (selectedPattern === "preselection") dp = "ps";
      else if (selectedPattern === "disguised ads") dp = "da";
      router.push(`/linkedin?dp=${dp}`);
    }
  };

  const handleGoToRoute = () => {
    let route = "";
    if (selectedPattern === "nagging") {
      route = `/linkedin/import?dp=na`;
    } else if (selectedPattern === "disguised ads") {
      route = "/linkedin";
    }
    if (route) {
      router.push(route);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-800 to-black text-white">
      <div className="max-w-4xl text-center">
        <h1 className="text-5xl font-extrabold text-white mb-6">
          Welcome to the NextJS Test Bed
        </h1>
        <p className="text-lg text-gray-300">
          Experiment with dark patterns and see their effects on user behavior.
        </p>
      </div>

      <div className="mt-10 w-full max-w-2xl bg-gray-900 shadow-lg rounded-lg p-8">
        <h2 className="text-3xl font-semibold text-white mb-4">
          LinkedIn Routes
        </h2>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
          <div className="flex items-center gap-4">
            <label
              htmlFor="pattern-select"
              className="text-gray-200 font-medium"
            >
              Dark Pattern:
            </label>
            <select
              id="pattern-select"
              value={selectedPattern}
              onChange={(e) => setSelectedPattern(e.target.value)}
              className="w-48 px-3 py-2 bg-gray-700 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring focus:ring-yellow-500 hover:bg-gray-600"
            >
              <option value="">No Pattern</option>
              {patterns.map((pattern) => (
                <option
                  key={pattern}
                  value={pattern}
                  className="bg-gray-700 text-gray-200 hover:bg-gray-600"
                >
                  {pattern.charAt(0).toUpperCase() + pattern.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleApplyPattern}
            className="px-5 py-2 bg-yellow-600 text-black font-bold rounded-lg shadow hover:bg-yellow-700 transition"
          >
            Apply Pattern
          </button>
          <button
            onClick={handleGoToRoute}
            className="px-5 py-2 bg-blue-600 text-white font-bold rounded-lg shadow hover:bg-blue-700 transition"
          >
            Route which triggers DP
          </button>
        </div>
      </div>
    </div>
  );
}
