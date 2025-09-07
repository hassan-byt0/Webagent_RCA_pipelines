"use client";

import React, { useState } from "react";
import { Card, List, Avatar, Tag } from "antd";
import Link from "next/link";
import users from "../data/users";
import companies from "../data/companies";

interface User {
  id: string;
  applications: Application[];
}

interface Application {
  companyId: string;
  title: string;
  date: string;
  status: string;
}

const ApplicationStatus: React.FC = () => {
  const [currentUser] = useState<User | undefined>(
    users.find((u) => u.id === "1")
  );
  if (!currentUser) return <div className="p-4">User not found.</div>;

  const userApplications = currentUser.applications || [];

  const applicationData = userApplications.map((app) => {
    const company = companies.find((c) => c.id === app.companyId);
    return {
      ...app,
      companyName: company?.name || "Unknown Company",
      companyLogo: company?.logo || "",
    };
  });

  return (
    <div className="max-w-2xl mx-auto p-4">
      <Card title="My Applications" className="shadow-md rounded-lg">
        <List
          dataSource={applicationData}
          renderItem={(app) => (
            <List.Item className="border-b py-4 flex justify-between items-center" aria-label={`Application for ${app.title} at ${app.companyName}`}>
              <List.Item.Meta
                avatar={<Avatar src={app.companyLogo} aria-label={`${app.companyName} Logo`} />}
                title={
                  <Link href={`/linkedin/company/${app.companyId}`} aria-label={`Company ${app.companyName}`}>
                    {app.title} at {app.companyName}
                  </Link>
                }
                description={`Applied on ${new Date(app.date).toLocaleDateString()}`}
              />
              <Tag color="blue" aria-label={`Application Status: ${app.status}`}>{app.status}</Tag>
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default ApplicationStatus;
