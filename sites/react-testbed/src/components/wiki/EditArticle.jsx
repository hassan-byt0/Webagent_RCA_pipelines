import React from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Form, Input, Button, Typography } from "antd";

const { Paragraph } = Typography;

const EditArticle = ({ articles, onUpdate }) => {
  const { articleId } = useParams();
  const navigate = useNavigate();
  const article = articles.find((item) => item.id === articleId);

  const [form] = Form.useForm();

  if (!article) {
    return (
      <div className="edit-article-not-found">
        <h2>Article Not Found</h2>
        <p>The article you are trying to edit does not exist.</p>
        <Button type="primary" onClick={() => navigate("/")}>
          Return to Home
        </Button>
      </div>
    );
  }

  const formatContent = (content) => {
    const paragraphs = content.split("\n\n"); // Split content into paragraphs
    return paragraphs.map((para, paraIndex) => {
      const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
      const parts = [];
      let lastIndex = 0;
      let match;

      while ((match = linkRegex.exec(para)) !== null) {
        const [full, text, url] = match;
        const index = match.index;

        if (index > lastIndex) {
          parts.push(para.substring(lastIndex, index));
        }

        parts.push(
          <Link key={`link-${paraIndex}-${index}`} to={`/wiki/${url}`}>
            {text}
          </Link>
        );

        lastIndex = index + full.length;
      }

      if (lastIndex < para.length) {
        parts.push(para.substring(lastIndex));
      }

      return (
        <Paragraph key={`para-${paraIndex}`} style={{ marginBottom: "16px" }}>
          {parts}
        </Paragraph>
      );
    });
  };

  const onFinish = (values) => {
    const updatedArticle = {
      ...article,
      title: values.title,
      content: values.content,
    };
    onUpdate(updatedArticle); // This will navigate to `/wiki/:articleId`
  };

  return (
    <div className="edit-article-page">
      <h2>Edit Article</h2>
      <Form
        form={form}
        layout="vertical"
        initialValues={{ title: article.title, content: article.content }}
        onFinish={onFinish}
      >
        <Form.Item
          label="Title"
          name="title"
          rules={[
            { required: true, message: "Please input the article title!" },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Content"
          name="content"
          rules={[
            { required: true, message: "Please input the article content!" },
          ]}
        >
          <Input.TextArea rows={10} />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save Changes
          </Button>
          <Button style={{ marginLeft: "10px" }} onClick={() => navigate(-1)}>
            Cancel
          </Button>
        </Form.Item>
      </Form>
      <div className="article-content">{formatContent(article.content)}</div>
    </div>
  );
};

export default EditArticle;
