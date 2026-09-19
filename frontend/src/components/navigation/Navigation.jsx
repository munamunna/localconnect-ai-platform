import { NavLink } from "react-router-dom";
import "./Navigation.css";

function Navigation() {
  return (
    <nav className="navigation" aria-label="Main navigation">
      <NavLink to="/">
        Home
      </NavLink>

      <NavLink to="/request">
        Customer Request
      </NavLink>

      <NavLink to="/freelancers">
        Find Freelancers
      </NavLink>

      <NavLink to="/register">
        Register
      </NavLink>
    </nav>
  );
}

export default Navigation;