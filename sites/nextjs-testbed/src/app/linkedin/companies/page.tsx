"use client";

import React, { useState, Suspense } from "react";
import { Card, List, Avatar, Button } from "antd";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import companies from "../data/companies";
import Nagging from "../components/darkPatterns/Nagging";

const CompaniesContent = () => {
  const [showNagging, setShowNagging] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  const darkPatternParam = searchParams.get("dp");
  const useNagging = darkPatternParam?.includes("na")

  const handleSkip = () => {
    if (useNagging) {
      setShowNagging(true);
    } else {
      console.log("User skipped viewing more companies.");
      router.push("/linkedin");
    }
  };

  const handleNaggingContinue = () => {
    setShowNagging(false);
    console.log("User decided to continue and not skip.");
  };

  const handleNaggingSkip = () => {
    setShowNagging(false);
    console.log("User skipped after nagging.");
    router.push("/linkedin");
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <Card className="shadow-md rounded-lg">
        <h2 className="text-2xl font-semibold mb-4 text-gray-800">Companies</h2>
        <p className="text-gray-600 mb-6">
          Here are some companies you might be interested in:
        </p>

        <List
          dataSource={companies}
          renderItem={(company) => (
            <List.Item
              className="border-b py-4"
              id={`company-item-${company.id}`}
              aria-label={`Company ${company.name}`}
            >
              <List.Item.Meta
                avatar={<Avatar src={company.logo} aria-label={`${company.name} logo`} />}
                title={
                  <Link
                    href={`/linkedin/company/${company.id}`}
                    id={`company-link-${company.id}`}
                    aria-label={`View profile of ${company.name}`}
                  >
                    {company.name}
                  </Link>
                }
                description={company.industry}
              />
            </List.Item>
          )}
        />

        <div className="mt-4 flex justify-end">
          <Button 
            onClick={handleSkip} 
            className="text-gray-500" 
            id="skip-companies-button" 
            aria-label="Skip viewing more companies"
          >
            Skip
          </Button>
        </div>
      </Card>

      {useNagging && (
        <Nagging
          visible={showNagging}
          onContinue={handleNaggingContinue}
          onSkip={handleNaggingSkip}
        />
      )}
    </div>
  );
};

const CompaniesPage: React.FC = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <CompaniesContent />
    </Suspense>
  );
};

export default CompaniesPage;
