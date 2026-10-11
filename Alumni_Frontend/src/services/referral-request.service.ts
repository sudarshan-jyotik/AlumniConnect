import apiClient from '@/lib/api-client';
import { ApiResponse, PaginationParams, ReferralRequest } from '@/types';

export interface CreateReferralRequest {
  company_id: number;
  position_title: string;
  job_description?: string;
  job_url?: string;
  location?: string;
  motivation: string;
  skills_match?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
}

export interface UpdateReferralRequest {
  position_title?: string;
  job_description?: string;
  job_url?: string;
  location?: string;
  motivation?: string;
  skills_match?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
}

export const referralRequestApi = {
  getAll: async (params?: PaginationParams): Promise<ApiResponse<ReferralRequest[]>> => {
    const response = await apiClient.get('/referral-requests/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.get(`/referral-requests/${id}`);
    return response.data;
  },

  create: async (data: CreateReferralRequest): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.post('/referral-requests/', data);
    return response.data;
  },

  update: async (id: number, data: UpdateReferralRequest): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.put(`/referral-requests/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/referral-requests/${id}`);
  },

  submit: async (id: number): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.post(`/referral-requests/${id}/submit`);
    return response.data;
  },

  endorse: async (id: number): Promise<ApiResponse<ReferralRequest>> => {
    const response = await apiClient.post(`/referral-requests/${id}/endorse`);
    return response.data;
  },

  submitReferral: async (data: { request_id: number; notes?: string; confidence_level?: number }): Promise<ApiResponse<any>> => {
    const response = await apiClient.post('/referral-submissions/', data);
    return response.data;
  },
};
