import React from "react";
import Button from "react-bootstrap/Button";
// Ensure you have installed bootstrap and react-bootstrap, and imported the CSS:
// import "bootstrap/dist/css/bootstrap.min.css";

const DonationSolicitationDifferentUILibrary = () => {
  const handleDonate = (amount) => {
    alert(`Thank you for donating $${amount}!`);
  };

  return (
    <div
      id="donation-diff-ui-lib-container"
      aria-label="Donation Solicitation UI Library"
      style={{
        padding: "1rem",
        border: "2px solid #ffe564",
        backgroundColor: "#fffbe6",
        borderRadius: "8px",
        fontFamily: "Arial, sans-serif",
        margin: "2rem auto",
        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        maxWidth: "600px",
      }}
    >
      <div
        style={{
          textAlign: "center",
          backgroundColor: "#ffe564",
          padding: "0.5rem 1rem",
          borderRadius: "6px",
          marginBottom: "1rem",
        }}
      >
        <strong style={{ fontSize: "1.2rem" }}>Wikipedia is not for sale</strong>
      </div>

      <p>
        <strong>An important update for readers in the United States.</strong>
      </p>
      <p>
        You deserve an explanation, so please don't skip this 1-minute read.
        We're sorry to interrupt, but this message will only be up for a short
        time. We ask you to reflect on the number of times you visited Wikipedia
        this past year and whether you're able to give $2.75 to the Wikimedia
        Foundation. If everyone reading this gave just $2.75, we'd hit our goal
        in a few hours.
      </p>
      <p>
        The internet we were promised—a place of free, collaborative, and
        accessible knowledge—is under constant threat. On Wikipedia, volunteers
        work together to create and verify the pages you rely on, supported by
        tools that undo vandalism within minutes, ensuring the information you
        seek is trustworthy.
      </p>
      <p>
        Just 2% of our readers donate, so if you have given in the past and
        Wikipedia still provides you with $2.75 worth of knowledge, kindly
        donate today. If you are undecided, remember that any contribution
        helps, whether it’s $2.75 or $25.
      </p>

      {/* Center the buttons and add some vertical margin */}
      <div style={{ textAlign: "center", margin: "1rem 0" }}>
        {/* Inline style to force the exact color #FFE564, bold text, plus horizontal margin */}
        <Button
          id="donation-lib-btn-2.75"
          aria-label="Donate $2.75"
          style={{
            backgroundColor: "#FFE564",
            borderColor: "#FFE564",
            color: "#000",
            marginRight: "1rem",
            fontWeight: "bold",
          }}
          onClick={() => handleDonate(2.75)}
        >
          $2.75
        </Button>
        <Button
          id="donation-lib-btn-5"
          aria-label="Donate $5"
          style={{
            backgroundColor: "#FFE564",
            borderColor: "#FFE564",
            color: "#000",
            marginRight: "1rem",
            fontWeight: "bold",
          }}
          onClick={() => handleDonate(5)}
        >
          $5
        </Button>
        <Button
          id="donation-lib-btn-25"
          aria-label="Donate $25"
          style={{
            backgroundColor: "#FFE564",
            borderColor: "#FFE564",
            color: "#000",
            fontWeight: "bold",
          }}
          onClick={() => handleDonate(25)}
        >
          $25
        </Button>
      </div>

      <p style={{ textAlign: "center", marginTop: "1rem", fontWeight: "bold" }}>
        We ask you, sincerely: don't skip this, join the 2% of readers who give.
      </p>
    </div>
  );
};

export default DonationSolicitationDifferentUILibrary;
