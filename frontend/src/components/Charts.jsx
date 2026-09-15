import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  PieChart, Pie, Cell, ResponsiveContainer, Legend
} from 'recharts';

const SEVERITY_COLORS = {
  HIGH:   '#ff7b72',
  MEDIUM: '#e3b341',
  LOW:    '#3fb950',
};

export default function Charts({ alerts }) {
  const threatCounts = alerts.reduce((acc, alert) => {
    acc[alert.threat_type] = (acc[alert.threat_type] || 0) + 1;
    return acc;
  }, {});

  const barData = Object.entries(threatCounts).map(([name, count]) => ({
    name: name.replace(/_/g, ' '),
    count
  }));

  const severityCounts = alerts.reduce((acc, alert) => {
    acc[alert.severity] = (acc[alert.severity] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(severityCounts).map(([name, value]) => ({
    name, value
  }));

  return (
    <div style={styles.row}>
      <div style={styles.chartBox}>
        <h3 style={styles.title}>🔍 Alerts by Threat Type</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={barData}>
            <XAxis dataKey="name" tick={{ fill: '#8b949e', fontSize: 10 }} />
            <YAxis tick={{ fill: '#8b949e' }} />
            <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d' }} />
            <Bar dataKey="count" fill="#58a6ff" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div style={styles.chartBox}>
        <h3 style={styles.title}>⚠️ Severity Breakdown</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              outerRadius={90}
              dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            >
              {pieData.map((entry) => (
                <Cell key={entry.name} fill={SEVERITY_COLORS[entry.name] || '#58a6ff'} />
              ))}
            </Pie>
            <Legend />
            <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d' }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

const styles = {
  row: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '16px',
    marginBottom: '24px',
  },
  chartBox: {
    background: '#161b22',
    border: '1px solid #30363d',
    borderRadius: '10px',
    padding: '20px',
  },
  title: { fontSize: '14px', color: '#8b949e', marginBottom: '16px' },
};