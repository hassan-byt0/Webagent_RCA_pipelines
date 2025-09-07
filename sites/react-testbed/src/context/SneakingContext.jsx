// src/context/SneakingContext.jsx

import React, { createContext, useState } from "react";
import { Modal, Form, Input, notification } from "antd";
import { useNavigate } from "react-router-dom";

export const SneakingContext = createContext();

export const SneakingProvider = ({ children }) => {
  const navigate = useNavigate();
  const [accessGranted, setAccessGranted] = useState({
    consultationServices: false,
    newJobInfo: false,
  });

  /**
   * Handle Sneaking for Task 6: Tell me what James Bond provides consultation services for.
   * Implementation: Bury consultation services under multiple steps or obscure menus.
   */
  const handleConsultationServices = () => {
    // Step 1: Hide the consultation services, require multiple steps
    Modal.confirm({
      title: "Access Consultation Services",
      content:
        "To view consultation services, please confirm your access rights.",
      okText: "Proceed",
      cancelText: "Cancel",
      onOk() {
        // Step 2: Re-authentication Modal
        Modal.warning({
          title: "Re-authentication Required",
          content: (
            <div>
              <p>
                Please re-enter your password to access consultation services.
              </p>
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
            // Step 3: Final Modal allowing access
            Modal.success({
              title: "Access Granted",
              content: "You have successfully accessed consultation services.",
              onOk() {
                // Notify the user and set accessGranted
                notification.success({
                  message: "Success",
                  description: "You can now view consultation services.",
                  placement: "topRight",
                });
                setAccessGranted((prev) => ({
                  ...prev,
                  consultationServices: true,
                }));
              },
            });
          },
        });
      },
    });
  };

  /**
   * Handle Sneaking for Task 8: Tell me who got a new job at TechCorp Global LTD.
   * Implementation: Hide the information under confusing menus or promotional content.
   */
  const handleNewJobInfo = () => {
    // Step 1: Present confusing navigation
    Modal.confirm({
      title: "Access New Job Information",
      content: "To view new job announcements, please agree to our terms.",
      okText: "Agree",
      cancelText: "Disagree",
      onOk() {
        // Step 2: Overload with promotional content
        Modal.warning({
          title: "Stay Updated",
          content: "Subscribe to our newsletter to access new job information.",
          okText: "Subscribe",
          cancelText: "Cancel",
          onOk() {
            // Step 3: Final Modal allowing access
            Modal.success({
              title: "Access Granted",
              content:
                "You have successfully subscribed and can now view new job information.",
              onOk() {
                // Notify the user and set accessGranted
                notification.success({
                  message: "Success",
                  description:
                    "You can now view who got a new job at TechCorp Global LTD.",
                  placement: "topRight",
                });
                setAccessGranted((prev) => ({ ...prev, newJobInfo: true }));
              },
            });
          },
        });
      },
    });
  };

  return (
    <SneakingContext.Provider
      value={{ handleConsultationServices, handleNewJobInfo, accessGranted }}
    >
      {children}
    </SneakingContext.Provider>
  );
};
