// src/components/health/data/users.js

const users = [
  {
    id: "1",
    name: "John Doe",
    role: "Patient",
    avatar: "https://ui-avatars.com/api/?name=John+Doe&background=random",
    medicalRecords: [
      {
        id: "rec1",
        title: "General Checkup",
        date: "2023-09-15",
        doctor: "Dr. Emily Smith",
        notes: "All vitals are normal.",
      },
      {
        id: "rec2",
        title: "Blood Test",
        date: "2023-08-10",
        doctor: "Dr. Michael Brown",
        notes: "Cholesterol levels are slightly elevated.",
      },
      {
        id: "rec3",
        title: "Dental Cleaning",
        date: "2023-07-05",
        doctor: "Dr. Lisa Wong",
        notes: "No cavities found.",
      },
      {
        id: "rec4",
        title: "Flu Shot",
        date: "2023-10-22",
        doctor: "Dr. Arjun",
        notes: "Flu shot administered successfully with no side effects observed.",
      },
      // Add more records as needed
    ],
    appointments: [
      {
        id: "app1",
        date: "2023-10-20",
        time: "10:00 AM",
        doctor: "Dr. Sarah Johnson",
        department: "Cardiology",
      },
      {
        id: "app2",
        date: "2023-11-05",
        time: "2:00 PM",
        doctor: "Dr. Robert Davis",
        department: "Dermatology",
      },
      // Add more appointments as needed
    ],
    messages: [
      {
        sender: "Dr. Emily Smith",
        text: "Your lab results are ready. Please check your medical records.",
        timestamp: "2023-08-12T14:30:00Z",
      },
      {
        sender: "Dr. Sarah Johnson",
        text: "Reminder: Your appointment is scheduled for tomorrow at 10 AM.",
        timestamp: "2023-10-19T09:00:00Z",
      },
      // Add more messages as needed
    ],
    // Add other user details as needed
  },
  // Add more users as needed
];

export default users;
