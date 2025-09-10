import React from 'react'

export default function RiskGauge({ score = 0 }) {
  const clamped = Math.max(0, Math.min(100, score))
  const color = clamped < 33 ? '#22c55e' : clamped < 66 ? '#f59e0b' : '#ef4444'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width="220" height="120" viewBox="0 0 220 120">
        <path d="M20 100 A 90 90 0 0 1 200 100" stroke="#e5e7eb" strokeWidth="20" fill="none" />
        <path d={`M20 100 A 90 90 0 ${clamped > 50 ? 1 : 0} 1 ${20 + 1.8 * clamped} 100`} stroke={color} strokeWidth="20" fill="none" />
        <circle cx={20 + 1.8 * clamped} cy="100" r="8" fill={color} />
      </svg>
      <div style={{ fontSize: 24, fontWeight: 700, color }}>{clamped.toFixed(1)}%</div>
    </div>
  )
}