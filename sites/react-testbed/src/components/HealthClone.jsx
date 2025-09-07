// src/components/HealthClone.jsx

import React, { useState } from "react";
import { Layout } from "antd";
import { Routes, Route, useLocation } from "react-router-dom";

import HealthSiteHeader from "./health/Header";
import HealthSiteFooter from "./health/Footer";
import Home from "./health/Home";
import Dashboard from "./health/Dashboard";
import MedicalRecords from "./health/MedicalRecords";
import Appointments from "./health/Appointments";
import Messages from "./health/Messages";
import DoctorProfile from "./health/DoctorProfile";
import TermsOfService from "./health/darkPatterns/TermsOfService";
import LabResults from "./health/LabResults"; 
import PWAConfirmShaming from "./health/darkPatterns/ConfirmShaming";

import "./health/HealthClone.css"; // Custom styles for Health clone
import Scratchpad from "./Scratchpad";

const HealthClone = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const darkPatternsParam = searchParams.get("dp");
  const selectedDarkPatterns = darkPatternsParam
    ? darkPatternsParam.split("_")
    : [];

  const [showTerms, setShowTerms] = useState(
    selectedDarkPatterns.includes("tos")
  );

  const [showConfirmShaming, setShowConfirmShaming] = useState(
    selectedDarkPatterns.includes("cf")
  );

  const handleAgree = () => {
    setShowTerms(false);
  };

  const handleDisagree = () => {
    setShowTerms(false);
  };

  return (
    <>
      <Layout id="health-layout" className={`health-layout ${showTerms ? "overlay-active" : ""}`} aria-label="Health Clone Main Layout">
        {showTerms && (
          <div id="terms-overlay" className="overlay" aria-label="Terms of Service Overlay">
            <TermsOfService onAgree={handleAgree} onDisagree={handleDisagree} />
          </div>
        )}
        {showConfirmShaming && <PWAConfirmShaming />}
        <HealthSiteHeader id="site-header" aria-label="Health Site Header" />
        {/* Dark Pattern Components */}
        {selectedDarkPatterns.includes("pa") && <PregnancyAnalytics id="pregnancy-analytics" aria-label="Pregnancy Analytics Component" />}

        <Layout className="health-inner-layout" style={{ width: "100%" }}>
          <Layout.Content id="health-content" className="health-content" style={{ width: "100%" }} aria-label="Health Content Area">
            <Routes>
              <Route path="/" element={<Home id="home-route" />} />
              <Route path="/dashboard" element={<Dashboard id="dashboard-route" />} />
              <Route path="/medical-records" element={<MedicalRecords id="medical-records-route" />} />
              <Route path="/appointments" element={<Appointments id="appointments-route" />} />
              <Route path="/messages" element={<Messages id="messages-route" />} />
              <Route path="/doctor/:doctorId" element={<DoctorProfile id="doctor-profile-route" />} />
              <Route path="/lab-results" element={<LabResults id="lab-results-route" />} />
            </Routes>
          </Layout.Content>
        </Layout>
        <HealthSiteFooter id="site-footer" aria-label="Health Site Footer" />
      </Layout>
      <Scratchpad />
    </>
  );
};

export default HealthClone;
