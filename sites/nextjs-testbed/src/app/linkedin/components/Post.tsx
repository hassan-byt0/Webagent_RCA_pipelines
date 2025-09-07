"use client";

import React from "react";
import { Card, Avatar } from "antd";
import Link from "next/link";
import Image from "next/image";
import companies from "../data/companies";
import { PostType } from "../types";
import ReactMarkdown from "react-markdown";
import { useId } from "react-id-generator";

interface PostProps {
  post: PostType;
}

const Post: React.FC<PostProps> = ({ post }) => {
  const company: any = post.companyId
    ? companies.find((c: any) => c.id === post.companyId)
    : undefined;

  // Generate unique IDs for post elements
  const [cardId, coverImageId, companyLinkId, authorNameId] = useId(7, "post-");

  return (
    <Card
      id={cardId}
      className="mb-4 shadow-md rounded-lg"
      cover={
        post.image && (
          <Image
            id={coverImageId}
            alt="post"
            src={post.image}
            width={post.width}
            height={post.height}
            className="object-cover"
            aria-label="Post Image"
          />
        )
      }
    >
      <Card.Meta
        avatar={
          company ? (
            <Link href={`/linkedin/company/${company.id}`} aria-label={`Company ${company.name}`}>
              <Avatar src={post.avatar} aria-label="Author Avatar" />
            </Link>
          ) : (
            <Avatar src={post.avatar} aria-label="Author Avatar" />
          )
        }
        title={
          <div className="flex items-center space-x-2">
            <span id={authorNameId} className="font-semibold text-gray-800">
              {post.author}
            </span>
            {company && (
              <span className="text-sm text-gray-500">
                at{" "}
                <Link
                  id={companyLinkId}
                  href={`/linkedin/company/${company.id}`}
                  aria-label={`Company Link ${company.name}`}
                >
                  {company.name}
                </Link>
              </span>
            )}
          </div>
        }
        description={
          <ReactMarkdown className="text-gray-700">
            {post.content}
          </ReactMarkdown>
        }
      />
    </Card>
  );
};

export default Post;
