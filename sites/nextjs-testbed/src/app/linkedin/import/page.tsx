"use client";

import React, { useState } from "react";
import { Card, Input, Button, Modal } from "antd";
import { useRouter } from "next/navigation";

const ImportPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [showSkipModal, setShowSkipModal] = useState(false);
  const router = useRouter();

  const handleContinue = () => {
    console.log("Importing address book for email:", email);
    // In a real scenario, you'd proceed with import logic here
    // For this example, just stay on the page or redirect somewhere else if desired.
  };

  const handleSkipStep = () => {
    setShowSkipModal(true);
  };

  const handleFindNow = () => {
    // User decided to "Find Now" and not skip - close modal and continue
    setShowSkipModal(false);
  };

  const handleSkipConfirmation = () => {
    // User insists on skipping after seeing the modal
    // Redirect to the signup page
    router.push("/linkedin/signup");
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card 
        id="import-card" 
        className="w-full max-w-md p-6 bg-white rounded-lg shadow-lg" 
        aria-label="Import Address Book Form Card"
      >
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Grow your network on LinkedIn
        </h2>
        <p className="text-gray-600 mb-6">
          Get started by adding your email address. We&apos;ll import your
          address book to suggest connections and help you manage your contacts.
        </p>

        <div className="mb-4">
          <Input
            type="email"
            placeholder="Your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mb-4"
            id="import-email-input"
            aria-label="User Email Address"
          />

          <div className="flex justify-between items-center">
            <Button 
              type="primary" 
              onClick={handleContinue} 
              id="import-continue-button" 
              aria-label="Continue Importing Address Book"
            >
              Continue
            </Button>
            <button
              type="button"
              onClick={handleSkipStep}
              className="text-blue-500 hover:underline bg-transparent border-none cursor-pointer"
              id="import-skip-button"
              aria-label="Skip Importing Address Book"
            >
              Skip this step &raquo;
            </button>
          </div>
        </div>
      </Card>

      {/* Skip Modal */}
      <Modal
        open={showSkipModal}
        title="Skip seeing who you already know?"
        onCancel={() => setShowSkipModal(false)}
        footer={null}
        aria-label="Skip Import Confirmation Modal"
      >
        <p className="mb-4">
          If you skip this step, you&apos;ll miss out on easily finding people
            id="import-confirm-skip-button" 
          you know on LinkedIn.
        </p>
        <div className="flex justify-end space-x-2">
          <Button 
            onClick={handleFindNow} 
            id="import-find-now-button" 
            aria-label="Continue Importing Address Book"
          >
            Find now
          </Button>
          <Button 
            type="default" 
            onClick={handleSkipConfirmation} 
            id="import-confirm-skip-button" 
            aria-label="Confirm Skip Importing Address Book"
          >
            Skip
          </Button>
        </div>
      </Modal>
    </div>
  );
};

export default ImportPage;
