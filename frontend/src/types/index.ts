// API Response Types
export interface TransactionRequest {
  user_id: string
  amount: number
  merchant: string
  transaction_type: string
  device_id?: string
  ip_address?: string
  location?: string
}

export interface TransactionResponse {
  user_id: string
  amount: number
  is_anomalous: boolean
  is_fraudulent: boolean
  anomaly_score: number
  fraud_score: number
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  timestamp: string
}

export interface EmailData {
  sender: string
  display_name?: string
  subject: string
  body: string
  recipient?: string
}

export interface PhishingDetectionResponse {
  is_phishing: boolean
  phishing_score: number
  confidence: number
  sender_risk: number
  content_risk: number
  url_risk: number
  suspicious_urls: string[]
  indicators: string[]
}

export interface BehaviorAnalysisRequest {
  user_id: string
  behavior_type: 'login' | 'access_pattern'
  metrics: Record<string, any>
}

export interface BehaviorAnalysisResponse {
  user_id: string
  is_anomalous: boolean
  anomaly_score: number
  severity: 'low' | 'medium' | 'high'
  details: Record<string, any>
}

export interface HealthResponse {
  status: string
  models_loaded: {
    anomaly_detector: boolean
    fraud_detector: boolean
    phishing_detector: boolean
    behavioral_analyzer: boolean
  }
  timestamp: string
}

export interface ModelStatus {
  type: string
  status: string
  model_path?: string
  feature_importance?: Record<string, number>
}

export interface ModelsStatusResponse {
  status: string
  models: {
    anomaly_detector: ModelStatus
    fraud_detector: ModelStatus
    phishing_detector: ModelStatus
    behavioral_analyzer: ModelStatus
  }
  timestamp: string
}

export interface RiskSummary {
  total_transactions: number
  fraudulent_count: number
  anomalous_count: number
  phishing_count: number
  overall_risk_level: string
  timestamp: string
}

// Auth Types
export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'analyst' | 'user'
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

// UI Types
export interface Alert {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}

export interface AnalysisResult {
  id: string
  type: 'transaction' | 'phishing' | 'behavior'
  result: TransactionResponse | PhishingDetectionResponse | BehaviorAnalysisResponse
  timestamp: string
}
