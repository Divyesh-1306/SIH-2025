import React, { useEffect, useMemo, useState } from 'react'
import RiskGauge from '../components/Riskgauge.jsx'
import TrendChart from '../components/trendchart.jsx'
import Heatmap from '../components/Heatmap.jsx'
import { getSampleCases, postPredict } from '../services/api.js'

const defaultInput = {
  rainfall_mm: 10,
  temp_C: 24,
  slope_angle: 25,
  vibration: 0.1,
  displacement: 0.2,
  pore_pressure: 0.8,
}

export default function Dashboard() {
  const [form, setForm] = useState(defaultInput)
  const [samples, setSamples] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [alertMsg, setAlertMsg] = useState('')

  useEffect(() => {
    getSampleCases().then(setSamples).catch(() => {})
  }, [])

  const trendData = useMemo(() => {
    const points = 24
    const arr = []
    for (let i = 0; i < points; i++) {
      const factor = i / (points - 1)
      arr.push({
        t: `${i}h`,
        rainfall_mm: Math.max(0, form.rainfall_mm * (0.2 + 0.8 * factor) * (0.8 + 0.4 * Math.sin(i / 3))),
        displacement: Math.max(0, form.displacement * (0.6 + 0.8 * factor) * (0.8 + 0.2 * Math.cos(i / 4))),
      })
    }
    return arr
  }, [form])

  function onChange(e) {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: Number(value) }))
  }

  async function onPredict() {
    setLoading(true)
    setResult(null)
    setAlertMsg('')
    try {
      const data = await postPredict(form)
      setResult(data)
    } catch (e) {
      setAlertMsg('Prediction failed. Ensure backend is running.')
    } finally {
      setLoading(false)
    }
  }

  function selectSample(key) {
    if (!samples) return
    setForm(samples[key])
    setResult(null)
    setAlertMsg('')
  }

  function triggerAlert() {
    if (!result) return
    const level = result.risk_level
    const msg = level === 'Red' ? 'Evacuate area immediately, SMS/Email triggered.' : level === 'Yellow' ? 'Monitor slope closely.' : 'No action needed.'
    setAlertMsg(msg)
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
      <div style={{ gridColumn: 'span 1' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8, marginBottom: 12 }}>
          <button disabled={!samples} onClick={() => selectSample('safe')}>Sample: Safe</button>
          <button disabled={!samples} onClick={() => selectSample('caution')}>Sample: Caution</button>
          <button disabled={!samples} onClick={() => selectSample('high')}>Sample: High Risk</button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
          {Object.keys(defaultInput).map(key => (
            <label key={key} style={{ display: 'flex', flexDirection: 'column', fontSize: 12 }}>
              {key}
              <input
                type="number"
                step="any"
                name={key}
                value={form[key]}
                onChange={onChange}
                style={{ padding: 6 }}
              />
            </label>
          ))}
        </div>
        <div style={{ marginTop: 12 }}>
          <button onClick={onPredict} disabled={loading} style={{ padding: '8px 12px' }}>
            {loading ? 'Predicting…' : 'Predict Risk'}
          </button>
        </div>

        <div style={{ marginTop: 12 }}>
          <TrendChart data={trendData} />
        </div>
      </div>

      <div style={{ gridColumn: 'span 1', display: 'flex', flexDirection: 'column', gap: 12 }}>
        <Heatmap />
        <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 12 }}>
          <h3 style={{ marginTop: 0 }}>Risk Gauge</h3>
          <RiskGauge score={result?.risk_score || 0} />
          <div style={{ marginTop: 8, fontWeight: 600 }}>
            Level: {result?.risk_level || '—'}
          </div>
          {result?.reasons && (
            <ul>
              {result.reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          )}
          <button onClick={triggerAlert} disabled={!result} style={{ marginTop: 8 }}>
            Simulate Alert
          </button>
          {alertMsg && (
            <div style={{ marginTop: 8 }}>
              {alertMsg}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}