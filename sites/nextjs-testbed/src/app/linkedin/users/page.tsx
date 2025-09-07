"use client";

import { Card, List, Avatar } from "antd";
import Link from "next/link";
import users from "../data/users";

const UsersPage: React.FC = () => {
  return (
    <div className="p-4 max-w-3xl mx-auto">
      <Card className="shadow-md rounded-lg">
        <h2 className="text-2xl font-semibold mb-4 text-gray-800">Users</h2>
        <p className="text-gray-600 mb-6">
          Explore users you might want to connect with:
        </p>

        <List
          dataSource={users}
          renderItem={(user) => (
            <List.Item
              className="border-b py-4"
              id={`user-item-${user.id}`}
              aria-label={`User item for ${user.name}`}
            >
              <List.Item.Meta
                avatar={<Avatar src={user.avatar} aria-label={`Avatar of ${user.name}`} />}
                title={
                  <Link 
                    href={`/linkedin/user/${user.id}`} 
                    id={`user-link-${user.id}`} 
                    aria-label={`View profile of ${user.name}`}
                  >
                    {user.name}
                  </Link>
                }
                description={user.title}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default UsersPage;
