
import { Link, useNavigate } from "react-router-dom"

function Navbar() {
  const navigate = useNavigate()

  function handleLogout() {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <nav className="navbar">
      <h2>Job Intelligence</h2>

      <div className="nav-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/jobs">Jobs</Link>
        <Link to="/recommended-jobs">Recommended Jobs</Link>

        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  )
}

export default Navbar
