import React from 'react'
import { ENDPOINTS } from '../api-data/apiConstants.js'

function useStatsData() {
  const [rideStats, setRideStats] = React.useState([])
  const [userStats, setUserStats] = React.useState([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState(null)

  React.useEffect(() => {
    const fetchAll = async () => {
      try {
        const [classic, electric, member, casual] = await Promise.all([
          fetch(ENDPOINTS.classicRideStats).then(r => r.json()),
          fetch(ENDPOINTS.electricRideStats).then(r => r.json()),
          fetch(ENDPOINTS.memberUserStats).then(r => r.json()),
          fetch(ENDPOINTS.casualUserStats).then(r => r.json()),
        ])

        setRideStats([classic, electric])
        setUserStats([member, casual])
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchAll()
  }, [])

  return { rideStats, userStats, loading, error }
}

export default useStatsData