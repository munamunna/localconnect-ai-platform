import { useState } from "react";
import { registerFreelancer } from "../services/api";

function FreelancerRegistration() {
  const [form, setForm] = useState({
    name: "",
    service: "",
    location: "",
    phone: "",
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (
      !form.name.trim() ||
      !form.service.trim() ||
      !form.location.trim()
    ) {
      setError(
        "Name, service, and location are required."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await registerFreelancer({
        name: form.name.trim(),
        service: form.service.trim(),
        location: form.location.trim(),
        phone: form.phone.trim(),
      });

      setResult(data);

      setForm({
        name: "",
        service: "",
        location: "",
        phone: "",
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2>Freelancer Registration</h2>

      <p>
        Register your service so customers can find you.
      </p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name</label>

          <br />

          <input
            id="name"
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Your name"
          />
        </div>

        <br />

        <div>
          <label htmlFor="service">Service</label>

          <br />

          <input
            id="service"
            name="service"
            value={form.service}
            onChange={handleChange}
            placeholder="Example: Electrician"
          />
        </div>

        <br />

        <div>
          <label htmlFor="location">Location</label>

          <br />

          <input
            id="location"
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="Example: Kozhikode"
          />
        </div>

        <br />

        <div>
          <label htmlFor="phone">Phone</label>

          <br />

          <input
            id="phone"
            name="phone"
            value={form.phone}
            onChange={handleChange}
            placeholder="Optional"
          />
        </div>

        <br />

        <button type="submit" disabled={loading}>
          {loading
            ? "Registering..."
            : "Register"}
        </button>
      </form>

      {error && (
        <p>{error}</p>
      )}

      {result && (
        <div>
          <h3>Registration Successful</h3>

          <p>
            <strong>Name:</strong>{" "}
            {result.name}
          </p>

          <p>
            <strong>Service:</strong>{" "}
            {result.service}
          </p>

          <p>
            <strong>Location:</strong>{" "}
            {result.location}
          </p>

          <p>
            <strong>Verified:</strong>{" "}
            {result.verified ? "Yes" : "Pending"}
          </p>

          <p>
            <strong>Available:</strong>{" "}
            {result.available ? "Yes" : "No"}
          </p>

          <p>
            Your profile has been submitted successfully.
          </p>
        </div>
      )}
    </div>
  );
}

export default FreelancerRegistration;