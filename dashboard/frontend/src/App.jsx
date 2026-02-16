import React, { useEffect, useMemo, useState } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function parseISODate(s) {
  // s: YYYY-MM-DD
  const [y, m, d] = s.split('-').map(Number)
  return new Date(y, m - 1, d)
}

function formatISODate(d) {
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

export default function App() {
  const [prices, setPrices] = useState([])
  const [events, setEvents] = useState([])
  const [cp, setCp] = useState(null)
  const [start, setStart] = useState('2012-01-01')
  const [end, setEnd] = useState('2022-09-30')

  useEffect(() => {
    async function loadAll() {
      const [p, e, c] = await Promise.all([
        fetch(`${API_BASE}/api/prices?start=${start}&end=${end}`).then((r) => r.json()),
        fetch(`${API_BASE}/api/events`).then((r) => r.json()),
        fetch(`${API_BASE}/api/changepoint`).then((r) => r.json()),
      ])
      setPrices(p)
      setEvents(e)
      setCp(c)
    }
    loadAll().catch(console.error)
  }, [start, end])

  const chartData = useMemo(() => {
    return prices.map((r) => ({
      date: r.date,
      price: r.price,
    }))
  }, [prices])

  const visibleEvents = useMemo(() => {
    const s = parseISODate(start)
    const t = parseISODate(end)
    return (events || []).filter((ev) => {
      const d = parseISODate(ev.event_date)
      return d >= s && d <= t
    })
  }, [events, start, end])

  const tauDate = cp?.tau_date_median
  const hdi = cp?.tau_date_hdi_94
  const nearest = cp?.nearest_event
  const impact = cp?.impact_stats_usd

  return (
    <div style={{ fontFamily: 'system-ui, Arial', padding: 16, maxWidth: 1100, margin: '0 auto' }}>
      <h2>Brent Oil Price - Change Point Dashboard</h2>
      <p style={{ marginTop: 0, color: '#444' }}>
        Explore Brent price history with curated events and a Bayesian change point estimate.
      </p>

      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'end' }}>
        <div>
          <label>Start</label>
          <div>
            <input type="date" value={start} onChange={(e) => setStart(e.target.value)} />
          </div>
        </div>
        <div>
          <label>End</label>
          <div>
            <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} />
          </div>
        </div>
        <div style={{ flex: 1 }} />
        <div style={{ fontSize: 13, color: '#333' }}>
          API: <code>{API_BASE}</code>
        </div>
      </div>

      <div style={{ height: 420, marginTop: 16, border: '1px solid #eee', borderRadius: 8, padding: 8 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" minTickGap={40} />
            <YAxis domain={['auto', 'auto']} />
            <Tooltip />
            <Line type="monotone" dataKey="price" stroke="#1f77b4" dot={false} name="Price" />
            {tauDate ? (
              <ReferenceLine x={tauDate} stroke="#d62728" strokeDasharray="6 4" label="tau (median)" />
            ) : null}
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 16 }}>
        <div style={{ border: '1px solid #eee', borderRadius: 8, padding: 12 }}>
          <h3 style={{ marginTop: 0 }}>Change point summary</h3>
          {!cp || Object.keys(cp).length === 0 ? (
            <p style={{ color: '#666' }}>No model summary found. Run Task 2 notebook to generate it.</p>
          ) : (
            <>
              <div><b>tau (median):</b> {tauDate}</div>
              {hdi ? <div><b>94% HDI:</b> {hdi[0]} to {hdi[1]}</div> : null}
              {impact ? (
                <div style={{ marginTop: 8 }}>
                  <div><b>90-day mean price (pre):</b> {impact.pre_mean_price_usd?.toFixed?.(2)} USD</div>
                  <div><b>90-day mean price (post):</b> {impact.post_mean_price_usd?.toFixed?.(2)} USD</div>
                  <div><b>% change (mean):</b> {impact.pct_change_mean_price?.toFixed?.(2)}%</div>
                </div>
              ) : null}
            </>
          )}
        </div>

        <div style={{ border: '1px solid #eee', borderRadius: 8, padding: 12 }}>
          <h3 style={{ marginTop: 0 }}>Nearest event</h3>
          {!nearest ? (
            <p style={{ color: '#666' }}>
              No nearby event found within the matching window.
            </p>
          ) : (
            <>
              <div><b>Date:</b> {nearest.event_date} ({nearest.abs_days} days away)</div>
              <div><b>Title:</b> {nearest.event_title}</div>
              <div><b>Type:</b> {nearest.event_type}</div>
              <div><b>Region:</b> {nearest.region}</div>
              <div style={{ marginTop: 8, color: '#444' }}>{nearest.notes}</div>
            </>
          )}
        </div>
      </div>

      <div style={{ marginTop: 16, border: '1px solid #eee', borderRadius: 8, padding: 12 }}>
        <h3 style={{ marginTop: 0 }}>Events in selected range</h3>
        {visibleEvents.length === 0 ? (
          <p style={{ color: '#666' }}>No events in the selected range.</p>
        ) : (
          <ul>
            {visibleEvents.map((ev) => (
              <li key={`${ev.event_date}-${ev.event_title}`}>
                <b>{ev.event_date}</b> - {ev.event_title} ({ev.event_type})
              </li>
            ))}
          </ul>
        )}
      </div>

      <p style={{ marginTop: 24, color: '#666', fontSize: 12 }}>
        Note: visual alignment of events and change points indicates temporal association, not proof of causality.
      </p>
    </div>
  )
}
