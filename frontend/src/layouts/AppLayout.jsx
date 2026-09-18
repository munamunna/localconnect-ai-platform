import { Outlet } from "react-router-dom";
import Navigation from "../components/Navigation";

function AppLayout() {
  return (
    <div>
      <header>
        <h1>LocalConnect</h1>

        <Navigation />
      </header>

      <hr />

      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default AppLayout;