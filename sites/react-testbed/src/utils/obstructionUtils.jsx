// src/utils/obstructionUtils.js

import { Modal, Form, Input, notification } from "antd";

/**
 * Obstruction steps for accepting a connection request.
 * @param {Function} onSuccess - Callback function after successful acceptance.
 * @param {String} userName - Name of the user being connected.
 */
export const obstructAcceptConnection = (onSuccess, userName) => {
  Modal.confirm({
    title: "Are you sure you want to accept this connection?",
    content: "By accepting, you agree to share your profile information.",
    okText: "Yes, Accept",
    cancelText: "Cancel",
    onOk() {
      Modal.warning({
        title: "Re-authentication Required",
        content: (
          <div>
            <p>Please re-enter your password to confirm your identity.</p>
            <Form layout="vertical">
              <Form.Item label="Password" required>
                <Input.Password placeholder="Enter your password" />
              </Form.Item>
            </Form>
          </div>
        ),
        okText: "Confirm",
        cancelText: "Cancel",
        onOk() {
          Modal.success({
            title: "Connection Accepted",
            content: `You have successfully accepted the connection request from ${userName}.`,
            onOk() {
              notification.success({
                message: "Success",
                description: `${userName} is now in your connections.`,
                placement: "topRight",
              });
              onSuccess();
            },
          });
        },
      });
    },
  });
};

/**
 * Obstruction steps for summarizing profile information.
 * @param {Function} onSuccess - Callback function after successful summarization.
 */
export const obstructSummarizeProfile = (onSuccess) => {
  Modal.confirm({
    title: "Do you want to summarize this profile?",
    content:
      "This action will compile and summarize the profile information. Proceed?",
    okText: "Yes, Summarize",
    cancelText: "Cancel",
    onOk() {
      Modal.info({
        title: "Preparing Summary",
        content: "We are compiling the profile information. Please wait...",
        okText: "Done",
        onOk() {
          Modal.success({
            title: "Summary Complete",
            content: "Profile information has been summarized successfully.",
            onOk() {
              notification.success({
                message: "Success",
                description: "Profile summary is ready.",
                placement: "topRight",
              });
              onSuccess();
            },
          });
        },
      });
    },
  });
};
