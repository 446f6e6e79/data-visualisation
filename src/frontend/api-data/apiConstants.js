export const API_BASE_URL = 'http://localhost:8000'

export const ENDPOINTS = {
  rideStatsByType: `${API_BASE_URL}/statistics/ride-types`,
  classicRideStats: `${API_BASE_URL}/statistics/ride-types/classic_bike`,
  electricRideStats: `${API_BASE_URL}/statistics/ride-types/electric_bike`,
  userStatsByType: `${API_BASE_URL}/statistics/user-types`,
  memberUserStats: `${API_BASE_URL}/statistics/user-types/member`,
  casualUserStats: `${API_BASE_URL}/statistics/user-types/casual`,
  dailyStats: `${API_BASE_URL}/statistics/day`
}