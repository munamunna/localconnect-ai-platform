import {
    render,
    screen,
    fireEvent,
    waitFor,
  } from "@testing-library/react";
  import {
    describe,
    it,
    expect,
    vi,
  } from "vitest";
  
  import FreelancerRegistration from "./FreelancerRegistration";
  import { registerFreelancer } from "../services/api";
  
  vi.mock("../services/api", () => ({
    registerFreelancer: vi.fn(),
  }));
  
  describe("FreelancerRegistration", () => {
    it("renders the registration form", () => {
      render(<FreelancerRegistration />);
  
      expect(
        screen.getByRole("heading", {
          name: "Freelancer Registration",
        })
      ).toBeInTheDocument();
  
      expect(
        screen.getByLabelText("Name")
      ).toBeInTheDocument();
  
      expect(
        screen.getByLabelText("Service")
      ).toBeInTheDocument();
  
      expect(
        screen.getByLabelText("Location")
      ).toBeInTheDocument();
  
      expect(
        screen.getByLabelText("Phone")
      ).toBeInTheDocument();
  
      expect(
        screen.getByRole("button", {
          name: "Register",
        })
      ).toBeInTheDocument();
    });
  
    it("registers a freelancer successfully", async () => {
      registerFreelancer.mockResolvedValue({
        id: 10,
        name: "Muna",
        service: "web and app",
        location: "Payyoli",
        phone: "9876543210",
        verified: false,
        available: true,
        created_at: null,
      });
  
      render(<FreelancerRegistration />);
  
      fireEvent.change(
        screen.getByLabelText("Name"),
        {
          target: { value: "Muna" },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Service"),
        {
          target: { value: "web and app" },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Location"),
        {
          target: { value: "Payyoli" },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Phone"),
        {
          target: { value: "9876543210" },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Register",
        })
      );
  
      await waitFor(() => {
        expect(registerFreelancer).toHaveBeenCalledWith({
          name: "Muna",
          service: "web and app",
          location: "Payyoli",
          phone: "9876543210",
        });
      });
  
      expect(
        screen.getByText("Registration Successful")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("Pending")
      ).toBeInTheDocument();
  
      expect(
        screen.getByText("Yes")
      ).toBeInTheDocument();
    });
  
    it("shows validation error when required fields are empty", () => {
      render(<FreelancerRegistration />);
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Register",
        })
      );
  
      expect(
        screen.getByText(
          "Name, service, and location are required."
        )
      ).toBeInTheDocument();
  
      expect(
        registerFreelancer
      ).not.toHaveBeenCalled();
    });
  
    it("shows API error when registration fails", async () => {
      registerFreelancer.mockRejectedValue(
        new Error("Failed to register freelancer")
      );
  
      render(<FreelancerRegistration />);
  
      fireEvent.change(
        screen.getByLabelText("Name"),
        {
          target: { value: "Muna" },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Service"),
        {
          target: { value: "web and app" },
        }
      );
  
      fireEvent.change(
        screen.getByLabelText("Location"),
        {
          target: { value: "Payyoli" },
        }
      );
  
      fireEvent.click(
        screen.getByRole("button", {
          name: "Register",
        })
      );
  
      await waitFor(() => {
        expect(
          screen.getByText(
            "Failed to register freelancer"
          )
        ).toBeInTheDocument();
      });
    });
  });