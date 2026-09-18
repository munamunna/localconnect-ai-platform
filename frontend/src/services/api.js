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


export async function registerFreelancer({
    name,
    service,
    location,
    phone,
  }) {
    const response = await fetch(
      `${API_BASE_URL}/api/freelancers`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          service,
          location,
          phone: phone || null,
        }),
      }
    );
  
    const data = await response.json();
  
    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to register freelancer"
      );
    }
  
    return data;
  }