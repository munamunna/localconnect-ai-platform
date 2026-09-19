import "./EmptyState.css";

function EmptyState({
  icon = "🔎",
  title,
  message,
  hint,
}) {
  return (
    <div className="empty-state">
      <div
        className="empty-state-icon"
        aria-hidden="true"
      >
        {icon}
      </div>

      <h2>{title}</h2>

      <p>{message}</p>

      {hint && <span>{hint}</span>}
    </div>
  );
}

export default EmptyState;