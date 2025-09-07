// src/components/health/data/doctors.js

const doctors = [
  {
    id: "d1",
    name: "Dr. Emily Smith",
    specialty: "General Medicine",
    avatar: "https://ui-avatars.com/api/?name=Emily+Smith&background=random",
    schedule: [
      { day: "Monday", time: "9:00 AM - 5:00 PM" },
      { day: "Tuesday", time: "9:00 AM - 5:00 PM" },
      { day: "Wednesday", time: "9:00 AM - 5:00 PM" },
      { day: "Thursday", time: "9:00 AM - 5:00 PM" },
      { day: "Friday", time: "9:00 AM - 3:00 PM" },
    ],
  },
  {
    id: "d2",
    name: "Dr. Sarah Johnson",
    specialty: "Cardiology",
    avatar: "https://ui-avatars.com/api/?name=Sarah+Johnson&background=random",
    schedule: [
      { day: "Monday", time: "10:00 AM - 6:00 PM" },
      { day: "Tuesday", time: "10:00 AM - 6:00 PM" },
      { day: "Wednesday", time: "10:00 AM - 6:00 PM" },
      { day: "Thursday", time: "10:00 AM - 6:00 PM" },
      { day: "Friday", time: "10:00 AM - 4:00 PM" },
    ],
  },
  {
    id: "d3",
    name: "Dr. Arjun",
    specialty: "Neurology",
    avatar: "https://ui-avatars.com/api/?name=Arjun&background=random",
    schedule: [
      { day: "Monday", time: "8:00 AM - 12:00 PM" },
      { day: "Tuesday", time: "8:00 AM - 12:00 PM" },
      { day: "Wednesday", time: "8:00 AM - 12:00 PM" },
      { day: "Thursday", time: "1:00 PM - 6:00 PM" },
      { day: "Friday", time: "1:00 PM - 6:00 PM" },
    ],
  },
  // Add more doctors as needed
];

export default doctors;
