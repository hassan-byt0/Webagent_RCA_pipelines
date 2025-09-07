// src/components/health/Messages.jsx

import React, { useState } from "react";
import { Layout, List, Avatar, Input, Button } from "antd";
import users from "./data/users";
import { MessageOutlined } from "@ant-design/icons";

const { Content } = Layout;

const Messages = () => {
  const currentUser = users.find((u) => u.id === "1"); // Replace with actual user ID
  const [messages, setMessages] = useState(currentUser.messages);
  const [newMessage, setNewMessage] = useState("");

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      setMessages([
        ...messages,
        {
          sender: "You",
          text: newMessage,
          timestamp: new Date().toISOString(),
        },
      ]);
      setNewMessage("");
    }
  };

  return (
    <Content id="messages-content" className="messages-content" aria-label="Messages Section">
      <h2 id="messages-header">Messages</h2>

      <List
        id="messages-list"
        dataSource={messages}
        renderItem={(msg) => (
          <List.Item>
            <List.Item.Meta
              avatar={<Avatar icon={<MessageOutlined />} />}
              title={msg.sender}
              description={msg.text}
            />
          </List.Item>
        )}
        aria-label="List of Messages"
      />

      <Input.TextArea
        id="new-message-input"
        rows={2}
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        placeholder="Type your message..."
        aria-label="New Message Input"
      />
      <Button
        id="send-message-button"
        type="primary"
        onClick={handleSendMessage}
        style={{ marginTop: "10px" }}
        aria-label="Send Message Button"
      >
        Send
      </Button>
    </Content>
  );
};

export default Messages;
