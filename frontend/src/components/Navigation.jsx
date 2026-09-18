import { NavLink } from "react-router-dom";

function Navigation() {
  return (
    <nav>
      <NavLink to="/">
        Home
      </NavLink>

      {" | "}

      <NavLink to="/request">
        Find a Freelancer
      </NavLink>

      {" | "}

      <NavLink to="/register">
        Register as a Freelancer
      </NavLink>
    </nav>
  );
}

export default Navigation;