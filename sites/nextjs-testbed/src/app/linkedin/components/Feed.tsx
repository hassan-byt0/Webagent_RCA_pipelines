"use client";

import React, { useContext } from "react";
import { List } from "antd";
import Post from "./Post";
import { PostsContext } from "../context/PostsContext";
import { useSearchParams } from "next/navigation";
import { useId } from "react-id-generator";

const Feed: React.FC = () => {
  const { posts } = useContext(PostsContext);
  const searchParams = useSearchParams();
  const darkpattern = searchParams.get("dp");

  // Generate unique IDs for elements
  const [listContainerId, listItemBaseId] = useId(2, "feed-");

  // Determine if the query parameter 'darkpattern=disguisedads' is present
  const showGooglePost = darkpattern === "da";

  // Filter posts based on the presence of 'darkpattern=disguisedads'
  const filteredPosts = posts.filter((post) => {
    if (post.id === 1) {
      return showGooglePost;
    }
    return post.id !== 1; // Exclude Google post unless condition is met
  });

  return (
    <div id={listContainerId} className="max-w-2xl mx-auto" aria-label="Post Feed">
      <List
        itemLayout="vertical"
        dataSource={filteredPosts}
        renderItem={(post, index) => (
          <Post key={`${listItemBaseId}-${index}`} post={post} />
        )}
      />
    </div>
  );
};

export default Feed;
