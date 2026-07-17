import apiClient from '@/lib/api-client';
import { ApiResponse, PaginationParams, ReferralRequest } from '@/types';

export const adminApi = {
  getPendingRequests: async (params?: PaginationParams): Promise<ApiResponse<ReferralRequest[]>> => {
    const response = await apiClient.get('/admin/pending-requests', { params });
    return response.data;
  },

  approveRequest: async (id: number): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.post(`/admin/requests/${id}/approve`);
    return response.data;
  },

  rejectRequest: async (id: number, reason: string): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.post(`/admin/requests/${id}/reject`, { reason });
    return response.data;
  },
};
