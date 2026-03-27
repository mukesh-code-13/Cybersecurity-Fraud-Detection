import React from 'react'
import { Menu, LogOut, Settings, Bell } from 'lucide-react'
import { useAuthStore, useUIStore } from '../store'
import authService from '../services/auth'

const Header: React.FC = () => {
  const { user } = useAuthStore()
  const { toggleSidebar } = useUIStore()

  const handleLogout = () => {
    authService.logout()
    useAuthStore.setState({ isAuthenticated: false, user: null })
    window.location.href = '/login'
  }

  return (
    <header className="bg-white dark:bg-slate-800 shadow sticky top-0 z-40">
      <div className="flex items-center justify-between px-6 py-3">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition"
          >
            <Menu className="w-6 h-6 text-gray-700 dark:text-gray-300" />
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Fraud Detection Dashboard
          </h1>
        </div>

        <div className="flex items-center gap-6">
          <button className="relative p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition">
            <Bell className="w-6 h-6 text-gray-700 dark:text-gray-300" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          <button className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition">
            <Settings className="w-6 h-6 text-gray-700 dark:text-gray-300" />
          </button>

          <div className="flex items-center gap-3 pl-6 border-l border-gray-200 dark:border-slate-700">
            <div className="text-right">
              <p className="text-sm font-semibold text-gray-900 dark:text-white">
                {user?.username || 'User'}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {user?.role || 'Analyst'}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 hover:bg-red-100 dark:hover:bg-red-900 rounded-lg transition"
            >
              <LogOut className="w-5 h-5 text-red-600 dark:text-red-400" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
