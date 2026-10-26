import { useId } from 'react'
import './brand.css'

interface PrismArtProps {
  className?: string
  variant?: 'hero' | 'cta'
}

export function PrismArt({ className = '', variant = 'hero' }: PrismArtProps) {
  const uid = useId().replace(/:/g, '')
  const fill = `${uid}-fill`
  const line = `${uid}-line`
  const glow = `${uid}-glow`

  return (
    <svg
      className={`pl-prism-art ${className}`}
      viewBox="0 0 600 620"
      fill="none"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id={fill} x1="150" y1="70" x2="470" y2="560">
          <stop stopColor="#B8A5FF" stopOpacity=".42" />
          <stop offset=".35" stopColor="#6C3BFF" stopOpacity=".2" />
          <stop offset=".7" stopColor="#2775FF" stopOpacity=".17" />
          <stop offset="1" stopColor="#FF6B6B" stopOpacity=".08" />
        </linearGradient>
        <linearGradient id={line} x1="100" y1="80" x2="500" y2="560">
          <stop stopColor="#D8CFFF" stopOpacity=".8" />
          <stop offset=".45" stopColor="#6C3BFF" stopOpacity=".55" />
          <stop offset="1" stopColor="#2775FF" stopOpacity=".15" />
        </linearGradient>
        <radialGradient id={glow}>
          <stop stopColor="#6C3BFF" stopOpacity=".36" />
          <stop offset=".6" stopColor="#2775FF" stopOpacity=".08" />
          <stop offset="1" stopColor="#17152B" stopOpacity="0" />
        </radialGradient>
      </defs>

      <ellipse cx="306" cy="320" rx="265" ry="250" fill={`url(#${glow})`} />
      {variant === 'hero' && (
        <g opacity=".45" stroke={`url(#${line})`}>
          <ellipse cx="305" cy="330" rx="252" ry="116" transform="rotate(-26 305 330)" />
          <ellipse cx="305" cy="330" rx="205" ry="82" transform="rotate(32 305 330)" />
          <circle cx="82" cy="392" r="3.5" fill="#FF6B6B" stroke="none" />
          <circle cx="516" cy="234" r="3" fill="#56CCF2" stroke="none" />
          <circle cx="433" cy="487" r="2.5" fill="#FCA048" stroke="none" />
        </g>
      )}

      <g style={{ transformOrigin: '300px 320px' }} className="pl-prism-shape">
        <path
          d="M300 42 536 540H64L300 42Z"
          fill={`url(#${fill})`}
          stroke={`url(#${line})`}
          strokeWidth="1.2"
        />
        <path d="M300 42v498" stroke="rgba(255,255,255,.24)" strokeWidth="1" />
        <path d="M300 42 64 540" stroke="rgba(255,255,255,.13)" />
        <path d="M300 42 536 540" stroke="rgba(255,255,255,.13)" />
        <path d="m182 291 118-249 118 249-118 249-118-249Z" fill="rgba(255,255,255,.025)" stroke="rgba(255,255,255,.15)" />
        <path d="m201 321 99-40 99 40-99 40-99-40Z" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.2)" />
      </g>
    </svg>
  )
}
