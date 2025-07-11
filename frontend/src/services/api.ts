import axios from 'axios'
import type { 
  User, 
  Campaign, 
  CampaignFilters, 
  CreatorFilters, 
  LoginData, 
  RegisterData, 
  AuthResponse 
} from '../types'

const API_BASE_URL ='https://api.fastfluence.home.lineofcode.pl/'

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: (data: LoginData): Promise<AuthResponse> => 
    api.post('/auth/token', data, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(res => res.data),
  
  register: (data: RegisterData): Promise<User> =>
    api.post('/auth/register', data).then(res => res.data),
}

// User API
export const userApi = {
  getCurrentUser: (): Promise<User> =>
    api.get('/users/me').then(res => res.data),
  
  updateCurrentUser: (data: Partial<User>): Promise<User> =>
    api.put('/users/me', data).then(res => res.data),
  
  getUser: (id: number): Promise<User> =>
    api.get(`/users/${id}`).then(res => res.data),
}

// Campaign API
export const campaignApi = {
  getCampaigns: (filters?: CampaignFilters): Promise<Campaign[]> =>
    api.get('/campaigns', { params: filters }).then(res => res.data),
  
  getCampaign: (id: number): Promise<Campaign> =>
    api.get(`/campaigns/${id}`).then(res => res.data),
  
  createCampaign: (data: Partial<Campaign>): Promise<Campaign> =>
    api.post('/campaigns', data).then(res => res.data),
  
  updateCampaign: (id: number, data: Partial<Campaign>): Promise<Campaign> =>
    api.put(`/campaigns/${id}`, data).then(res => res.data),
  
  deleteCampaign: (id: number): Promise<void> =>
    api.delete(`/campaigns/${id}`).then(res => res.data),
}

// Creator API
export const creatorApi = {
  getCreators: (filters?: CreatorFilters): Promise<User[]> =>
    api.get('/creators', { params: filters }).then(res => res.data),
}