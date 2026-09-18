import { useState } from "react";
import { extractLead } from "../services/api";

function CustomerRequest() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!message.trim()) {
      setError("Please describe the service you need.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await extractLead(message);

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2>Find a Local Freelancer</h2>

      <p>
        Tell us what service you need.
      </p>

      <form onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          placeholder="Example: I need an electrician in Kozhikode tomorrow"
          rows={6}
        />

        <br />

        <button type="submit" disabled={loading}>
          {loading
            ? "Finding..."
            : "Find a Freelancer"}
        </button>
      </form>

      {error && (
        <p>
          {error}
        </p>
      )}

      {result && (
        <div>
          <h3>AI Extracted Lead</h3>

          <p>
            <strong>Service:</strong>{" "}
            {result.lead.service || "Not provided"}
          </p>

          <p>
            <strong>Location:</strong>{" "}
            {result.lead.location || "Not provided"}
          </p>

          <p>
            <strong>Urgency:</strong>{" "}
            {result.lead.urgency || "Not provided"}
          </p>

          <p>
            <strong>Problem:</strong>{" "}
            {result.lead.problem || "Not provided"}
          </p>

          <p>
            <strong>Priority:</strong>{" "}
            {result.lead.lead_priority || "Not provided"}
          </p>

          <p>
            <strong>Lead ID:</strong>{" "}
            {result.lead_id}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            {result.status}
          </p>
        </div>
      )}
    </div>
  );
}

export default CustomerRequest;