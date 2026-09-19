import { useState } from "react";

import EmptyState from "../../components/common/EmptyState";
import LoadingState from "../../components/common/LoadingState";
import FreelancerCard from "../../components/freelancer/FreelancerCard";
import { matchFreelancers } from "../../services/api";

import "./FreelancerDiscovery.css";

function FreelancerDiscovery() {
  const [service, setService] = useState("");
  const [location, setLocation] = useState("");
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!service.trim()) {
      setError("Please enter the service you need.");
      return;
    }

    if (!location.trim()) {
      setError("Please enter your location.");
      return;
    }

    setLoading(true);
    setError("");
    setMatches([]);
    setSearched(false);

    try {
      const data = await matchFreelancers({
        service,
        location,
      });

      setMatches(data.matches || []);
      setSearched(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="discovery-page">
      <section className="discovery-hero">
        <div className="discovery-container">
          <span className="discovery-eyebrow">
            LOCALCONNECT
          </span>

          <h1>Find trusted local professionals</h1>

          <p className="discovery-hero-description">
            Connect directly with verified and available
            freelancers near you.
          </p>

          <form
            className="discovery-search-panel"
            onSubmit={handleSubmit}
          >
            <div className="discovery-search-field">
              <span className="discovery-search-icon">
                🔧
              </span>

              <div>
                <label htmlFor="service">
                  What service do you need?
                </label>

                <input
                  id="service"
                  type="text"
                  value={service}
                  onChange={(event) =>
                    setService(event.target.value)
                  }
                  placeholder="Electrician, plumber, painter..."
                />
              </div>
            </div>

            <div className="discovery-search-divider" />

            <div className="discovery-search-field">
              <span className="discovery-search-icon">
                📍
              </span>

              <div>
                <label htmlFor="location">
                  Where do you need it?
                </label>

                <input
                  id="location"
                  type="text"
                  value={location}
                  onChange={(event) =>
                    setLocation(event.target.value)
                  }
                  placeholder="Kozhikode"
                />
              </div>
            </div>

            <button
              className="discovery-search-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Searching..."
                : "Find Freelancers"}
            </button>
          </form>

          {error && (
            <p className="discovery-form-error" role="alert">
              {error}
            </p>
          )}
        </div>
      </section>

      <section className="discovery-results">
        <div className="discovery-container">
          {loading && (
            <LoadingState
              title="Finding professionals..."
              message="We're looking for verified and available freelancers near you."
            />
          )}

          {!loading && !searched && (
            <div className="discovery-placeholder">
              <span className="discovery-eyebrow">
                LOCALCONNECT NETWORK
              </span>

              <h2>Available freelancers</h2>

              <p>
                Search by service and location to discover
                verified professionals who are currently
                available.
              </p>
            </div>
          )}

          {searched &&
            !loading &&
            matches.length === 0 &&
            !error && (
              <EmptyState
                title="No freelancers found"
                message="We couldn't find a verified and available freelancer for this service and location."
                hint="Try another service or nearby location."
              />
            )}

          {matches.length > 0 && (
            <div>
              <header className="discovery-results-header">
                <div>
                  <span className="discovery-eyebrow">
                    LOCAL RESULTS
                  </span>

                  <h2>Available professionals</h2>

                  <p>
                    {matches.length} professional
                    {matches.length !== 1 ? "s" : ""} found
                    {" "}for {service} in {location}
                  </p>
                </div>
              </header>

              <div className="freelancer-grid">
                {matches.map((freelancer) => (
                  <FreelancerCard
                    key={freelancer.id}
                    freelancer={freelancer}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default FreelancerDiscovery;