import React from 'react'

export default function Heatmap() {
  const gradient = 'linear-gradient(135deg, #22c55e, #f59e0b, #ef4444)'
  return (
    <div style={{
      width: '100%',
      height: 200,
      background: gradient,
      borderRadius: 12,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontWeight: 600
    }}>
      Risk Hotspots (placeholder)
    </div>
  )
}