import "./LoadingState.css";

function LoadingState({
  title = "Loading...",
  message,
}) {
  return (
    <div className="loading-state" role="status">
      <div className="loading-spinner" />

      <h2>{title}</h2>

      {message && <p>{message}</p>}
    </div>
  );
}

export default LoadingState;