import React from 'react';

const SEVERITY_COLORS = {
  HIGH:   { bg: '#3d1a1a', text: '#ff7b72', border: '#ff7b72' },
  MEDIUM: { bg: '#2d2010', text: '#e3b341', border: '#e3b341' },
  LOW:    { bg: '#112d1a', text: '#3fb950', border: '#3fb950' },
};

export default function AlertTable({ alerts }) {
  return (
    <div style={styles.container}>
      <h3 style={styles.title}>🚨 Live Alert Feed</h3>
      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr>
              {['Time', 'User', 'IP', 'Threat Type', 'Severity', 'Score', 'Description'].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {alerts.length === 0 ? (
              <tr>
                <td colSpan={7} style={styles.empty}>No alerts detected yet...</td>
              </tr>
            ) : (
              alerts.map(alert => {
                const colors = SEVERITY_COLORS[alert.severity] || SEVERITY_COLORS.LOW;
                return (
                  <tr key={alert.id}>
                    <td style={styles.td}>{alert.timestamp}</td>
                    <td style={styles.td}>{alert.user}</td>
                    <td style={{ ...styles.td, fontFamily: 'monospace', color: '#58a6ff' }}>
                      {alert.ip}
                    </td>
                    <td style={styles.td}>{alert.threat_type.replace(/_/g, ' ')}</td>
                    <td style={styles.td}>
                      <span style={{
                        background: colors.bg,
                        color: colors.text,
                        border: `1px solid ${colors.border}`,
                        padding: '2px 10px',
                        borderRadius: '20px',
                        fontSize: '11px',
                        fontWeight: 'bold',
                      }}>
                        {alert.severity}
                      </span>
                    </td>
                    <td style={{ ...styles.td, color: colors.text, fontWeight: 'bold' }}>
                      {alert.score}
                    </td>
                    <td style={{ ...styles.td, color: '#8b949e', fontSize: '12px' }}>
                      {alert.description}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: '#161b22',
    border: '1px solid #30363d',
    borderRadius: '10px',
    padding: '20px',
  },
  title: { fontSize: '14px', color: '#8b949e', marginBottom: '16px' },
  tableWrapper: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: {
    textAlign: 'left',
    padding: '10px 14px',
    fontSize: '12px',
    color: '#8b949e',
    borderBottom: '1px solid #30363d',
    whiteSpace: 'nowrap',
  },
  td: {
    padding: '10px 14px',
    fontSize: '13px',
    borderBottom: '1px solid #21262d',
    whiteSpace: 'nowrap',
  },
  empty: { textAlign: 'center', padding: '40px', color: '#8b949e' },
};