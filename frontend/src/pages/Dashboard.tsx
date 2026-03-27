import React, { useEffect, useState } from 'react'
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Activity,
} from 'lucide-react'
import { Card, StatCard, LoadingSpinner, Alert } from '../components/common/Card'
import api from '../services/api'
import { HealthResponse, ModelsStatusResponse } from '../types'
import { formatDate } from '../utils/helpers'

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [modelsStatus, setModelsStatus] = useState<ModelsStatusResponse | null>(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        const [healthData, statusData] = await Promise.all([
          api.getHealth(),
          api.getModelsStatus(),
        ])
        setHealth(healthData)
        setModelsStatus(statusData)
        setError(null)
      } catch (err) {
        setError(api.getErrorMessage(err))
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="section-title">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Real-time fraud detection and security monitoring
        </p>
      </div>

      {error && <Alert type="error" message={error} />}

      {/* System Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          label="System Status"
          value={health?.status === 'healthy' ? 'Healthy' : 'Degraded'}
          icon={<CheckCircle className="w-6 h-6" />}
          color={health?.status === 'healthy' ? 'green' : 'red'}
        />
        <StatCard
          label="Anomaly Detector"
          value={health?.models_loaded.anomaly_detector ? 'Active' : 'Inactive'}
          icon={<AlertTriangle className="w-6 h-6" />}
          color={health?.models_loaded.anomaly_detector ? 'green' : 'red'}
        />
        <StatCard
          label="Fraud Detector"
          value={health?.models_loaded.fraud_detector ? 'Active' : 'Inactive'}
          icon={<TrendingUp className="w-6 h-6" />}
          color={health?.models_loaded.fraud_detector ? 'green' : 'red'}
        />
        <StatCard
          label="Phishing Detector"
          value={health?.models_loaded.phishing_detector ? 'Active' : 'Inactive'}
          icon={<Activity className="w-6 h-6" />}
          color={health?.models_loaded.phishing_detector ? 'green' : 'red'}
        />
      </div>

      {/* Models Status */}
      {modelsStatus && (
        <Card>
          <h2 className="subsection-title">Detection Models Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(modelsStatus.models).map(([key, model]) => (
              <div
                key={key}
                className="flex items-start justify-between p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
              >
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white capitalize">
                    {key.replace(/_/g, ' ')}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Type: <span className="font-medium">{model.type}</span>
                  </p>
                  {model.model_path && (
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1 truncate">
                      {model.model_path}
                    </p>
                  )}
                </div>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  {model.status}
                </span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">
              Recent Activity
            </h3>
            <BarChart3 className="w-5 h-5 text-blue-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            242
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Transactions analyzed today
          </p>
        </Card>

        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">
              Fraud Attempts
            </h3>
            <AlertTriangle className="w-5 h-5 text-red-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            8
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Detected and blocked
          </p>
        </Card>

        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">
              Risk Level
            </h3>
            <Activity className="w-5 h-5 text-green-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Low
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            System operating normally
          </p>
        </Card>
      </div>

      {/* System Info */}
      <Card>
        <h2 className="subsection-title">System Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Status</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {health?.status}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Last Updated</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {health?.timestamp ? formatDate(health.timestamp) : 'N/A'}
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default Dashboard
