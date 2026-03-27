import React, { useState } from 'react'
import { Send, Activity, AlertTriangle } from 'lucide-react'
import { Card, Button, Badge } from '../components/common/Card'
import api from '../services/api'
import { BehaviorAnalysisRequest, BehaviorAnalysisResponse } from '../types'
import toast from 'react-hot-toast'

const BehaviorAnalysis: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<BehaviorAnalysisResponse | null>(null)
  const [formData, setFormData] = useState<BehaviorAnalysisRequest>({
    user_id: '',
    behavior_type: 'login',
    metrics: {
      login_time: 'morning',
      location: 'home',
      device_type: 'desktop',
      failed_attempts: 0,
    },
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleMetricsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      metrics: {
        ...prev.metrics,
        [name]: isNaN(Number(value)) ? value : Number(value),
      },
    }))
  }

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.user_id) {
      toast.error('Please enter a user ID')
      return
    }

    try {
      setLoading(true)
      const response = await api.analyzeBehavior(formData)
      setResult(response)
      toast.success('Behavior analyzed successfully')
    } catch (error) {
      toast.error(api.getErrorMessage(error))
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'text-red-600'
      case 'medium':
        return 'text-yellow-600'
      case 'low':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  const getSeverityBg = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-50 dark:bg-red-900/20'
      case 'medium':
        return 'bg-yellow-50 dark:bg-yellow-900/20'
      case 'low':
        return 'bg-green-50 dark:bg-green-900/20'
      default:
        return 'bg-gray-50 dark:bg-gray-900/20'
    }
  }

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'danger'
      case 'medium':
        return 'warning'
      case 'low':
        return 'success'
      default:
        return 'info'
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="section-title">Behavior Analysis</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Detect anomalies in user behavior patterns
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form */}
        <div className="lg:col-span-1">
          <Card>
            <h2 className="subsection-title">Analyze Behavior</h2>
            <form onSubmit={handleAnalyze} className="space-y-4">
              <div>
                <label className="label">User ID *</label>
                <input
                  type="text"
                  name="user_id"
                  value={formData.user_id}
                  onChange={handleInputChange}
                  placeholder="user123"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label">Behavior Type</label>
                <select
                  name="behavior_type"
                  value={formData.behavior_type}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  <option value="login">Login Pattern</option>
                  <option value="access_pattern">Access Pattern</option>
                </select>
              </div>

              <div className="border-t pt-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                  Metrics
                </h3>

                {formData.behavior_type === 'login' ? (
                  <>
                    <div className="mb-3">
                      <label className="label">Login Time</label>
                      <input
                        type="text"
                        name="login_time"
                        value={formData.metrics.login_time || ''}
                        onChange={handleMetricsChange}
                        placeholder="morning, afternoon, night"
                        className="input-field"
                      />
                    </div>
                    <div className="mb-3">
                      <label className="label">Location</label>
                      <input
                        type="text"
                        name="location"
                        value={formData.metrics.location || ''}
                        onChange={handleMetricsChange}
                        placeholder="home, office, travel"
                        className="input-field"
                      />
                    </div>
                    <div className="mb-3">
                      <label className="label">Device Type</label>
                      <input
                        type="text"
                        name="device_type"
                        value={formData.metrics.device_type || ''}
                        onChange={handleMetricsChange}
                        placeholder="desktop, mobile, tablet"
                        className="input-field"
                      />
                    </div>
                    <div>
                      <label className="label">Failed Attempts</label>
                      <input
                        type="number"
                        name="failed_attempts"
                        value={formData.metrics.failed_attempts || 0}
                        onChange={handleMetricsChange}
                        min="0"
                        className="input-field"
                      />
                    </div>
                  </>
                ) : (
                  <>
                    <div className="mb-3">
                      <label className="label">Access Time</label>
                      <input
                        type="text"
                        name="access_time"
                        value={formData.metrics.access_time || ''}
                        onChange={handleMetricsChange}
                        placeholder="morning, afternoon, night"
                        className="input-field"
                      />
                    </div>
                    <div className="mb-3">
                      <label className="label">Resources Accessed</label>
                      <input
                        type="number"
                        name="resources_accessed"
                        value={formData.metrics.resources_accessed || 0}
                        onChange={handleMetricsChange}
                        min="0"
                        className="input-field"
                      />
                    </div>
                    <div>
                      <label className="label">Access Velocity</label>
                      <input
                        type="number"
                        name="access_velocity"
                        value={formData.metrics.access_velocity || 0}
                        onChange={handleMetricsChange}
                        step="0.1"
                        min="0"
                        className="input-field"
                      />
                    </div>
                  </>
                )}
              </div>

              <Button
                type="submit"
                variant="primary"
                loading={loading}
                className="w-full flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" />
                Analyze Behavior
              </Button>
            </form>
          </Card>
        </div>

        {/* Results */}
        <div className="lg:col-span-2">
          {result ? (
            <div className="space-y-6">
              {/* Summary */}
              <Card>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="subsection-title">Analysis Result</h2>
                  <Badge variant={getSeverityBadge(result.severity) as any}>
                    {result.severity.toUpperCase()}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">User</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {result.user_id}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Status</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {result.is_anomalous ? 'Anomalous' : 'Normal'}
                    </p>
                  </div>
                </div>
              </Card>

              {/* Anomaly Score */}
              <Card>
                <h3 className="subsection-title">Anomaly Score</h3>
                <div className="mb-4">
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Score
                    </span>
                    <span
                      className={`text-sm font-semibold ${getSeverityColor(result.severity)}`}
                    >
                      {(result.anomaly_score * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full ${
                        result.severity === 'high'
                          ? 'bg-red-600'
                          : result.severity === 'medium'
                            ? 'bg-yellow-600'
                            : 'bg-green-600'
                      }`}
                      style={{ width: `${result.anomaly_score * 100}%` }}
                    ></div>
                  </div>
                </div>

                <div className="p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Severity</p>
                  <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getSeverityBg(result.severity)}`}>
                    <span className={getSeverityColor(result.severity)}>
                      {result.severity.toUpperCase()}
                    </span>
                  </div>
                </div>
              </Card>

              {/* Details */}
              {Object.keys(result.details).length > 0 && (
                <Card>
                  <h3 className="subsection-title">Behavior Details</h3>
                  <div className="space-y-3">
                    {Object.entries(result.details).map(([key, value]) => (
                      <div
                        key={key}
                        className="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
                      >
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                          {key.replace(/_/g, ' ')}
                        </span>
                        <span className="text-sm text-gray-900 dark:text-white font-semibold">
                          {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                        </span>
                      </div>
                    ))}
                  </div>
                </Card>
              )}

              {/* Alert */}
              {result.is_anomalous && (
                <Card className="border-l-4 border-yellow-500">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                        Anomaly Detected
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Unusual behavior pattern detected for this user. Recommend manual review and
                        possible verification.
                      </p>
                    </div>
                  </div>
                </Card>
              )}
            </div>
          ) : (
            <Card>
              <div className="flex flex-col items-center justify-center py-12">
                <Activity className="w-12 h-12 text-gray-400 mb-4" />
                <p className="text-gray-600 dark:text-gray-400">
                  Enter user details and click "Analyze Behavior" to detect anomalies
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default BehaviorAnalysis
