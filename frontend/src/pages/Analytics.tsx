import React from 'react'
import { BarChart3, LineChart, PieChart } from 'lucide-react'
import { Card, StatCard } from '../components/common/Card'

const Analytics: React.FC = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="section-title">Analytics & Reports</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Comprehensive analytics and insights on fraud detection
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          label="Total Transactions"
          value="2,456"
          icon={<BarChart3 className="w-6 h-6" />}
          color="blue"
        />
        <StatCard
          label="Fraud Detected"
          value="47"
          icon={<LineChart className="w-6 h-6" />}
          color="red"
        />
        <StatCard
          label="Phishing Emails"
          value="132"
          icon={<PieChart className="w-6 h-6" />}
          color="yellow"
        />
        <StatCard
          label="Accuracy Rate"
          value="98.2%"
          icon={<BarChart3 className="w-6 h-6" />}
          color="green"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Transaction Volume */}
        <Card>
          <h2 className="subsection-title">Transaction Volume (Last 30 Days)</h2>
          <div className="aspect-video bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-900/10 rounded-lg flex items-center justify-center">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization</p>
          </div>
        </Card>

        {/* Fraud Detection Rate */}
        <Card>
          <h2 className="subsection-title">Fraud Detection Rate</h2>
          <div className="aspect-video bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-900/10 rounded-lg flex items-center justify-center">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization</p>
          </div>
        </Card>

        {/* Risk Distribution */}
        <Card>
          <h2 className="subsection-title">Risk Level Distribution</h2>
          <div className="aspect-video bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-900/10 rounded-lg flex items-center justify-center">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization</p>
          </div>
        </Card>

        {/* Model Performance */}
        <Card>
          <h2 className="subsection-title">Model Performance Metrics</h2>
          <div className="aspect-video bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-900/10 rounded-lg flex items-center justify-center">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization</p>
          </div>
        </Card>
      </div>

      {/* Detailed Reports */}
      <Card>
        <h2 className="subsection-title">Recent Detection Alerts</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-slate-700">
                <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">
                  Date
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">
                  Type
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">
                  User
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">
                  Risk Level
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  date: '2024-01-15 10:30',
                  type: 'Fraud',
                  user: 'user_001',
                  risk: 'Critical',
                },
                {
                  date: '2024-01-15 09:15',
                  type: 'Phishing',
                  user: 'user_045',
                  risk: 'High',
                },
                {
                  date: '2024-01-15 08:45',
                  type: 'Anomaly',
                  user: 'user_123',
                  risk: 'Medium',
                },
                {
                  date: '2024-01-15 07:30',
                  type: 'Behavioral',
                  user: 'user_089',
                  risk: 'Low',
                },
              ].map((alert, idx) => (
                <tr
                  key={idx}
                  className="border-b border-gray-100 dark:border-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700/50"
                >
                  <td className="py-3 px-4 text-gray-900 dark:text-white">{alert.date}</td>
                  <td className="py-3 px-4 text-gray-900 dark:text-white">{alert.type}</td>
                  <td className="py-3 px-4 text-gray-900 dark:text-white">{alert.user}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                        alert.risk === 'Critical'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          : alert.risk === 'High'
                            ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
                            : alert.risk === 'Medium'
                              ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                              : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      }`}
                    >
                      {alert.risk}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <button className="text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium">
                      Review
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Export Section */}
      <Card>
        <h2 className="subsection-title">Export Reports</h2>
        <div className="flex gap-3">
          <button className="btn btn-secondary btn-sm">
            📊 Export as CSV
          </button>
          <button className="btn btn-secondary btn-sm">
            📄 Export as PDF
          </button>
          <button className="btn btn-secondary btn-sm">
            📈 Export as Excel
          </button>
        </div>
      </Card>
    </div>
  )
}

export default Analytics
