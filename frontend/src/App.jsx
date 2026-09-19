import {
  Routes,
  Route,
} from "react-router-dom";

import AppLayout from "./layouts/AppLayout";
import Home from "./pages/Home";
import CustomerRequest from "./pages/CustomerRequest";
import FreelancerRegistration from "./pages/FreelancerRegistration";
import NotFound from "./pages/NotFound";
import FreelancerDiscovery from "./pages/freelancer-discovery/FreelancerDiscovery";

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/request"
          element={<CustomerRequest />}
        />

        <Route
          path="/register"
          element={<FreelancerRegistration />}
        />

        <Route
          path="*"
          element={<NotFound />}
        />
      </Route>

      <Route
      path="/freelancers"
      element={<FreelancerDiscovery />}
      />
    </Routes>
  );
}

export default App;