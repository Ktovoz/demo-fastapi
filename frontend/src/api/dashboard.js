import { apiRequest } from '../utils/api'

export const dashboardApi = {
  fetchOverview() {
    return apiRequest.get('/dashboard/overview')
  },
  fetchMetrics() {
    return apiRequest.get('/dashboard/metrics')
  }
}
