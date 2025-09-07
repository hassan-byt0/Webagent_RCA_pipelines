"use client";

import React, { Suspense } from "react";
import { Card, List, Avatar, Typography } from "antd";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import users from "../data/users";
import companies from "../data/companies";
import { useId } from "react-id-generator";

const { Text } = Typography;

const SearchResultsContent: React.FC = () => {
  const searchParams = useSearchParams();
  const query = searchParams.get("q")?.toLowerCase() || "";
  const locationFilter = searchParams.get("location")?.toLowerCase() || "";
  const salaryFilter = searchParams.get("salary")?.toLowerCase() || "";
  const jobTypeFilter = searchParams.get("jobType")?.toLowerCase() || "";

  // Filter users
  const filteredUsers = users.filter((user) => {
    const matchesQuery = user.name.toLowerCase().includes(query);
    const matchesLocation = locationFilter
      ? user.location.toLowerCase().includes(locationFilter)
      : true;
    const matchesJobType = jobTypeFilter
      ? user.jobType.toLowerCase().includes(jobTypeFilter)
      : true;
    const matchesSalary = salaryFilter
      ? user.salary.toString().includes(salaryFilter)
      : true;
    return matchesQuery && matchesLocation && matchesJobType && matchesSalary;
  });

  // Flatten all job postings from companies
  const allJobPostings = companies.flatMap(
    (company) =>
      company.jobPostings?.map((job) => ({
        ...job,
        companyName: company.name,
        companyId: company.id,
      })) || []
  );

  const filteredJobs = allJobPostings.filter((job) => {
    const matchesQuery = job.title.toLowerCase().includes(query);
    const matchesLocation = locationFilter
      ? job.location.toLowerCase().includes(locationFilter)
      : true;
    const matchesJobType = jobTypeFilter
      ? job.jobType.toLowerCase().includes(jobTypeFilter)
      : true;
    const matchesSalary = salaryFilter
      ? job.salary.toString().includes(salaryFilter)
      : true;
    return matchesQuery && matchesLocation && matchesJobType && matchesSalary;
  });

  const filteredCompanies = companies.filter((company) =>
    company.name.toLowerCase().includes(query)
  );

  const noResults =
    filteredUsers.length === 0 &&
    filteredCompanies.length === 0 &&
    filteredJobs.length === 0;

  // Generate unique IDs for search results elements
  const [
    containerId,
    usersCardId,
    usersListId,
    jobsCardId,
    jobsListId,
    companiesCardId,
    companiesListId,
    noResultsId,
  ] = useId(8, "search-results-");

  return (
    <div id={containerId} className="p-4 max-w-3xl mx-auto">
      <Text
        id={`${containerId}-title`}
        className="text-2xl font-semibold mb-4 text-gray-800"
      >
        Search Results for &quot;{query}&quot;
      </Text>

      {filteredUsers.length > 0 && (
        <Card
          id={usersCardId}
          title="Users"
          className="mb-4 shadow-md rounded-lg"
        >
          <List
            id={usersListId}
            dataSource={filteredUsers}
            renderItem={(user) => (
              <List.Item
                key={user.id}
                className="border-b py-4"
                id={`search-user-item-${user.id}`}
                aria-label={`Search result for user ${user.name}`}
              >
                <List.Item.Meta
                  avatar={<Avatar src={user.avatar} aria-label={`${user.name}'s avatar`} />}
                  title={
                    <Link
                      href={`/linkedin/user/${user.id}`}
                      id={`search-user-link-${user.id}`}
                      aria-label={`View profile of ${user.name}`}
                    >
                      {user.name}
                    </Link>
                  }
                  description={`${user.title} - ${user.location} - $${user.salary} - ${user.jobType}`}
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {filteredJobs.length > 0 && (
        <Card
          id={jobsCardId}
          title="Job Postings"
          className="mb-4 shadow-md rounded-lg"
        >
          <List
            id={jobsListId}
            dataSource={filteredJobs}
            renderItem={(job) => (
              <List.Item
                key={job.id}
                className="border-b py-4"
                id={`search-job-item-${job.id}`}
                aria-label={`Search result for job ${job.title} at ${job.companyName}`}
              >
                <List.Item.Meta
                  avatar={
                    <Avatar
                      src={`https://logo.clearbit.com/${job.companyName
                        .toLowerCase()
                        .replace(/\s/g, "")}.com`}
                      aria-label={`${job.companyName} logo`}
                    />
                  }
                  title={
                    <Link
                      href={`/linkedin/company/${job.companyId}`}
                      id={`search-job-link-${job.id}`}
                      aria-label={`View job ${job.title} at ${job.companyName}`}
                    >
                      {job.title} at {job.companyName}
                    </Link>
                  }
                  description={`${job.location} - $${job.salary} - ${job.jobType}`}
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {filteredCompanies.length > 0 && (
        <Card
          id={companiesCardId}
          title="Companies"
          className="mb-4 shadow-md rounded-lg"
        >
          <List
            id={companiesListId}
            dataSource={filteredCompanies}
            renderItem={(company) => (
              <List.Item
                key={company.id}
                className="border-b py-4"
                id={`search-company-item-${company.id}`}
                aria-label={`Search result for company ${company.name}`}
              >
                <List.Item.Meta
                  avatar={<Avatar src={company.logo} aria-label={`${company.name} logo`} />}
                  title={
                    <Link
                      href={`/linkedin/company/${company.id}`}
                      id={`search-company-link-${company.id}`}
                      aria-label={`View profile of ${company.name}`}
                    >
                      {company.name}
                    </Link>
                  }
                  description={company.industry}
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {noResults && (
        <Text id={noResultsId} className="text-gray-700">
          No results found.
        </Text>
      )}
    </div>
  );
};

const SearchResults: React.FC = () => {
  // Generate unique ID for the Suspense fallback
  const [fallbackId] = useId(1, "search-results-fallback-");

  return (
    <Suspense fallback={<div id={fallbackId}>Loading search results...</div>}>
      <SearchResultsContent />
    </Suspense>
  );
};

export default SearchResults;
