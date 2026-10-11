import apiClient from '@/lib/api-client';
import { ApiResponse, PaginationParams, ReferralRequest } from '@/types';

export interface AdminStats {
  pending_requests_count: number;
  approved_requests_count: number;
  fulfilled_requests_count: number;
  rejected_requests_count: number;
  total_requests_count: number;
  unverified_alumni_count: number;
  total_companies_count: number;
  total_users_count: number;
  approval_rate_percentage: number;
}

export interface AlumniVerificationItem {
  id: number;
  user_id: number;
  user_name?: string;
  user_email: string;
  current_company_id?: number;
  current_company_name?: string;
  current_position?: string;
  graduation_year?: number;
  degree?: string;
  department?: string;
  linkedin_url?: string;
  bio?: string;
  is_verified: boolean;
  verified_at?: string;
}

export const adminApi = {
  getStats: async (): Promise<ApiResponse<AdminStats>> => {
    const response = await apiClient.get('/admin/stats');
    return response.data;
  },

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

  getAlumniVerifications: async (): Promise<ApiResponse<AlumniVerificationItem[]>> => {
    const response = await apiClient.get('/admin/alumni-verifications');
    return response.data;
  },

  verifyAlumni: async (userId: number): Promise<ApiResponse<AlumniVerificationItem>> => {
    const response = await apiClient.post(`/admin/alumni/${userId}/verify`);
    return response.data;
  },

  rejectAlumni: async (userId: number): Promise<ApiResponse<AlumniVerificationItem>> => {
    const response = await apiClient.post(`/admin/alumni/${userId}/reject`);
    return response.data;
  },
};
