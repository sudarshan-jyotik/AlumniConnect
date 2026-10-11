import apiClient from '@/lib/api-client';
import { ApiResponse } from '@/types';

export interface DashboardStats {
  stats: Array<{ label: string; value: string; type: string }>;
  chart_data: Array<{ name: string; referrals: number; applications: number }>;
  status_pie_data: Array<{ name: string; value: number; color: string }>;
  recent_activities: Array<{ id: number; title: string; desc: string; time: string; status: string }>;
}

export const userApi = {
  getDashboardStats: async (): Promise<ApiResponse<DashboardStats>> => {
    const response = await apiClient.get('/users/dashboard-stats');
    return response.data;
  },
};
