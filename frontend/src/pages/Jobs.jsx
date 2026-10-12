import Navbar from "../components/Navbar"
import { useState, useEffect } from "react"

function Jobs() {
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
          throw new Error("Unable to load jobs.")
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
    <>
    <Navbar />

    <main className="dashboard-content">
      <h1>Explore Jobs</h1>
      <p>Browse the jobs available in your account.</p>

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
              <p>{job.description || "No description available."}</p>
              <p>{job.location || "Location not specified"}</p>
            </article>
          ))}
        </div>
      )}
    </main>
    </>

  )
}

export default Jobs
