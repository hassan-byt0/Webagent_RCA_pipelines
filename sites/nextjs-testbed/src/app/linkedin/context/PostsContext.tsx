// app/linkedin/context/PostsContext.tsx
"use client";

import React, { createContext, useState, ReactNode } from "react";
import { PostType } from "../types";
import initialPosts from "../data/posts";

interface PostsContextProps {
  posts: PostType[];
  addPost: (post: PostType) => void;
}

export const PostsContext = createContext<PostsContextProps>({
  posts: [],
  addPost: () => {},
});

export const PostsProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [posts, setPosts] = useState<PostType[]>(() => {
    return [...initialPosts].sort((a, b) =>
      a.sponsored === b.sponsored ? 0 : a.sponsored ? -1 : 1
    );
  });

  const addPost = (post: PostType) => {
    setPosts([post, ...posts]);
  };

  return (
    <PostsContext.Provider value={{ posts, addPost }}>
      {children}
    </PostsContext.Provider>
  );
};
