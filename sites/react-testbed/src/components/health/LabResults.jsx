// LabResults.jsx
import React from "react";
import { Button } from "antd";

const labResultsData = [
  { id: 1, label: "Pregnancy Test", time: "October 1, 2023 09:00", file: "/downloads/lab_results.pdf" },
  { id: 2, label: "Blood Test", time: "September 15, 2023 15:30", file: "/downloads/blood_test.pdf" },
  { id: 3, label: "X-Ray", time: "August 20, 2023 11:15", file: "/downloads/xray.pdf" },
];

const LabResults = () => {
  return (
    <section
      id="lab-results"
      style={{ padding: "20px", borderTop: "1px solid #ccc", marginTop: "20px" }}
      aria-label="Lab Results Section"
    >
      <h3>Lab Results</h3>
      {labResultsData.map(result => (
        <div key={result.id} style={{ marginBottom: "15px" }}>
          <p>
            {result.label} - <span style={{ fontWeight: "bold" }}>{result.time}</span>
          </p>
          <a href={result.file} download>
            <Button id={`button-${result.label}`} type="primary">Download {result.label}</Button>
          </a>
        </div>
      ))}
    </section>
  );
};

export default LabResults;
