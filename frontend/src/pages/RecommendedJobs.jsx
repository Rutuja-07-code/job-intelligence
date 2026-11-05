
import Navbar from "../components/Navbar"
import { useState, useEffect } from "react"

function RecommendedJobs() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchRecommendations() {
      try {
        const token = localStorage.getItem("token")

        const response = await fetch(
          "http://127.0.0.1:8000/jobs/recommendations",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(
            errorData.detail || "Unable to load recommendations."
          )
        }

        const data = await response.json()
        setJobs(data)

      } catch (err) {
        setError(err.message)

      } finally {
        setLoading(false)
      }
    }

    fetchRecommendations()
  }, [])

  return (
    <>
      <Navbar />

      <main className="dashboard-content">
        <h1>Recommended Jobs</h1>

        <p>
          Jobs ranked according to how well your skills match
          employer requirements.
        </p>

        {loading ? (
          <p>Finding suitable jobs...</p>

        ) : error ? (
          <p className="error-message">{error}</p>

        ) : jobs.length === 0 ? (
          <p>No recommendations available yet.</p>

        ) : (
          <div className="jobs-list">
            {jobs.map((job) => (
              <article className="job-card" key={job.job_id}>

                <h3>{job.job_title}</h3>

                <p>{job.company_name}</p>

                <p>
                  {job.location || "Location not specified"}
                </p>

                <h3>
                  Match Score: {job.match_score}%
                </h3>

                <div>
                  <strong>Matched Skills:</strong>

                  <p>
                    {job.matched_skills.length > 0
                      ? job.matched_skills.join(", ")
                      : "No matching skills"}
                  </p>
                </div>

                <div>
                  <strong>Missing Skills:</strong>

                  <p>
                    {job.missing_skills.length > 0
                      ? job.missing_skills.join(", ")
                      : "No missing skills"}
                  </p>
                </div>

              </article>
            ))}
          </div>
        )}
      </main>
    </>
  )
}

export default RecommendedJobs
