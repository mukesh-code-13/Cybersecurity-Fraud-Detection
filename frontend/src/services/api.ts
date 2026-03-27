import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosError, AxiosResponse } from 'axios'
import {
  TransactionRequest,
  TransactionResponse,
  EmailData,
  PhishingDetectionResponse,
  BehaviorAnalysisRequest,
  BehaviorAnalysisResponse,
  HealthResponse,
  ModelsStatusResponse,
  RiskSummary,
} from '../types'

const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    })

    // Add request interceptor
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error: AxiosError) => Promise.reject(error)
    )

    // Add response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Health & Status endpoints
  async getHealth(): Promise<HealthResponse> {
    const response = await this.client.get('/api/v1/health')
    return response.data
  }

  async getModelsStatus(): Promise<ModelsStatusResponse> {
    const response = await this.client.get('/api/v1/models/status')
    return response.data
  }

  async getRiskSummary(): Promise<RiskSummary> {
    const response = await this.client.get('/api/v1/alerts/risk-summary')
    return response.data
  }

  // Transaction Analysis
  async analyzeTransaction(data: TransactionRequest): Promise<TransactionResponse> {
    const response = await this.client.post('/api/v1/transactions/analyze', data)
    return response.data
  }

  async getTransactionHistory(userId: string): Promise<TransactionResponse[]> {
    const response = await this.client.get(`/api/v1/transactions/history?user_id=${userId}`)
    return response.data
  }

  // Phishing Detection
  async detectPhishing(data: EmailData): Promise<PhishingDetectionResponse> {
    const response = await this.client.post('/api/v1/phishing/detect', data)
    return response.data
  }

  // Behavioral Analysis
  async analyzeBehavior(data: BehaviorAnalysisRequest): Promise<BehaviorAnalysisResponse> {
    const response = await this.client.post('/api/v1/behavior/analyze', data)
    return response.data
  }

  async updateBaseline(userId: string, metrics: Record<string, any>): Promise<any> {
    const response = await this.client.post(
      `/api/v1/models/update-baseline?user_id=${userId}`,
      { metrics }
    )
    return response.data
  }

  // Error handling
  getErrorMessage(error: any): string {
    if (error.response?.data?.detail) {
      return error.response.data.detail
    }
    if (error.message) {
      return error.message
    }
    return 'An error occurred'
  }
}

export default new APIClient()
