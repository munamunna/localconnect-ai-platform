import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";

import CustomerRequest from "./CustomerRequest";
import { extractLead } from "../services/api";

vi.mock("../services/api", () => ({
  extractLead: vi.fn(),
}));

describe("CustomerRequest", () => {
  it("renders the customer request form", () => {
    render(<CustomerRequest />);

    expect(
      screen.getByRole("heading", {
        name: "Find a Local Freelancer",
      })
    ).toBeInTheDocument();

    expect(
      screen.getByPlaceholderText(
        "Example: I need an electrician in Kozhikode tomorrow"
      )
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", {
        name: "Find a Freelancer",
      })
    ).toBeInTheDocument();
  });

  it("submits the customer request and displays the lead", async () => {
    extractLead.mockResolvedValue({
      lead: {
        service: "electrician",
        location: "Kozhikode",
        urgency: "tomorrow",
        problem: "wiring problem",
        lead_priority: "high",
      },
      lead_id: 3,
      status: "NEW",
    });

    render(<CustomerRequest />);

    const textarea = screen.getByPlaceholderText(
      "Example: I need an electrician in Kozhikode tomorrow"
    );

    fireEvent.change(textarea, {
      target: {
        value:
          "I need an electrician in Kozhikode tomorrow",
      },
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Find a Freelancer",
      })
    );

    await waitFor(() => {
      expect(extractLead).toHaveBeenCalledWith(
        "I need an electrician in Kozhikode tomorrow"
      );
    });

    expect(
      screen.getByText("AI Extracted Lead")
    ).toBeInTheDocument();

    expect(
      screen.getByText("electrician")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Kozhikode")
    ).toBeInTheDocument();

    expect(
      screen.getByText("tomorrow")
    ).toBeInTheDocument();

    expect(
      screen.getByText("wiring problem")
    ).toBeInTheDocument();

    expect(
      screen.getByText("high")
    ).toBeInTheDocument();

    expect(
      screen.getByText("3")
    ).toBeInTheDocument();

    expect(
      screen.getByText("NEW")
    ).toBeInTheDocument();
  });

  it("shows validation error when request is empty", () => {
    render(<CustomerRequest />);

    fireEvent.click(
      screen.getByRole("button", {
        name: "Find a Freelancer",
      })
    );

    expect(
      screen.getByText(
        "Please describe the service you need."
      )
    ).toBeInTheDocument();

    expect(extractLead).not.toHaveBeenCalled();
  });

  it("shows API error when lead extraction fails", async () => {
    extractLead.mockRejectedValue(
      new Error("Failed to extract lead")
    );

    render(<CustomerRequest />);

    const textarea = screen.getByPlaceholderText(
      "Example: I need an electrician in Kozhikode tomorrow"
    );

    fireEvent.change(textarea, {
      target: {
        value: "I need an electrician in Kozhikode",
      },
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Find a Freelancer",
      })
    );

    await waitFor(() => {
      expect(
        screen.getByText("Failed to extract lead")
      ).toBeInTheDocument();
    });
  });
});