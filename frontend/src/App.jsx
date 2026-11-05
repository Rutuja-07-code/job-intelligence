import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Link, useNavigate } from "react-router-dom"
import RecommendedJobs from "./pages/RecommendedJobs"

import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Jobs from "./pages/Jobs"
import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route 
          path="/dashboard" 
          element={ 
            <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
        />
        <Route
          path="/jobs"
          element={
            <ProtectedRoute>
              <Jobs />
            </ProtectedRoute>
          }
        />
        <Route
          path="/recommended-jobs"
          element={
            <ProtectedRoute>
              <RecommendedJobs />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  )
}

export default App

