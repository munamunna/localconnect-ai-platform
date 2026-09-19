import {
    fireEvent,
    render,
    screen,
    waitFor,
  } from "@testing-library/react";
  import { beforeEach, describe, expect, it, vi } from "vitest";
  import { MemoryRouter } from "react-router-dom";
  
  import FreelancerDiscovery from "./FreelancerDiscovery";
  import * as api from "../../services/api";
  
  vi.mock("../../services/api", () => ({
    matchFreelancers: vi.fn(),
  }));
  
  function renderPage() {
    return render(
      <MemoryRouter>
        <FreelancerDiscovery />
      </MemoryRouter>
    );
  }
  
  describe("FreelancerDiscovery", () => {
    beforeEach(() => {
      vi.clearAllMocks();
    });
  
    it("renders the freelancer discovery page", () => {
      renderPage();
  
      expect(
        screen.getByRole("heading", {
          name: "Find trusted local professionals",
        })
      ).toBeInTheDocument();
  
      expect(
        screen.getByLabelText("What service do you need?")
      ).toBeInTheDocument();
  
      expect(
        screen.getByLabelText("Where do you need it?")
      ).toBeInTheDocument();
  
      expect(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      ).toBeInTheDocument();
    });
  
    it("validates required service", async () => {
      renderPage();
  
      fireEvent.change(
        screen.getByLabelText("Where do you need it?"),
        {
          target: {
            value: "Kozhikode",
          },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      );
  
      expect(
        await screen.findByRole("alert")
      ).toHaveTextContent(
        "Please enter the service you need."
      );
  
      expect(
        api.matchFreelancers
      ).not.toHaveBeenCalled();
    });
  
    it("validates required location", async () => {
      renderPage();
  
      fireEvent.change(
        screen.getByLabelText("What service do you need?"),
        {
          target: {
            value: "Electrician",
          },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      );
  
      expect(
        await screen.findByRole("alert")
      ).toHaveTextContent(
        "Please enter your location."
      );
  
      expect(
        api.matchFreelancers
      ).not.toHaveBeenCalled();
    });
  
    it("searches for freelancers and displays matching results", async () => {
      api.matchFreelancers.mockResolvedValue({
        matches: [
          {
            id: 101,
            name: "Nooh",
            service: "Electrician",
            location: "Kozhikode",
            phone: "9999999999",
            verified: true,
            available: true,
            created_at: "2026-09-18T10:00:00",
          },
        ],
      });
  
      renderPage();
  
      fireEvent.change(
        screen.getByLabelText("What service do you need?"),
        {
          target: {
            value: "Electrician",
          },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Where do you need it?"),
        {
          target: {
            value: "Kozhikode",
          },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      );
  
      await waitFor(() => {
        expect(
          api.matchFreelancers
        ).toHaveBeenCalledWith({
          service: "Electrician",
          location: "Kozhikode",
        });
      });
  
      expect(
        await screen.findByRole("heading", {
          name: "Available professionals",
        })
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("Nooh")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("Electrician")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("📍 Kozhikode")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("✓ Verified")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("Available now")
      ).toBeInTheDocument();
  
      expect(
        screen.getByRole("link", {
          name: "Contact Freelancer",
        })
      ).toHaveAttribute(
        "href",
        "tel:9999999999"
      );
    });
  
    it("displays the empty state when no freelancers are found", async () => {
      api.matchFreelancers.mockResolvedValue({
        matches: [],
      });
  
      renderPage();
  
      fireEvent.change(
        screen.getByLabelText("What service do you need?"),
        {
          target: {
            value: "Plumber",
          },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Where do you need it?"),
        {
          target: {
            value: "Kozhikode",
          },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      );
  
      expect(
        await screen.findByRole("heading", {
          name: "No freelancers found",
        })
      ).toBeInTheDocument();
  
      expect(
        screen.getByText(
          "We couldn't find a verified and available freelancer for this service and location."
        )
      ).toBeInTheDocument();
  
      expect(
        screen.getByText(
          "Try another service or nearby location."
        )
      ).toBeInTheDocument();
    });
  
    it("displays an API error", async () => {
      api.matchFreelancers.mockRejectedValue(
        new Error("Freelancer matching failed")
      );
  
      renderPage();
  
      fireEvent.change(
        screen.getByLabelText("What service do you need?"),
        {
          target: {
            value: "Electrician",
          },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Where do you need it?"),
        {
          target: {
            value: "Kozhikode",
          },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      );
  
      expect(
        await screen.findByRole("alert")
      ).toHaveTextContent(
        "Freelancer matching failed"
      );
    });
  
    it("shows the loading state while searching", async () => {
      let resolveRequest;
  
      api.matchFreelancers.mockImplementation(
        () =>
          new Promise((resolve) => {
            resolveRequest = resolve;
          })
      );
  
      renderPage();
  
      fireEvent.change(
        screen.getByLabelText("What service do you need?"),
        {
          target: {
            value: "Electrician",
          },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Where do you need it?"),
        {
          target: {
            value: "Kozhikode",
          },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Find Freelancers",
        })
      );
  
      expect(
        screen.getByRole("status")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("Finding professionals...")
      ).toBeInTheDocument();
  
      expect(
        screen.getByRole("button", {
          name: "Searching...",
        })
      ).toBeDisabled();
  
      resolveRequest({
        matches: [],
      });
  
      await waitFor(() => {
        expect(
          screen.getByRole("heading", {
            name: "No freelancers found",
          })
        ).toBeInTheDocument();
      });
    });
  });