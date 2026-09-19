import { describe, expect, it, vi } from "vitest";
import { matchFreelancers } from "./api";

describe("matchFreelancers", () => {
  it("returns matching freelancers successfully", async () => {
    const mockResponse = {
      matches: [
        {
          id: 1,
          name: "Ahmed Electrician",
          service: "Electrician",
          location: "Kozhikode",
          phone: "9999999999",
          verified: true,
          available: true,
          created_at: "2026-09-18T10:00:00",
        },
      ],
    };

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      })
    );

    const result = await matchFreelancers({
      service: "Electrician",
      location: "Kozhikode",
    });

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/freelancers/match",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          service: "Electrician",
          location: "Kozhikode",
        }),
      }
    );

    expect(result).toEqual(mockResponse);
  });

  it("throws an API error when matching fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({
          detail: "Service is required",
        }),
      })
    );

    await expect(
      matchFreelancers({
        service: "",
        location: "Kozhikode",
      })
    ).rejects.toThrow("Service is required");
  });
});