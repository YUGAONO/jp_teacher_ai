export interface User {
  id: string
  email: string
  display_name: string
  locale: string
  current_plan: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface SignupRequest {
  email: string
  password: string
  display_name: string
  locale: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface UserProfileResponse {
  id: string
  email: string
  display_name: string
  locale: string
  current_plan: string
  created_at: string
  updated_at: string
}

export interface UpdateProfileRequest {
  display_name?: string
  locale?: string
  current_plan?: string
}