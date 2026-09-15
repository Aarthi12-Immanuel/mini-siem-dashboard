import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StatCards from './components/StatCards';
import Charts from './components/Charts';
import AlertTable from './components/AlertTable';

const API = 'http://localhost:5000/api';

export default function App() {
  const [stats, setStats]   = useState({});
  const [alerts, setAlerts] = useState([]);
  const [lastUpdated, setLastUpdated] = useState('');

  const fetchData = async () => {
    try {
      const [statsRes, alertsRes] = await Promise.all([
        axios.get(`${API}/stats`),
        axios.get(`${API}/alerts`),
      ]);
      setStats(statsRes.data);
      setAlerts(alertsRes.data);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      console.error('API error:', err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={styles.app}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>🛡️ Mini SIEM Dashboard</h1>
          <p style={styles.subtitle}>Real-time Security Information & Event Management</p>
        </div>
        <div style={styles.live}>
          <span style={styles.dot}></span>
          LIVE — Last updated: {lastUpdated}
        </div>
      </div>
      <StatCards stats={stats} />
      <Charts alerts={alerts} />
      <AlertTable alerts={alerts} />
    </div>
  );
}

const styles = {
  app: { maxWidth: '1400px', margin: '0 auto', padding: '24px' },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '24px',
    paddingBottom: '16px',
    borderBottom: '1px solid #30363d',
  },
  title: { fontSize: '22px', fontWeight: 'bold', color: '#e6edf3' },
  subtitle: { fontSize: '13px', color: '#8b949e', marginTop: '4px' },
  live: { display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#3fb950' },
  dot: {
    width: '8px',
    height: '8px',
    background: '#3fb950',
    borderRadius: '50%',
    display: 'inline-block',
  },
};