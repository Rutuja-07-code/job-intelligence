import Navbar from "../components/Navbar"
import { useState, useEffect } from "react"

function Dashboard() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchJobs() {
      try {
        const token = localStorage.getItem("token")

        const response = await fetch(
          "http://127.0.0.1:8000/jobs",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        if (!response.ok) {
          throw new Error("Unable to load jobs. Please try again.")
        }

        const data = await response.json()
        setJobs(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchJobs()
  }, [])


  return (
    
    <div className="dashboard">
  <Navbar />
      <main className="dashboard-content">
        <section className="welcome">
          <h1>Welcome to Job Intelligence</h1>
          <p>Manage and explore your job opportunities.</p>
        </section>

        <section className="jobs-section">
          <h2>Your Jobs</h2>

          {loading ? (
            <p>Loading jobs...</p>
          ) : error ? (
            <p className="error-message">{error}</p>
          ) : jobs.length === 0 ? (
            <p>No jobs available yet.</p>
          ) : (

            <div className="jobs-list">
              {jobs.map((job) => (
                <article className="job-card" key={job.id}>
                  <h3>{job.title}</h3>
                  <p>{job.description}</p>
                  <p>{job.location}</p>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default Dashboard
