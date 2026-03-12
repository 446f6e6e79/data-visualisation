import React from 'react'

function StatusMessage({ loading, error }) {
  if (loading) {
    return <p className="status-message">Loading data from API...</p>
  }

  if (error) {
    return <p className="status-message status-error">Error: {error}</p>
  }

  return null
}

export default StatusMessage