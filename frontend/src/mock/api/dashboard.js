import { mockDashboard } from '../data/dashboard'
import { simulateResponse } from '../utils'

export const dashboardMockApi = {
  fetchOverview: async () => simulateResponse(mockDashboard.summaryCards),
  fetchMetrics: async () => simulateResponse(mockDashboard)
}
