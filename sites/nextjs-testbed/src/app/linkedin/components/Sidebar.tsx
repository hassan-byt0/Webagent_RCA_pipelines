"use client";

import React, { useState } from "react";
import { Card, Avatar, List, Button, notification } from "antd";
import Link from "next/link";
import users from "../data/users";
import companies from "../data/companies";
import { useId } from "react-id-generator";

const LinkedInSidebar: React.FC = () => {
  const [currentUser, setCurrentUser] = useState(
    users.find((u) => u.id === "1")
  );

  // Generate unique IDs for sidebar elements
  const [
    asideId,
    userCardId,
    userNameId,
    userTitleId,
    userCompanyLinkId,
    viewProfileLinkId,
    pendingConnectionsCardId,
    pendingConnectionsListId,
  ] = useId(10, "linkedin-sidebar-");

  if (!currentUser) return null;

  const pendingRequests = users.filter((user) =>
    currentUser.pendingConnections.includes(user.id)
  );

  const handleAcceptConnection = (userId: string, userName: string) => {
    const requester = users.find((u) => u.id === userId);
    if (requester) {
      currentUser.connections.push(userId);
      requester.connections.push(currentUser.id);
      currentUser.pendingConnections = currentUser.pendingConnections.filter(
        (id) => id !== userId
      );
      setCurrentUser({ ...currentUser });
      notification.success({
        message: "Connection Accepted",
        description: `You have successfully connected with ${userName}.`,
        placement: "topRight",
      });
    }
  };

  return (
    <aside
      id="linkedin-sidebar"
      className="w-64 bg-white border-r border-gray-200 p-4 space-y-4"
      aria-label="LinkedIn Sidebar"
    >
      <Card id="sidebar-user-card" className="shadow-md rounded-lg" aria-label="User Information">
        <div className="flex flex-col items-center">
          <Avatar src={currentUser.avatar} aria-label={`${currentUser.name}'s avatar`} />
          <h3 id="sidebar-user-name" className="mt-3 text-lg font-semibold">
            {currentUser.name}
          </h3>
          <p id="sidebar-user-title" className="text-gray-500">
            {currentUser.title}
          </p>
          {currentUser.companyId && (
            <p className="mt-2 text-sm text-gray-600">
              Company:{" "}
              <Link
                id="sidebar-user-company-link"
                href={`/linkedin/company/${currentUser.companyId}`}
                aria-label={`View profile of ${companies.find((c) => c.id === currentUser.companyId)?.name}`}
              >
                {companies.find((c) => c.id === currentUser.companyId)?.name}
              </Link>
            </p>
          )}
        </div>
        <div className="mt-3 text-center">
          <Link
            id="sidebar-view-profile-link"
            href={`/linkedin/user/${currentUser.id}`}
            aria-label="View Your Profile"
          >
            View Profile
          </Link>
        </div>
      </Card>

      {pendingRequests.length > 0 && (
        <Card
          id="pending-connections-card"
          title="Pending Connections"
          className="shadow-md rounded-lg"
          aria-label="Pending Connection Requests"
        >
          <List
            id="pending-connections-list"
            dataSource={pendingRequests}
            renderItem={(user) => (
              <List.Item
                key={user.id}
                className="border-b flex justify-between items-center"
                id={`pending-connection-item-${user.id}`}
                aria-label={`Pending connection request from ${user.name}`}
              >
                <div className="flex items-center space-x-2">
                  <Avatar src={user.avatar} aria-label={`${user.name}'s avatar`} />
                  <Link
                    id={`pending-connection-link-${user.id}`}
                    href={`/linkedin/user/${user.id}`}
                    aria-label={`View profile of ${user.name}`}
                  >
                    {user.name}
                  </Link>
                </div>
                <Button
                  id={`accept-connection-button-${user.id}`}
                  type="primary"
                  size="small"
                  onClick={() => handleAcceptConnection(user.id, user.name)}
                  aria-label={`Accept connection request from ${user.name}`}
                >
                  Accept
                </Button>
              </List.Item>
            )}
          />
        </Card>
      )}

      {/* 
      <Card title="Companies" className="shadow-md rounded-lg">
        <List
          dataSource={companies}
          renderItem={(company) => (
            <List.Item className="border-b py-2">
              <List.Item.Meta
                avatar={<Avatar src={company.logo} />}
                title={
                  <Link href={`/linkedin/company/${company.id}`}>
                    {company.name}
                  </Link>
                }
                description={company.industry}
              />
            </List.Item>
          )}
        />
      </Card> 
      */}
    </aside>
  );
};

export default LinkedInSidebar;
