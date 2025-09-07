"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, Avatar, Button, Typography } from "antd";
import Link from "next/link";
import users, { User } from "../data/users";
import companies from "../data/companies";
import { useId } from "react-id-generator";

const { Paragraph } = Typography;

const UserProfile: React.FC = () => {
  const params = useParams();
  const router = useRouter();
  const { userId } = params;

  const [user] = useState<User | undefined>(users.find((u) => u.id === userId));

  // Generate unique IDs for profile elements
  const [
    containerId,
    cardId,
    userNameId,
    userTitleId,
    companyLinkId,
    aboutParagraphId,
    editProfileLinkId,
  ] = useId(8, "user-profile-");

  useEffect(() => {
    if (!user) {
      router.back();
    }
  }, [user, router]);

  if (!user) {
    return (
      <div id={`${containerId}-not-found`} className="p-4">
        User not found.
      </div>
    );
  }

  const isCurrentUser = user.isCurrentUser;
  const company = user.companyId
    ? companies.find((c) => c.id === user.companyId)
    : undefined;

  return (
    <div id="user-profile-container" className="max-w-2xl mx-auto p-4">
      <Card id="user-profile-card" className="shadow-md rounded-lg" aria-label="User Profile Card">
        <div className="flex flex-col items-center">
          <Avatar size={100} src={user.avatar} aria-label={`${user.name}'s avatar`} />
          <h2 id="user-name" className="text-2xl font-semibold mt-4 text-gray-800">
            {user.name}
          </h2>
          <h3 id="user-title" className="text-lg text-gray-600">
            {user.title}
          </h3>
          {company && (
            <p className="mt-2 text-gray-600">
              Company:{" "}
              <Link 
                id="user-company-link" 
                href={`/linkedin/company/${company.id}`} 
                aria-label={`View profile of ${company.name}`}
              >
                {company.name}
              </Link>
            </p>
          )}
        </div>
        <div className="mt-4">
          <Paragraph id="user-about" className="text-gray-700">
            {user.about}
          </Paragraph>
        </div>
        {isCurrentUser && (
          <div className="mt-4 flex justify-end">
            <Link
              id="edit-profile-link"
              href={`/linkedin/user/${user.id}/edit`}
              aria-label="Edit Profile"
            >
              <Button type="primary" aria-label="Edit Profile Button">Edit Profile</Button>
            </Link>
          </div>
        )}
      </Card>
    </div>
  );
};

export default UserProfile;
