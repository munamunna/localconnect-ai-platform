import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>LocalConnect</h1>

      <p>
        Find trusted local freelancers for your service needs.
      </p>

      <div>
        <Link to="/request">
          Find a Freelancer
        </Link>
      </div>

      <br />

      <div>
        <Link to="/register">
          Register as a Freelancer
        </Link>
      </div>
    </div>
  );
}

export default Home;