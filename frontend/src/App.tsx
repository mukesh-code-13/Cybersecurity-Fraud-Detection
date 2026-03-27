import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

import authService from './services/auth'
import { useAuthStore } from './store'

import Header from './components/Header'
import Sidebar from './components/Sidebar'


import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Transactions from './pages/Transactions'
import PhishingDetection from './pages/Phishing'
import BehaviorAnalysis from './pages/Behavior'
import Analytics from './pages/Analytics'

const App: React.FC = () => {
  const { setUser, setAuthenticated, isAuthenticated } = useAuthStore()

  useEffect(() => {
    // Check if user is already authenticated
    const user = authService.getUser()
    if (user) {
      setUser(user)
      setAuthenticated(true)
    }
  }, [setUser, setAuthenticated])

  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        {/* Login Route */}
        <Route path="/login" element={<Login />} />

        {/* Protected Routes */}
        <Route
          path="/*"
          element={
            isAuthenticated ? (
              <div className="flex h-screen bg-light dark:bg-dark">
                <Sidebar />
                <div className="flex-1 flex flex-col overflow-hidden">
                  <Header />
                  <main className="flex-1 overflow-auto">
                    <div className="p-8">
                      <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/transactions" element={<Transactions />} />
                        <Route path="/phishing" element={<PhishingDetection />} />
                        <Route path="/behavior" element={<BehaviorAnalysis />} />
                        <Route path="/analytics" element={<Analytics />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                      </Routes>
                    </div>
                  </main>
                </div>
              </div>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </Router>
  )
}

export default App
