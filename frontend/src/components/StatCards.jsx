import React from 'react';

const cards = [
  { key: 'total_logs',    label: 'Total Logs',      color: '#58a6ff', icon: '📋' },
  { key: 'total_alerts',  label: 'Total Alerts',    color: '#f0883e', icon: '🔔' },
  { key: 'high_alerts',   label: 'High Severity',   color: '#ff7b72', icon: '🔴' },
  { key: 'medium_alerts', label: 'Medium Severity', color: '#e3b341', icon: '🟡' },
  { key: 'low_alerts',    label: 'Low Severity',    color: '#3fb950', icon: '🟢' },
];

export default function StatCards({ stats }) {
  return (
    <div style={styles.grid}>
      {cards.map(card => (
        <div key={card.key} style={styles.card}>
          <div style={styles.icon}>{card.icon}</div>
          <div>
            <div style={{ ...styles.value, color: card.color }}>
              {stats[card.key] ?? 0}
            </div>
            <div style={styles.label}>{card.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(5, 1fr)',
    gap: '16px',
    marginBottom: '24px',
  },
  card: {
    background: '#161b22',
    border: '1px solid #30363d',
    borderRadius: '10px',
    padding: '20px',
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  icon: { fontSize: '28px' },
  value: { fontSize: '28px', fontWeight: 'bold' },
  label: { fontSize: '12px', color: '#8b949e', marginTop: '4px' },
};