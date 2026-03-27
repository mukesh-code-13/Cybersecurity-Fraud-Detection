import { User, AuthResponse } from '../types'

class AuthService {
  private tokenKey = 'auth_token'
  private userKey = 'auth_user'

  // Mock authentication - replace with real API call
  async login(username: string, _password: string): Promise<AuthResponse> {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        const mockUser: User = {
          id: '1',
          username,
          email: `${username}@example.com`,
          role: 'analyst',
          created_at: new Date().toISOString(),
        }

        const mockToken = 'mock_token_' + Math.random().toString(36).substr(2, 9)

        this.setToken(mockToken)
        this.setUser(mockUser)

        resolve({
          access_token: mockToken,
          token_type: 'bearer',
          user: mockUser,
        })
      }, 500)
    })
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey)
    localStorage.removeItem(this.userKey)
  }

  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token)
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey)
  }

  setUser(user: User): void {
    localStorage.setItem(this.userKey, JSON.stringify(user))
  }

  getUser(): User | null {
    const user = localStorage.getItem(this.userKey)
    return user ? JSON.parse(user) : null
  }

  isAuthenticated(): boolean {
    return !!this.getToken()
  }
}

export default new AuthService()
