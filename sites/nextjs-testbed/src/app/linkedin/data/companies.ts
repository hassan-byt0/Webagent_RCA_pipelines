// app/linkedin/data/companies.ts

export interface JobPosting {
  id: string;
  title: string;
  location: string;
  salary: number;
  jobType: string;
  description: string;
}

export interface Company {
  id: string;
  name: string;
  industry: string;
  logo: string;
  about: string;
  employees: string[]; // Array of user IDs
  jobPostings?: JobPosting[];
}

const companies: Company[] = [
  {
    id: "1",
    name: "TechCorp Global LTD",
    industry: "Information Technology",
    logo: "https://logo.clearbit.com/techcorp.com",
    about:
      "Information technology consultancy activities. Registered office address: 229 Lordship Lane, London, England, SE22 8JF. Incorporated on 13 June 2017.",
    employees: ["1"],
    jobPostings: [
      {
        id: "job1",
        title: "Senior Software Engineer",
        location: "London",
        salary: 90000,
        jobType: "Full-time",
        description:
          "We are looking for a Senior Software Engineer with experience in full-stack development...",
      },
      // Add more job postings as needed
    ],
  },
  {
    id: "2",
    name: "Purdue University",
    industry: "Higher Education",
    logo: "https://logo.clearbit.com/purdue.edu",
    about:
      "A public land-grant research university in West Lafayette, Indiana, United States. Known for competitive engineering curricula, aviation programs, and producing 26 astronauts. Offers over 211 major areas of study across various colleges including Engineering, Science, Liberal Arts, and more.",
    employees: [],
    jobPostings: [
      {
        id: "job2",
        title: "Assistant Professor",
        location: "West Lafayette",
        salary: 70000,
        jobType: "Full-time",
        description:
          "Seeking candidates for a tenure-track position in Computer Science...",
      },
    ],
  },
  {
    id: "3",
    name: "Google",
    industry: "Technology",
    logo: "https://logo.clearbit.com/google.com",
    about:
      "A multinational technology company specializing in internet-related services and products, including search engine, cloud computing, software, and hardware.",
    employees: ["4", "6"],
    jobPostings: [
      {
        id: "job3",
        title: "Frontend Developer",
        location: "Mountain View",
        salary: 120000,
        jobType: "Full-time",
        description:
          "Seeking a Frontend Developer with expertise in React and Redux...",
      },
      {
        id: "job4",
        title: "UX Designer",
        location: "Mountain View",
        salary: 110000,
        jobType: "Full-time",
        description:
          "Looking for a UX Designer with experience in user research...",
      },
      // ...more job postings...
    ],
  },
  {
    id: "4",
    name: "Stanford University",
    industry: "Higher Education",
    logo: "https://logo.clearbit.com/stanford.edu",
    about:
      "A private research university in Stanford, California. Known for its academic strength, wealth, proximity to Silicon Valley, and ranking as one of the world's top universities.",
    employees: ["4"],
    jobPostings: [
      {
        id: "job5",
        title: "Research Assistant",
        location: "Stanford",
        salary: 50000,
        jobType: "Part-time",
        description:
          "Assist in ongoing research projects in the Computer Science department...",
      },
      {
        id: "job6",
        title: "Data Analyst",
        location: "Stanford",
        salary: 60000,
        jobType: "Full-time",
        description:
          "Analyze and interpret complex data sets related to ongoing studies...",
      },
    ],
  },
  {
    id: "5",
    name: "Yelp",
    industry: "Technology",
    logo: "https://logo.clearbit.com/yelp.com",
    about:
      "An American company that develops, hosts and markets the Yelp.com website and mobile app, which publishes crowd-sourced reviews about businesses.",
    employees: ["5"],
    // No jobPostings
  },
  {
    id: "6",
    name: "Amazon",
    industry: "E-commerce",
    logo: "https://logo.clearbit.com/amazon.com",
    about:
      "A multinational technology company focusing on e-commerce, cloud computing, and artificial intelligence.",
    employees: ["7", "8"],
    jobPostings: [
      {
        id: "job7",
        title: "Cloud Solutions Architect",
        location: "Seattle",
        salary: 130000,
        jobType: "Full-time",
        description:
          "Design and implement AWS cloud solutions for enterprise clients...",
      },
      {
        id: "job8",
        title: "Logistics Manager",
        location: "Seattle",
        salary: 90000,
        jobType: "Full-time",
        description:
          "Oversee and coordinate logistics operations across multiple warehouses...",
      },
    ],
  },
  {
    id: "7",
    name: "Microsoft",
    industry: "Technology",
    logo: "https://logo.clearbit.com/microsoft.com",
    about:
      "A multinational technology company producing computer software, consumer electronics, and related services.",
    employees: ["9"],
    jobPostings: [
      {
        id: "job9",
        title: "Software Engineer II",
        location: "Redmond",
        salary: 115000,
        jobType: "Full-time",
        description:
          "Contribute to the development of Windows OS features and updates...",
      },
      {
        id: "job10",
        title: "Product Manager",
        location: "Redmond",
        salary: 125000,
        jobType: "Full-time",
        description:
          "Lead cross-functional teams to deliver innovative software products...",
      },
    ],
  },
  {
    id: "8",
    name: "Facebook",
    industry: "Technology",
    logo: "https://logo.clearbit.com/facebook.com",
    about:
      "An online social media and social networking service owned by Meta Platforms.",
    employees: ["10"],
    jobPostings: [
      {
        id: "job11",
        title: "Data Scientist",
        location: "Menlo Park",
        salary: 130000,
        jobType: "Full-time",
        description:
          "Analyze user data to improve user engagement and experience...",
      },
      {
        id: "job12",
        title: "Backend Engineer",
        location: "Menlo Park",
        salary: 125000,
        jobType: "Full-time",
        description:
          "Develop scalable backend systems using PHP and GraphQL...",
      },
    ],
  },
  {
    id: "9",
    name: "Tesla",
    industry: "Automotive",
    logo: "https://logo.clearbit.com/tesla.com",
    about:
      "An American electric vehicle and clean energy company based in Palo Alto, California.",
    employees: ["11"],
    jobPostings: [
      {
        id: "job13",
        title: "Mechanical Engineer",
        location: "Palo Alto",
        salary: 110000,
        jobType: "Full-time",
        description:
          "Design and develop mechanical components for electric vehicles...",
      },
      {
        id: "job14",
        title: "Battery Technician",
        location: "Reno",
        salary: 70000,
        jobType: "Full-time",
        description:
          "Work on battery production and testing at Gigafactory Nevada...",
      },
    ],
  },
  {
    id: "10",
    name: "Apple Inc.",
    industry: "Technology",
    logo: "https://logo.clearbit.com/apple.com",
    about:
      "A multinational technology company that designs, develops, and sells consumer electronics, computer software, and online services.",
    employees: ["12"],
    jobPostings: [
      {
        id: "job15",
        title: "iOS Developer",
        location: "Cupertino",
        salary: 125000,
        jobType: "Full-time",
        description: "Develop applications and features for iOS devices...",
      },
      {
        id: "job16",
        title: "Hardware Engineer",
        location: "Cupertino",
        salary: 130000,
        jobType: "Full-time",
        description:
          "Design and test hardware components for Apple products...",
      },
    ],
  },
];

export default companies;
