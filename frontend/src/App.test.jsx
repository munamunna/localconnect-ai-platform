import {
    render,
    screen,
  } from "@testing-library/react";
  
  import {
    describe,
    it,
    expect,
  } from "vitest";
  
  import {
    MemoryRouter,
  } from "react-router-dom";
  
  import App from "./App";
  
  describe("App routing", () => {
    it("renders the home page", () => {
      render(
        <MemoryRouter initialEntries={["/"]}>
          <App />
        </MemoryRouter>
      );
  
      expect(
        screen.getByText(
          "Find trusted local freelancers for your service needs."
        )
      ).toBeInTheDocument();
    });
  
    it("renders the customer request page", () => {
      render(
        <MemoryRouter initialEntries={["/request"]}>
          <App />
        </MemoryRouter>
      );
  
      expect(
        screen.getByRole("heading", {
          name: "Find a Local Freelancer",
        })
      ).toBeInTheDocument();
    });
  
    it("renders the freelancer registration page", () => {
      render(
        <MemoryRouter initialEntries={["/register"]}>
          <App />
        </MemoryRouter>
      );
  
      expect(
        screen.getByRole("heading", {
          name: "Freelancer Registration",
        })
      ).toBeInTheDocument();
    });
  
    it("renders the not found page", () => {
      render(
        <MemoryRouter initialEntries={["/does-not-exist"]}>
          <App />
        </MemoryRouter>
      );
  
      expect(
        screen.getByRole("heading", {
          name: "Page Not Found",
        })
      ).toBeInTheDocument();
    });
  });