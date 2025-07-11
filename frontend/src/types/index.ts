export interface User {
  id: number
  email: string
  role: 'advertiser' | 'creator'
  display_name: string
  contact_email: string
  phone?: string
  website_url?: string
  social_links: string[]
  portfolio: PortfolioCampaign[]
  created_at: string
}

export interface PortfolioCampaign {
  title: string
  brand_name: string
  role_in_campaign: string
  landing_url?: string
  cover_image_url?: string
  short_description: string
}

export interface Campaign {
  id: number
  owner_id: number
  title: string
  description: string
  category: string
  media_channel: MediaChannel
  location: string
  compensation: CompensationType
  budget_min?: number
  budget_max?: number
  barter_descr?: string
  deadline: string
  created_at: string
  owner: User
}

export type MediaChannel = 'Instagram' | 'TikTok' | 'YouTube' | 'Blog' | 'Facebook' | 'LinkedIn' | 'Other'
export type CompensationType = 'Cash' | 'Barter' | 'Mixed'
export type UserRole = 'advertiser' | 'creator'

export interface CampaignFilters {
  search?: string
  category?: string
  media_channel?: MediaChannel
  location?: string
  compensation?: CompensationType
  min_budget?: number
  max_budget?: number
  limit?: number
  offset?: number
}

export interface CreatorFilters {
  search?: string
  category?: string
  media_channel?: MediaChannel
  location?: string
  limit?: number
  offset?: number
}

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  role: UserRole
  display_name: string
  contact_email: string
  phone?: string
  website_url?: string
  social_links?: string[]
  portfolio?: PortfolioCampaign[]
}

export interface AuthResponse {
  access_token: string
  token_type: string
}