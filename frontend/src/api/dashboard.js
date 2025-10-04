import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const dashboardApi = {
  fetchOverview() {
    if (isMockEnabled) {
      return mockApi.dashboard.fetchOverview()
    }
    return apiRequest.get('/dashboard/overview')
  },
  fetchMetrics() {
    if (isMockEnabled) {
      return mockApi.dashboard.fetchMetrics()
    }
    return apiRequest.get('/dashboard/metrics')
  }
}
