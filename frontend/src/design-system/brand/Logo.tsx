import { Link } from 'react-router-dom'
import './brand.css'

interface LogoProps {
  compact?: boolean
  className?: string
}

function PrismMark() {
  return (
    <svg
      className="pl-logo-mark"
      viewBox="0 0 34 38"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M17 2 32 31H2L17 2Z"
        fill="url(#pl-logo-fill)"
        stroke="rgba(255,255,255,.44)"
        strokeWidth="1"
      />
      <path d="M17 2v29" stroke="rgba(255,255,255,.36)" />
      <path d="M9.5 31 17 14l7.5 17" stroke="rgba(255,255,255,.22)" />
      <defs>
        <linearGradient id="pl-logo-fill" x1="5" y1="5" x2="29" y2="32">
          <stop stopColor="#B9A7FF" />
          <stop offset=".45" stopColor="#6C3BFF" />
          <stop offset=".78" stopColor="#2775FF" />
          <stop offset="1" stopColor="#FF6B6B" />
        </linearGradient>
      </defs>
    </svg>
  )
}

export function Logo({ compact = false, className = '' }: LogoProps) {
  return (
    <Link to="/" className={`pl-logo ${className}`} aria-label="Prisma.AI — início">
      <PrismMark />
      {!compact && (
        <span className="pl-logo-type">
          Prisma<span className="pl-logo-dot">.</span>AI
        </span>
      )}
    </Link>
  )
}
