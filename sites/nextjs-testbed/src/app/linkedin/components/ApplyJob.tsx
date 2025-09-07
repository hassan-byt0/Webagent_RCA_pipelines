"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { message } from "antd";
import companies from "../data/companies";
import users, { User } from "../data/users";
import JobApplicationModal from "./JobApplicationModal";

const ApplyJob: React.FC = () => {
  const params = useParams();
  const router = useRouter();

  const { companyId, jobId } = params;

  const [currentUser] = useState<User | undefined>(
    users.find((u) => u.id === "1")
  );
  const company = companies.find((c) => c.id === companyId);
  const job = company?.jobPostings?.find((j) => j.id === jobId);

  const [isModalVisible, setIsModalVisible] = useState<boolean>(false);

  useEffect(() => {
    if (!company || !job) {
      message.error("Job not found.");
      router.back();
    } else {
      setIsModalVisible(true);
    }
  }, [company, job, router]);

  const handleApply = (): void => {
    if (currentUser && company && job) {
      const newApplication = {
        jobId: job.id,
        companyId: company.id,
        title: job.title,
        date: new Date().toISOString(),
        status: "Submitted",
      };
      currentUser.applications.push(newApplication);
      message.success("Application submitted successfully!");
      setIsModalVisible(false);
      router.push("/linkedin/applications");
    }
  };

  const handleModalClose = (): void => {
    setIsModalVisible(false);
    router.back();
  };

  if (!job || !company) return null;

  return (
    <JobApplicationModal
      visible={isModalVisible}
      job={{ ...job, companyName: company.name }}
      onClose={handleModalClose}
      onApply={handleApply}
      currentUserId={currentUser?.id || ""}
      aria-label={`Apply for ${job.title} at ${company.name}`}
    />
  );
};

export default ApplyJob;
