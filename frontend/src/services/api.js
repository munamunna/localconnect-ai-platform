const API_BASE_URL = "http://localhost:8000";

export async function extractLead(message) {
  const response = await fetch(
    `${API_BASE_URL}/api/leads/extract`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to extract lead"
    );
  }

  return data;
}