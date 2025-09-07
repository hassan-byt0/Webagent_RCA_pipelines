"use client";

import React, { useState, useContext } from "react";
import { Card, Input, Button, message } from "antd";
import { useRouter } from "next/navigation";
import users from "../data/users";
import { PostsContext } from "../context/PostsContext";
import { useId } from "react-id-generator";

const { TextArea } = Input;

const CreatePost: React.FC = () => {
  const [newPostContent, setNewPostContent] = useState<string>("");
  const [newPostImage, setNewPostImage] = useState<string>("");
  const router = useRouter();
  const [textAreaId, inputId, buttonId] = useId(3, "create-post-");

  const currentUser = users.find((u) => u.id === "1");
  const { addPost } = useContext(PostsContext);

  const handleCreatePost = () => {
    if (newPostContent.trim()) {
      const newPost = {
        id: Date.now(),
        author: currentUser?.name || "Unknown",
        content: newPostContent,
        avatar: currentUser?.avatar || "",
        image: newPostImage,
        companyId: currentUser?.companyId || undefined,
      };
      addPost(newPost);
      message.success("Post created successfully!");
      setNewPostContent("");
      setNewPostImage("");
      router.push("/linkedin");
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <Card className="shadow-md rounded-lg">
        <TextArea
          id={textAreaId}
          placeholder="Start a post"
          value={newPostContent}
          onChange={(e) => setNewPostContent(e.target.value)}
          autoSize={{ minRows: 3, maxRows: 6 }}
          className="mb-2"
          aria-label="New Post Content"
        />
        <Input
          id={inputId}
          placeholder="Image URL (optional)"
          value={newPostImage}
          onChange={(e) => setNewPostImage(e.target.value)}
          className="mb-2"
          aria-label="Image URL"
        />
        <Button
          id={buttonId}
          type="primary"
          onClick={handleCreatePost}
          className="float-right"
          aria-label="Post Button"
        >
          Post
        </Button>
      </Card>
    </div>
  );
};

export default CreatePost;
