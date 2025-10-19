import { apiService } from './api'
import type {
  LoginRequest,
  SignupRequest,
  AuthResponse,
  UserProfileResponse,
  UpdateProfileRequest
} from '@/types'

export class AuthService {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiService.post<AuthResponse>('/api/v1/auth/signin', credentials)
    return response.data
  }

  async signup(userData: SignupRequest): Promise<AuthResponse> {
    const response = await apiService.post<AuthResponse>('/api/v1/auth/signup', userData)
    return response.data
  }

  async logout(): Promise<{ message: string }> {
    const response = await apiService.post<{ message: string }>('/api/v1/auth/signout')
    return response.data
  }

  async getProfile(): Promise<UserProfileResponse> {
    const response = await apiService.get<UserProfileResponse>('/api/v1/auth/profile')
    return response.data
  }

  async updateProfile(data: UpdateProfileRequest): Promise<UserProfileResponse> {
    const response = await apiService.put<UserProfileResponse>('/api/v1/auth/profile', data)
    return response.data
  }
}

export const authService = new AuthService()