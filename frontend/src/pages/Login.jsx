import { useState } from "react"
import { useNavigate } from "react-router-dom"

function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

  async function handleSubmit(event) {
    event.preventDefault()

    const formData = new URLSearchParams()

    formData.append("username", email)
    formData.append("password", password)

    const loginResponse = await fetch(
      "http://127.0.0.1:8000/users/login",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData
      }
    )

    const loginData = await loginResponse.json()

    localStorage.setItem("token", loginData.access_token)

    console.log("Login successful")
    navigate("/dashboard")
  }

  return (
    <div>
      <h1>Job Intelligence</h1>

      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <label>Email</label>

        <input
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <br />

        <label>Password</label>

        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <br />

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  )
}

export default Login