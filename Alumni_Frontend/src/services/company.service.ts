import apiClient from '@/lib/api-client';
import { ApiResponse, Company, PaginationParams } from '@/types';

export interface CreateCompany {
  name: string;
  industry?: string;
  website?: string;
  description?: string;
  headquarters?: string;
}

export const companyApi = {
  getAll: async (params?: PaginationParams & { search?: string }): Promise<ApiResponse<Company[]>> => {
    const response = await apiClient.get('/companies/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<ApiResponse<Company>> => {
    const response = await apiClient.get(`/companies/${id}`);
    return response.data;
  },

  search: async (query: string, params?: PaginationParams): Promise<ApiResponse<Company[]>> => {
    const response = await apiClient.get('/companies/search', {
      params: { q: query, ...params },
    });
    return response.data;
  },

  create: async (data: CreateCompany): Promise<ApiResponse<Company>> => {
    const response = await apiClient.post('/companies/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<CreateCompany>): Promise<ApiResponse<Company>> => {
    const response = await apiClient.put(`/companies/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/companies/${id}`);
  },
};
