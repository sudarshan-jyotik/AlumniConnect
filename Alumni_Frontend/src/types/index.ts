// User types
export type UserRole = 'student' | 'alumni' | 'admin';
export type UserStatus = 'pending' | 'active' | 'suspended' | 'inactive';

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  phone: string | null;
  role: UserRole;
  status: UserStatus;
  is_email_verified: boolean;
  created_at: string;
}

// Company types
export interface Company {
  id: number;
  name: string;
  industry: string | null;
  website: string | null;
  description: string | null;
  logo_url: string | null;
  headquarters: string | null;
  is_active: boolean;
  created_at: string;
}

// Referral Request types
export type RequestStatus = 'draft' | 'pending' | 'approved' | 'rejected' | 'fulfilled' | 'closed';
export type RequestPriority = 'low' | 'medium' | 'high' | 'urgent';

export interface ReferralRequest {
  id: number;
  student_id: number;
  company_id: number;
  position_title: string;
  job_description: string | null;
  job_url: string | null;
  location: string | null;
  motivation: string;
  skills_match: string | null;
  status: RequestStatus;
  priority: RequestPriority;
  submitted_at: string | null;
  approved_at: string | null;
  view_count: number;
  endorsement_count: number;
  created_at: string;
  updated_at: string;
  student: User;
  company: Company;
}

// Referral Submission types
export type SubmissionStatus = 
  | 'pending' 
  | 'approved' 
  | 'rejected' 
  | 'submitted_to_company'
  | 'interview_scheduled'
  | 'offer_received'
  | 'rejected_by_company'
  | 'withdrawn';

export interface ReferralSubmission {
  id: number;
  request_id: number;
  alumni_id: number;
  notes: string | null;
  confidence_level: number;
  status: SubmissionStatus;
  approved_at: string | null;
  created_at: string;
}

// Auth types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name?: string;
  phone?: string;
  role: UserRole;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// API Response wrapper
export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

// Pagination
export interface PaginationParams {
  skip?: number;
  limit?: number;
}

// Stats for dashboard
export interface DashboardStats {
  total_requests: number;
  pending_requests: number;
  approved_requests: number;
  my_submissions?: number;
  success_rate?: number;
}
