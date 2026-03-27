# Fraud Detection Dashboard - React Frontend

Modern, responsive React dashboard for AI-driven cybersecurity fraud detection system with real-time analysis capabilities.

## 🎯 Features

### 📊 Dashboard
- Real-time system health monitoring
- Detection model status overview
- Quick statistics and alerts
- System information display

### 💳 Transaction Analysis
- Analyze transactions for fraud detection
- Real-time anomaly and fraud scoring
- Risk level assessment (Low, Medium, High, Critical)
- Detailed scoring breakdowns
- Visual progress indicators

### 📧 Phishing Detection
- Email content analysis for phishing
- Multi-factor risk assessment (Sender, Content, URL)
- Suspicious URL identification
- Phishing indicators display
- Email validation

### 👥 Behavior Analysis
- User behavior pattern detection
- Login anomaly detection
- Access pattern anomaly detection
- Severity assessment (Low, Medium, High)
- Detailed behavior metrics

### 📈 Analytics & Reports
- Comprehensive statistics dashboard
- Transaction volume tracking
- Fraud detection rates
- Risk distribution analysis
- Model performance metrics
- Exportable reports (CSV, PDF, Excel)

### 🔐 Authentication
- Secure login system
- Role-based access control
- Session management
- Demo account support

## 🛠️ Tech Stack

- **Framework**: React 18.2.0
- **Routing**: React Router v6
- **Styling**: Tailwind CSS 3.3.6
- **HTTP Client**: Axios 1.6.2
- **Charts**: Chart.js with react-chartjs-2
- **State Management**: Zustand 4.4.1
- **Build Tool**: Vite 5.0.8
- **Notifications**: React Hot Toast 2.4.1
- **Icons**: Lucide React 0.294.0
- **Language**: TypeScript 5.3.3

## 📦 Installation

### Prerequisites
- Node.js >= 16.x
- npm or yarn package manager

### Setup

1. **Clone and navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Setup environment variables**
```bash
cp .env.example .env.local
```

Update `.env.local` with your configuration:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Fraud Detection Dashboard
```

## 🚀 Development

### Start Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

### Build for Production
```bash
npm run build
# or
yarn build
```

Output will be in the `dist/` directory

### Preview Production Build
```bash
npm run preview
# or
yarn preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable React components
│   │   ├── common/         # Common UI components
│   │   ├── Header.tsx      # Top navigation header
│   │   ├── Sidebar.tsx     # Left sidebar navigation
│   │   └── ProtectedRoute.tsx
│   ├── pages/              # Page components
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Transactions.tsx
│   │   ├── Phishing.tsx
│   │   ├── Behavior.tsx
│   │   └── Analytics.tsx
│   ├── services/           # API and auth services
│   │   ├── api.ts         # API client
│   │   └── auth.ts        # Authentication service
│   ├── store/              # State management (Zustand)
│   │   └── index.ts
│   ├── types/              # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/              # Utility functions
│   │   └── helpers.ts
│   ├── App.tsx             # Main app component with routing
│   ├── main.tsx            # React entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json            # Project dependencies
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
└── README.md              # This file
```

## 🔌 API Integration

The frontend communicates with the FastAPI backend at the URL specified in `VITE_API_URL`.

### API Endpoints Used

```
GET    /api/v1/health
GET    /api/v1/models/status
GET    /api/v1/alerts/risk-summary
POST   /api/v1/transactions/analyze
POST   /api/v1/phishing/detect
POST   /api/v1/behavior/analyze
POST   /api/v1/models/update-baseline
```

## 🎨 Styling

### Tailwind CSS
The project uses Tailwind CSS for utility-first styling. Custom components and utilities are defined in `src/index.css`.

### Color Scheme
- **Primary**: Blue (#3b82f6)
- **Secondary**: Indigo (#6366f1)
- **Danger**: Red (#ef4444)
- **Warning**: Amber (#f59e0b)
- **Success**: Emerald (#10b981)

### Component Classes

Common reusable component classes:
- `.card` - Card container
- `.btn-primary`, `.btn-secondary`, `.btn-danger`, `.btn-success` - Button variants
- `.input-field` - Form input styling
- `.label` - Form label styling
- `.badge-*` - Badge variants
- `.section-title`, `.subsection-title` - Typography

## 🔐 Authentication

### Login
- Default demo credentials:
  - Username: `demo_analyst`
  - Password: `demo123`

### Token Management
- Authentication tokens are stored in `localStorage`
- Tokens are automatically included in API requests via interceptors
- Expired tokens trigger automatic logout

## 📊 State Management

Using Zustand for lightweight state management:

```typescript
// Auth Store
useAuthStore() // { user, isAuthenticated, setUser, setAuthenticated }

// UI Store
useUIStore() // { sidebarOpen, toggleSidebar }
```

## 🛡️ Error Handling

- Request interceptors for token management
- Response interceptors for error handling
- Toast notifications for user feedback
- Comprehensive error messages from API

## 📱 Responsive Design

- Mobile-first approach using Tailwind CSS
- Responsive grid layouts
- Collapsible sidebar on mobile
- Touch-friendly components
- Tested on all screen sizes

## ♿ Accessibility

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Color contrast compliance
- Focus management

## 🚢 Deployment

### Vercel
```bash
npm install -g vercel
vercel
```

### Docker
```dockerfile
# Dockerfile for frontend
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### Environment-Specific Configuration

**Development**
```env
VITE_API_URL=http://localhost:8000
```

**Production**
```env
VITE_API_URL=https://api.production.com
```

## 🧪 Testing

### Run Tests
```bash
npm run test
```

### Testing Tools
- Jest for unit testing
- React Testing Library for component testing
- Cypress for E2E testing (optional)

## 📚 Documentation

### Component Usage

```typescript
// Button Component
<Button variant="primary" size="md" onClick={handleClick}>
  Click Me
</Button>

// Card Component
<Card clickable onClick={() => console.log('Clicked')}>
  <h3>Card Title</h3>
  <p>Card content</p>
</Card>

// StatCard Component
<StatCard 
  label="Total Users" 
  value="1,234"
  icon={<Users />}
  color="blue"
/>
```

## 🐛 Troubleshooting

### API Connection Issues
- Verify `VITE_API_URL` is correct
- Ensure backend is running on correct port
- Check CORS settings on backend

### Build Issues
- Clear `node_modules/` and `package-lock.json`
- Run `npm install` again
- Check Node.js version compatibility

### Performance Issues
- Check for unnecessary re-renders
- Use React DevTools Profiler
- Implement code splitting with React.lazy()

## 📝 Performance Optimization

- Lazy loading of route components
- Image optimization with proper formats
- Minified CSS and JavaScript
- Efficient state management
- Optimized API calls

## 🔄 Continuous Integration

Setup GitHub Actions for:
- Automated testing
- Code linting
- Build verification
- Deployment to staging/production

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Create feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open Pull Request

## 📞 Support

For issues and questions:
- Check existing GitHub issues
- Create new issue with detailed description
- Contact development team

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/)

---

**Last Updated**: January 2024
**Version**: 1.0.0
