import React, { useState } from 'react'
import { Send, Mail, AlertTriangle } from 'lucide-react'
import { Card, Button, Badge } from '../components/common/Card'
import api from '../services/api'
import { EmailData, PhishingDetectionResponse } from '../types'

import toast from 'react-hot-toast'

const PhishingDetection: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PhishingDetectionResponse | null>(null)
  const [formData, setFormData] = useState<EmailData>({
    sender: '',
    display_name: '',
    subject: '',
    body: '',
    recipient: '',
  })

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleDetect = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.sender || !formData.subject || !formData.body) {
      toast.error('Please fill in sender, subject, and body')
      return
    }

    try {
      setLoading(true)
      const response = await api.detectPhishing(formData)
      setResult(response)
      toast.success('Email analyzed successfully')
    } catch (error) {
      toast.error(api.getErrorMessage(error))
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (risk: number) => {
    if (risk > 0.7) return 'text-red-600'
    if (risk > 0.4) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getRiskBg = (risk: number) => {
    if (risk > 0.7) return 'bg-red-50 dark:bg-red-900/20'
    if (risk > 0.4) return 'bg-yellow-50 dark:bg-yellow-900/20'
    return 'bg-green-50 dark:bg-green-900/20'
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="section-title">Phishing Detection</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Analyze emails for phishing and suspicious content
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form */}
        <div className="lg:col-span-1">
          <Card>
            <h2 className="subsection-title">Analyze Email</h2>
            <form onSubmit={handleDetect} className="space-y-4">
              <div>
                <label className="label">Sender Email *</label>
                <input
                  type="email"
                  name="sender"
                  value={formData.sender}
                  onChange={handleInputChange}
                  placeholder="sender@example.com"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label">Display Name</label>
                <input
                  type="text"
                  name="display_name"
                  value={formData.display_name || ''}
                  onChange={handleInputChange}
                  placeholder="John Doe"
                  className="input-field"
                />
              </div>

              <div>
                <label className="label">Recipient</label>
                <input
                  type="email"
                  name="recipient"
                  value={formData.recipient || ''}
                  onChange={handleInputChange}
                  placeholder="recipient@example.com"
                  className="input-field"
                />
              </div>

              <div>
                <label className="label">Subject *</label>
                <input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleInputChange}
                  placeholder="Email subject"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label">Body *</label>
                <textarea
                  name="body"
                  value={formData.body}
                  onChange={handleInputChange}
                  placeholder="Email content"
                  rows={6}
                  className="input-field resize-none"
                  required
                ></textarea>
              </div>

              <Button
                type="submit"
                variant="primary"
                loading={loading}
                className="w-full flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" />
                Analyze Email
              </Button>
            </form>
          </Card>
        </div>

        {/* Results */}
        <div className="lg:col-span-2">
          {result ? (
            <div className="space-y-6">
              {/* Overall Result */}
              <Card className={result.is_phishing ? 'border-l-4 border-red-500' : ''}>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="subsection-title">Detection Result</h2>
                  {result.is_phishing ? (
                    <Badge variant="danger">PHISHING DETECTED</Badge>
                  ) : (
                    <Badge variant="success">LEGITIMATE</Badge>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className={`p-4 rounded-lg ${getRiskBg(result.phishing_score)}`}>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Phishing Confidence
                    </p>
                    <p className={`text-2xl font-bold ${getRiskColor(result.phishing_score)}`}>
                      {(result.phishing_score * 100).toFixed(2)}%
                    </p>
                  </div>
                  <div className={`p-4 rounded-lg ${getRiskBg(result.confidence)}`}>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Analysis Confidence
                    </p>
                    <p className={`text-2xl font-bold ${getRiskColor(result.confidence)}`}>
                      {(result.confidence * 100).toFixed(2)}%
                    </p>
                  </div>
                </div>
              </Card>

              {/* Risk Components */}
              <Card>
                <h3 className="subsection-title">Risk Components</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Sender Risk
                      </span>
                      <span className={`text-sm font-semibold ${getRiskColor(result.sender_risk)}`}>
                        {(result.sender_risk * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          result.sender_risk > 0.7
                            ? 'bg-red-600'
                            : result.sender_risk > 0.4
                              ? 'bg-yellow-600'
                              : 'bg-green-600'
                        }`}
                        style={{ width: `${result.sender_risk * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Content Risk
                      </span>
                      <span className={`text-sm font-semibold ${getRiskColor(result.content_risk)}`}>
                        {(result.content_risk * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          result.content_risk > 0.7
                            ? 'bg-red-600'
                            : result.content_risk > 0.4
                              ? 'bg-yellow-600'
                              : 'bg-green-600'
                        }`}
                        style={{ width: `${result.content_risk * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        URL Risk
                      </span>
                      <span className={`text-sm font-semibold ${getRiskColor(result.url_risk)}`}>
                        {(result.url_risk * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          result.url_risk > 0.7
                            ? 'bg-red-600'
                            : result.url_risk > 0.4
                              ? 'bg-yellow-600'
                              : 'bg-green-600'
                        }`}
                        style={{ width: `${result.url_risk * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Indicators */}
              {result.indicators.length > 0 && (
                <Card>
                  <h3 className="subsection-title">Detected Indicators</h3>
                  <div className="space-y-2">
                    {result.indicators.map((indicator, idx) => (
                      <div
                        key={idx}
                        className="flex items-center gap-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg"
                      >
                        <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
                        <span className="text-sm text-red-800 dark:text-red-200">
                          {indicator}
                        </span>
                      </div>
                    ))}
                  </div>
                </Card>
              )}

              {/* Suspicious URLs */}
              {result.suspicious_urls.length > 0 && (
                <Card>
                  <h3 className="subsection-title">Suspicious URLs</h3>
                  <div className="space-y-2">
                    {result.suspicious_urls.map((url, idx) => (
                      <div
                        key={idx}
                        className="flex items-start gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg"
                      >
                        <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-1" />
                        <span className="text-sm text-yellow-800 dark:text-yellow-200 break-all">
                          {url}
                        </span>
                      </div>
                    ))}
                  </div>
                </Card>
              )}
            </div>
          ) : (
            <Card>
              <div className="flex flex-col items-center justify-center py-12">
                <Mail className="w-12 h-12 text-gray-400 mb-4" />
                <p className="text-gray-600 dark:text-gray-400">
                  Enter email details and click "Analyze Email" to check for phishing
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default PhishingDetection
