// app/linkedin/data/users.ts

export interface Application {
  jobId: string;
  companyId: string;
  title: string;
  date: string; // ISO string
  status: string;
}

export interface User {
  id: string;
  name: string;
  isCurrentUser?: boolean; // Indicates if this user is the logged-in user
  title: string;
  avatar: string;
  coverImage: string;
  about: string;
  consultationServices?: string;
  connections: string[]; // Array of user IDs
  pendingConnections: string[]; // Array of user IDs
  companyId: string | null;
  location: string;
  salary: number;
  jobType: string;
  applications: Application[];
}

const users: User[] = [
  {
    id: "1",
    name: "James Bond",
    isCurrentUser: true, // Mark as current user
    title: "Head of the 007 British Intelligence Service",
    avatar:
      "https://ui-avatars.com/api/?name=Jose+Marcial+Portilla&background=random",
    coverImage: "https://source.unsplash.com/random/800x200?person",
    about:
      "Known for Python for Machine Learning and Data Science BootCamp. Provides consultation services in data science and programming for Fortune 500 companies.",
    consultationServices:
      "Data Science and Programming for Fortune 500 companies.", // Added consultationServices
    connections: ["2", "3"],
    pendingConnections: ["4"],
    companyId: "1", // Associate with TechCorp Global LTD
    location: "London",
    salary: 85000,
    jobType: "Full-time",
    applications: [], // Add this array to store applications
  },
  {
    id: "2",
    name: "Koo Ping Shung",
    title: "Co-founder of DataScience SG",
    avatar: "https://ui-avatars.com/api/?name=Koo+Ping+Shung&background=random",
    coverImage: "https://source.unsplash.com/random/800x200?person",
    about:
      "Expert in AI ethics, Big Data analysis for business, and Machine Learning. Managed the 2015 Earth Hour project.",
    connections: ["1", "5"],
    pendingConnections: [],
    companyId: null, // No company association
    location: "New York",
    salary: 95000,
    jobType: "Full-time",
    applications: [], // Add this array to store applications
  },
  {
    id: "3",
    name: "Fei-Fei Li",
    title: "Professor of Computer Science at Stanford University",
    avatar: "https://ui-avatars.com/api/?name=Fei-Fei+Li&background=random",
    coverImage: "https://source.unsplash.com/random/800x200?person",
    about:
      "Co-Director of Stanford's Human-Centered AI Institute. Former Chief Scientist of AI/ML at Google Cloud. Known for establishing ImageNet.",
    connections: ["1", "4"],
    pendingConnections: ["5"],
    companyId: null, // No company association
    location: "Stanford",
    salary: 120000,
    jobType: "Full-time",
    applications: [], // Add this array to store applications
  },
  {
    id: "4",
    name: "Ben Taylor",
    title: "Data Scientist at Google",
    avatar: "https://ui-avatars.com/api/?name=Ben+Taylor&background=random",
    coverImage: "https://source.unsplash.com/random/800x200?person",
    about:
      "13 years of experience in Machine Learning. Specializes in genetic programming and automated network design.",
    connections: ["3"],
    pendingConnections: ["1"],
    companyId: "3", // Associate with Google
    location: "San Francisco",
    salary: 130000,
    jobType: "Full-time",
    applications: [], // Add this array to store applications
  },
  {
    id: "5",
    name: "Eric Weber",
    title: "Head of Experimentation at Yelp",
    avatar: "https://ui-avatars.com/api/?name=Eric+Weber&background=random",
    coverImage: "https://source.unsplash.com/random/800x200?person",
    about:
      "Expert in data science, experimentation, and analytics. Passionate about leveraging data to drive business decisions.",
    connections: ["2"],
    pendingConnections: ["3"],
    companyId: null, // No company association
    location: "Chicago",
    salary: 110000,
    jobType: "Full-time",
    applications: [], // Add this array to store applications
  },
  {
    id: "6",
    name: "Nick Campbell",
    title: "Hiring Manager at Google",
    avatar:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2F5iXNXMq9V8E%2Fmaxresdefault.jpg&f=1&nofb=1&ipt=5f098b298284e6bb6c5ca37f395fc0b03b6c7d54c44ddf745462f0ff9aaf7160&ipo=images",
    coverImage: "https://source.unsplash.com/random/800x200?person",
    about:
      "Expert in data science, experimentation, and analytics. Passionate about leveraging data to drive business decisions.",
    connections: ["1", "2"],
    pendingConnections: ["4"],
    companyId: "3", // Associate with Google
    location: "Mountain View",
    salary: 140000,
    jobType: "Full-time",
    applications: [], // Add this array to store applications
  },
];

export default users;
