import React from 'react'
import { ENDPOINTS } from '../api-data/apiConstants.js'

function useStatsData() {
  {/* State variables, used to store the statistics data */}
  const [rideStats, setRideStats] = React.useState([])
  const [userStats, setUserStats] = React.useState([])
  const [dailyStats, setDailyStats] = React.useState([])

  {/* Set the loading state to true when loading the page */}
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState(null)

  // useEffect to fetch all the stats data when the component mounts
  React.useEffect(() => {
    const fetchAll = async () => {
      try {
        // Fetch all the stats data in parallel using Promise.all
        const [classic, electric, member, casual, daily] = await Promise.all([
          fetch(ENDPOINTS.classicRideStats).then(r => r.json()),
          fetch(ENDPOINTS.electricRideStats).then(r => r.json()),
          fetch(ENDPOINTS.memberUserStats).then(r => r.json()),
          fetch(ENDPOINTS.casualUserStats).then(r => r.json()),
          fetch(ENDPOINTS.dailyStats).then(r => r.json()),
        ])
        // Convert duration from seconds to minutes for display purposes
        // and flatten the stats into the main object
        const toDisplayStats = (item) => ({
          ...item,
          ...item.stats,
          average_duration_minutes: item.stats.average_duration_seconds / 60,
          total_duration_minutes: item.stats.total_duration_seconds / 60,
        })
        
        setRideStats([classic, electric].map(toDisplayStats))
        setUserStats([member, casual].map(toDisplayStats))
        setDailyStats(daily.map(toDisplayStats))
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchAll()
  }, [])

  return { rideStats, userStats, dailyStats, loading, error }
}

export default useStatsData