"use client";

import React from "react";
import { useParams } from "next/navigation";
import { Card, Typography } from "antd";
import { useId } from "react-id-generator";

const { Title } = Typography;

const summaries: Record<string, string> = {
  "2": "Purdue University is a leading institution in engineering and technology, known for its rigorous academic programs and industry connections.",
  // Add more summaries for other profiles as needed
};

const ProfileSummary: React.FC = () => {
  const params = useParams();
  const profileId = Array.isArray(params.profileId)
    ? params.profileId[0]
    : params.profileId;
  const summary = profileId ? summaries[profileId] : "Summary not available.";

  // Generate unique IDs for profile summary elements
  const [containerId, cardId, titleId] = useId(4, "profile-summary-");

  return (
    <div id="profile-summary-container" className="p-4 max-w-2xl mx-auto">
      <Card
        id="profile-summary-card"
        title="Profile Summary"
        className="shadow-md rounded-lg"
        aria-label="User Profile Summary"
      >
        <Title id="profile-summary-title" level={4} className="text-gray-800">
          {summary}
        </Title>
      </Card>
    </div>
  );
};

export default ProfileSummary;
