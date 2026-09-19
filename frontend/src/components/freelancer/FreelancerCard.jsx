import "./FreelancerCard.css";

function getInitials(name) {
  return name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function FreelancerCard({ freelancer }) {
  const {
    name,
    service,
    location,
    phone,
    verified,
    available,
  } = freelancer;

  return (
    <article className="freelancer-card">
      <div className="freelancer-card-top">
        <div
          className="freelancer-avatar"
          aria-hidden="true"
        >
          {getInitials(name)}
        </div>

        <div className="freelancer-name">
          <h3>{name}</h3>

          {verified && (
            <span className="verified-badge">
              ✓ Verified
            </span>
          )}
        </div>
      </div>

      <div className="freelancer-details">
        <div className="detail-row">
          <span>Service</span>
          <strong>{service}</strong>
        </div>

        <div className="detail-row">
          <span>Location</span>
          <strong>📍 {location}</strong>
        </div>

        <div className="availability">
          <span
            className="availability-dot"
            aria-hidden="true"
          />

          {available
            ? "Available now"
            : "Currently unavailable"}
        </div>
      </div>

      {phone && (
        <a
          className="contact-button"
          href={`tel:${phone}`}
        >
          Contact Freelancer
        </a>
      )}
    </article>
  );
}

export default FreelancerCard;