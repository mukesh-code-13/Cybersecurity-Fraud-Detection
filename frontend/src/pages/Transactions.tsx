import React, { useState } from 'react'
import { Send, AlertCircle } from 'lucide-react'
import { Card, Button, Badge } from '../components/common/Card'
import api from '../services/api'
import { TransactionRequest, TransactionResponse } from '../types'
import { getRiskBadgeColor, formatAmount, formatDate } from '../utils/helpers'
import toast from 'react-hot-toast'

const Transactions: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<TransactionResponse | null>(null)
  const [formData, setFormData] = useState<TransactionRequest>({
    user_id: '',
    amount: 0,
    merchant: '',
    transaction_type: 'purchase',
    device_id: '',
    ip_address: '192.168.1.1',
    location: 'US',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) : value,
    }))
  }

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.user_id || !formData.amount || !formData.merchant) {
      toast.error('Please fill in all required fields')
      return
    }

    try {
      setLoading(true)
      const response = await api.analyzeTransaction(formData)
      setResult(response)
      toast.success('Transaction analyzed successfully')
    } catch (error) {
      toast.error(api.getErrorMessage(error))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="section-title">Transaction Analysis</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Analyze transactions for fraud and anomalies in real-time
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form */}
        <div className="lg:col-span-1">
          <Card>
            <h2 className="subsection-title">New Transaction</h2>
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
                <label className="label">Amount (USD) *</label>
                <input
                  type="number"
                  name="amount"
                  value={formData.amount || ''}
                  onChange={handleInputChange}
                  placeholder="100.00"
                  step="0.01"
                  min="0"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label">Merchant *</label>
                <input
                  type="text"
                  name="merchant"
                  value={formData.merchant}
                  onChange={handleInputChange}
                  placeholder="Amazon"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label">Transaction Type</label>
                <select
                  name="transaction_type"
                  value={formData.transaction_type}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  <option value="purchase">Purchase</option>
                  <option value="transfer">Transfer</option>
                  <option value="withdrawal">Withdrawal</option>
                  <option value="deposit">Deposit</option>
                </select>
              </div>

              <div>
                <label className="label">Device ID</label>
                <input
                  type="text"
                  name="device_id"
                  value={formData.device_id || ''}
                  onChange={handleInputChange}
                  placeholder="device_abc123"
                  className="input-field"
                />
              </div>

              <div>
                <label className="label">IP Address</label>
                <input
                  type="text"
                  name="ip_address"
                  value={formData.ip_address || ''}
                  onChange={handleInputChange}
                  placeholder="192.168.1.1"
                  className="input-field"
                />
              </div>

              <div>
                <label className="label">Location</label>
                <input
                  type="text"
                  name="location"
                  value={formData.location || ''}
                  onChange={handleInputChange}
                  placeholder="US"
                  className="input-field"
                />
              </div>

              <Button
                type="submit"
                variant="primary"
                loading={loading}
                className="w-full flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" />
                Analyze Transaction
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
                <h2 className="subsection-title">Analysis Results</h2>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">User</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {result.user_id}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Amount</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {formatAmount(result.amount)}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-400">Anomaly</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {result.is_anomalous ? 'Yes' : 'No'}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                      Score: {(result.anomaly_score * 100).toFixed(2)}%
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-400">Fraudulent</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {result.is_fraudulent ? 'Yes' : 'No'}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                      Score: {(result.fraud_score * 100).toFixed(2)}%
                    </p>
                  </div>
                </div>
              </Card>

              {/* Risk Level */}
              <Card>
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    Risk Level
                  </h3>
                  <Badge variant={getRiskBadgeColor(result.risk_level) as any}>
                    {result.risk_level.toUpperCase()}
                  </Badge>
                </div>
              </Card>

              {/* Scores */}
              <Card>
                <h3 className="subsection-title">Detection Scores</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Anomaly Score
                      </span>
                      <span className="text-sm font-semibold text-gray-900 dark:text-white">
                        {(result.anomaly_score * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${result.anomaly_score * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Fraud Score
                      </span>
                      <span className="text-sm font-semibold text-gray-900 dark:text-white">
                        {(result.fraud_score * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                      <div
                        className="bg-red-600 h-2 rounded-full"
                        style={{ width: `${result.fraud_score * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Timestamp */}
              <Card>
                <p className="text-sm text-gray-600 dark:text-gray-400">Analyzed At</p>
                <p className="text-gray-900 dark:text-white">
                  {formatDate(result.timestamp)}
                </p>
              </Card>
            </div>
          ) : (
            <Card>
              <div className="flex flex-col items-center justify-center py-12">
                <AlertCircle className="w-12 h-12 text-gray-400 mb-4" />
                <p className="text-gray-600 dark:text-gray-400">
                  Fill in the form and click "Analyze Transaction" to see results
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default Transactions
