import apiClient from '@/lib/api-client';
import { ApiResponse, AuthResponse, LoginRequest, RegisterRequest, User } from '@/types';

export const authApi = {
  login: async (data: LoginRequest): Promise<ApiResponse<AuthResponse>> => {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<ApiResponse<User>> => {
    const response = await apiClient.post('/auth/register', data);
    return response.data;
  },

  logout: async (refreshToken: string): Promise<void> => {
    await apiClient.post('/auth/logout', { refresh_token: refreshToken });
  },

  refreshToken: async (refreshToken: string): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  verifyEmail: async (token: string): Promise<ApiResponse<User>> => {
    const response = await apiClient.get(`/auth/verify/${token}`);
    return response.data;
  },

  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  loginWithGoogle: async (credential: string, role?: string): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post('/auth/google', { credential, role: role || 'student' });
    return response.data;
  },
};
