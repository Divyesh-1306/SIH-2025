import React from 'react'
import Dashboard from './pages/Dashboard.jsx'

export default function App() {
  return (
    <div style={{ fontFamily: 'Inter, system-ui, Arial, sans-serif', padding: 16 }}>
      <h1 style={{ marginBottom: 8 }}>Open-Pit Rockfall Risk Dashboard</h1>
      <Dashboard />
    </div>
  )
}