import React from 'react'
import ReactDOM from 'react-dom/client'
import { App } from './App'
import '@/design-system/tokens.css'
import '@/design-system/brand/brand.css'
import '@/areas/student/student-theme.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
