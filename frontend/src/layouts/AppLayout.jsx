import { Link, Outlet } from "react-router-dom";
import Navigation from "../components/navigation/Navigation";
import "./AppLayout.css";

function AppLayout() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <Link className="brand" to="/">
          Local<span>Connect</span>
        </Link>

        <Navigation />
      </header>

      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default AppLayout;