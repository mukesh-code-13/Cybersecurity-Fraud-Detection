import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  CreditCard,
  Mail,
  Activity,
  BarChart3,
  Shield,
  ChevronRight,
} from 'lucide-react'
import { useUIStore } from '../store'

interface NavItem {
  label: string
  path: string
  icon: React.ReactNode
}

const navItems: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: <LayoutDashboard className="w-5 h-5" /> },
  { label: 'Transactions', path: '/transactions', icon: <CreditCard className="w-5 h-5" /> },
  { label: 'Phishing Detection', path: '/phishing', icon: <Mail className="w-5 h-5" /> },
  { label: 'Behavior Analysis', path: '/behavior', icon: <Activity className="w-5 h-5" /> },
  { label: 'Analytics', path: '/analytics', icon: <BarChart3 className="w-5 h-5" /> },
]

const Sidebar: React.FC = () => {
  const { sidebarOpen } = useUIStore()
  const location = useLocation()

  return (
    <aside
      className={`${
        sidebarOpen ? 'w-64' : 'w-20'
      } bg-white dark:bg-slate-800 shadow transition-all duration-300 h-screen sticky top-0 overflow-y-auto`}
    >
      <div className="p-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          {sidebarOpen && (
            <div>
              <h1 className="text-lg font-bold text-gray-900 dark:text-white">SecureAI</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">Fraud Detection</p>
            </div>
          )}
        </div>

        <nav className="space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                location.pathname === item.path
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700'
              }`}
              title={!sidebarOpen ? item.label : ''}
            >
              {item.icon}
              {sidebarOpen && (
                <>
                  <span className="flex-1">{item.label}</span>
                  {location.pathname === item.path && (
                    <ChevronRight className="w-4 h-4" />
                  )}
                </>
              )}
            </Link>
          ))}
        </nav>
      </div>

      {/* Footer */}
      <div
        className={`absolute bottom-0 left-0 right-0 p-6 border-t border-gray-200 dark:border-slate-700 ${
          !sidebarOpen && 'hidden'
        }`}
      >
        <p className="text-xs text-gray-500 dark:text-gray-400">
          © 2024 Fraud Detection System
        </p>
      </div>
    </aside>
  )
}

export default Sidebar
