"use client";

import React, { useState } from "react";
import { Card, Avatar, List, Button, message } from "antd";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import companies, { Company, JobPosting } from "../data/companies";
import users from "../data/users";
import JobApplicationModal from "./JobApplicationModal";

const CompanyProfile: React.FC = () => {
  const params = useParams();
  const { companyId } = params;
  const router = useRouter();

  const company: Company | undefined = companies.find(
    (c) => c.id === companyId
  );
  const [currentUser] = useState(users.find((u) => u.id === "1"));
  const [selectedJob, setSelectedJob] = useState<JobPosting | null>(null);
  const [isModalVisible, setIsModalVisible] = useState<boolean>(false);

  if (!company) {
    return <div className="p-4">Company not found.</div>;
  }

  const employees = users.filter((u) => company.employees.includes(u.id));

  const handleApplyNow = (job: JobPosting) => {
    setSelectedJob(job);
    setIsModalVisible(true);
  };

  const handleApply = () => {
    if (currentUser && selectedJob) {
      const newApplication = {
        jobId: selectedJob.id,
        companyId: company.id,
        title: selectedJob.title,
        date: new Date().toISOString(),
        status: "Submitted",
      };
      currentUser.applications.push(newApplication);
      message.success("Application submitted successfully!");
      setIsModalVisible(false);
      router.push("/linkedin/applications");
    }
  };

  const handleModalClose = () => {
    setIsModalVisible(false);
    setSelectedJob(null);
  };

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      <Card className="shadow-md rounded-lg text-center">
        <Avatar size={100} src={company.logo} className="mx-auto" />
        <h2 className="text-2xl font-semibold mt-4 text-gray-800">
          {company.name}
        </h2>
        <h3 className="text-lg text-gray-600">{company.industry}</h3>
        <p className="mt-2 text-gray-700">{company.about}</p>
      </Card>

      {company.jobPostings && company.jobPostings.length > 0 && (
        <Card title="Job Postings" className="shadow-md rounded-lg">
          <List
            dataSource={company.jobPostings}
            renderItem={(job) => (
              <List.Item className="border-b py-4 flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <h4 className="text-lg font-semibold">{job.title}</h4>
                  <p className="text-gray-600">
                    {job.location} - ${job.salary} - {job.jobType}
                  </p>
                  <p className="text-gray-700 mt-2">{job.description}</p>
                </div>
                <Button
                  type="primary"
                  className="mt-2 md:mt-0"
                  onClick={() => handleApplyNow(job)}
                  aria-label={`Apply Now for ${job.title}`}
                >
                  Apply Now
                </Button>
              </List.Item>
            )}
          />
        </Card>
      )}

      {employees.length > 0 && (
        <Card title="Employees" className="shadow-md rounded-lg">
          <List
            dataSource={employees}
            renderItem={(user) => (
              <List.Item className="border-b py-4">
                <List.Item.Meta
                  avatar={<Avatar src={user.avatar} />}
                  title={
                    <Link href={`/linkedin/user/${user.id}`} aria-label={`Employee ${user.name}`}>
                      {user.name}
                    </Link>
                  }
                  description={user.title}
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {selectedJob && (
        <JobApplicationModal
          visible={isModalVisible}
          job={{ ...selectedJob, companyName: company.name }}
          onClose={handleModalClose}
          onApply={handleApply}
          currentUserId={currentUser?.id || ""}
        />
      )}
    </div>
  );
};

export default CompanyProfile;
