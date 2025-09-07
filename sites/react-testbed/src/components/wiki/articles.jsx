// components/wiki/Articles.js

import React from "react";
import { Link } from "react-router-dom";

const articles = [
  {
    id: "react",
    title: "React (JavaScript library)",
    content:
      "React is an open-source, front-end JavaScript library for building user interfaces or UI components.\n\nIt is maintained by [Facebook](articles/facebook) and a community of individual developers and companies.\n\nReact can be used as a base in the development of single-page or mobile applications.\n\nIts component-based architecture allows for reusable code and efficient rendering.\n\nRelated articles: [JavaScript](articles/javascript), [Web Development](articles/web-development), [Frontend](articles/frontend).",
  },
  {
    id: "javascript",
    title: "JavaScript",
    content:
      "JavaScript, often abbreviated as JS, is a programming language that conforms to the ECMAScript specification.\n\nJavaScript is high-level, often just-in-time compiled, and multi-paradigm.\n\nIt has curly-bracket syntax, dynamic typing, prototype-based object-orientation, and first-class functions.\n\nJavaScript is essential for creating interactive and dynamic web pages.\n\nRelated articles: [Programming Language](articles/programming-language), [React](articles/react), [Node.js](articles/nodejs).",
  },
  {
    id: "social-networking",
    title: "Social Networking",
    content:
      "Social networking is the use of dedicated websites and applications to interact with other users, or to find people with similar interests to oneself.\n\nMany websites and applications facilitate social networking, including MySpace, Facebook, Instagram, Twitter, and LinkedIn.\n\nSocial networking has become a key component of modern life, influencing how people communicate and interact.\n\nIt plays a significant role in marketing, information dissemination, and personal relationships.\n\nRelated articles: [Facebook](articles/facebook), [Instagram](articles/instagram), [Twitter](articles/twitter).",
  },
  {
    id: "facebook",
    title: "Facebook",
    content:
      "Facebook is a social networking service owned by Meta Platforms.\n\nUsers can post status updates, share photos, and connect with friends and family.\n\nIt offers various features such as groups, events, and marketplace.\n\nFacebook has a significant impact on global communication and information sharing.\n\nRelated articles: [Instagram](articles/instagram), [WhatsApp](articles/whatsapp), [Meta Platforms](articles/meta).",
  },
  {
    id: "instagram",
    title: "Instagram",
    content:
      "Instagram is a photo and video-sharing social networking service owned by Meta Platforms.\n\nUsers can upload media that can be edited with filters and organized with tags and location information.\n\nIt offers features like Stories, IGTV, and Reels to enhance user engagement.\n\nInstagram plays a crucial role in digital marketing and influencer culture.\n\nRelated articles: [Facebook](articles/facebook), [WhatsApp](articles/whatsapp), [Meta Platforms](articles/meta).",
  },
  // Add more articles as needed
];

export default articles;
