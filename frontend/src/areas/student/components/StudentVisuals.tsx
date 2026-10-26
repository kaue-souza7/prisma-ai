import { useId } from 'react'
import type { ReactNode } from 'react'
import {
  CardIcon,
  ChartIcon,
  ChatIcon,
  GrowthIcon,
  OrbitIcon,
  PercentIcon,
  PiggyIcon,
  ShieldIcon,
  WalletIcon,
} from '@/design-system/Icons'
import styles from './StudentVisuals.module.css'

export type AgentKey = 'catalyst' | 'mentor' | 'analyst'
export type MascotTone = 'violet' | 'mentor' | 'analyst' | 'catalyst'

export const AGENT_META: Record<
  AgentKey,
  { name: string; role: string; icon: typeof OrbitIcon }
> = {
  catalyst: {
    name: 'Catalisador',
    role: 'Recomenda o próximo passo',
    icon: OrbitIcon,
  },
  mentor: {
    name: 'Mentor',
    role: 'Explica conceitos com você',
    icon: ChatIcon,
  },
  analyst: {
    name: 'Analista de Progresso',
    role: 'Mostra evidências e revisões',
    icon: ChartIcon,
  },
}

const TONES: Record<MascotTone, { from: string; mid: string; to: string; soft: string }> = {
  violet: { from: '#C5B5FF', mid: '#7C4DFF', to: '#2775FF', soft: 'rgba(108, 59, 255, .16)' },
  mentor: { from: '#A9D8FF', mid: '#2F80ED', to: '#56CCF2', soft: 'rgba(47, 128, 237, .16)' },
  analyst: { from: '#A9F5D0', mid: '#11998E', to: '#38EF7D', soft: 'rgba(17, 153, 142, .16)' },
  catalyst: { from: '#FFC6B0', mid: '#FF6B6B', to: '#FCA048', soft: 'rgba(255, 107, 107, .16)' },
}

export function PrismMascot({
  tone = 'violet',
  size = 230,
  className = '',
  floating = true,
}: {
  tone?: MascotTone
  size?: number
  className?: string
  floating?: boolean
}) {
  const uid = useId().replace(/:/g, '')
  const body = `${uid}-body`
  const glow = `${uid}-glow`
  const palette = TONES[tone]

  return (
    <svg
      className={[styles.mascot, floating ? styles.mascotFloat : '', className].join(' ')}
      width={size}
      height={size}
      viewBox="0 0 240 240"
      fill="none"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id={body} x1="54" y1="36" x2="194" y2="208" gradientUnits="userSpaceOnUse">
          <stop stopColor={palette.from} />
          <stop offset=".5" stopColor={palette.mid} />
          <stop offset="1" stopColor={palette.to} />
        </linearGradient>
        <radialGradient id={glow}>
          <stop stopColor={palette.mid} stopOpacity=".3" />
          <stop offset="1" stopColor={palette.mid} stopOpacity="0" />
        </radialGradient>
      </defs>

      <ellipse cx="120" cy="124" rx="112" ry="108" fill={`url(#${glow})`} />
      <ellipse cx="120" cy="216" rx="67" ry="12" fill="rgba(31, 22, 71, .12)" />

      <g className={styles.mascotOrbit} opacity=".9">
        <ellipse cx="120" cy="120" rx="103" ry="39" transform="rotate(-24 120 120)" stroke={palette.mid} strokeOpacity=".24" />
        <ellipse cx="120" cy="120" rx="88" ry="30" transform="rotate(31 120 120)" stroke={palette.to} strokeOpacity=".18" />
        <circle cx="34" cy="143" r="4" fill={palette.to} />
        <circle cx="209" cy="92" r="3" fill={palette.from} />
        <circle cx="184" cy="180" r="3.5" fill={palette.mid} />
      </g>

      <g className={styles.mascotBody}>
        <path
          d="M120 28c13 0 24 8 31 21l52 100c14 27-4 58-33 58H70c-29 0-47-31-33-58l52-100c7-13 18-21 31-21Z"
          fill={`url(#${body})`}
          stroke="rgba(255,255,255,.6)"
          strokeWidth="1.4"
        />
        <path d="M120 30v176" stroke="rgba(255,255,255,.2)" />
        <path d="m120 30-67 129c-8 16 2 35 21 35h46" fill="rgba(255,255,255,.07)" />
        <path d="m54 169 33-16 33 16-33 17-33-17Z" fill="rgba(255,255,255,.13)" stroke="rgba(255,255,255,.22)" />
        <path d="M82 154v38M115 169v39" stroke="rgba(255,255,255,.18)" />

        <ellipse cx="97" cy="133" rx="5.2" ry="6.4" fill="#fff" />
        <ellipse cx="145" cy="133" rx="5.2" ry="6.4" fill="#fff" />
        <circle cx="98" cy="134.5" r="2.2" fill="#24174F" />
        <circle cx="146" cy="134.5" r="2.2" fill="#24174F" />
        <path d="M108 153c7 7 17 7 24 0" stroke="#fff" strokeWidth="3.4" strokeLinecap="round" />
        <path d="M87 149c3 2 7 2 10 0M143 149c3 2 7 2 10 0" stroke="rgba(255,255,255,.35)" strokeWidth="2" strokeLinecap="round" />

        <path d="m68 84 8 8M76 84l-8 8" stroke="rgba(255,255,255,.55)" strokeWidth="2.4" strokeLinecap="round" />
        <path d="m174 64 6 6M180 64l-6 6" stroke="rgba(255,255,255,.45)" strokeWidth="2" strokeLinecap="round" />
      </g>
    </svg>
  )
}

export function AgentAvatar({
  agent,
  size = 42,
  className = '',
}: {
  agent: AgentKey
  size?: number
  className?: string
}) {
  const Icon = AGENT_META[agent].icon
  return (
    <span
      className={[styles.agentAvatar, styles[`agent_${agent}`], className].join(' ')}
      style={{ width: size, height: size }}
      aria-hidden="true"
    >
      <span className={styles.agentAvatarInner}>
        <Icon size={Math.round(size * 0.42)} />
      </span>
    </span>
  )
}

const PHASE_ICONS = [WalletIcon, CardIcon, PiggyIcon, PercentIcon, GrowthIcon, ShieldIcon]
const PHASE_LABELS = [
  'Primeiro salário',
  'Dinheiro digital',
  'Poupar',
  'Juros',
  'Investimentos',
  'Proteção',
]

export function PhaseArt({ number, size = 74 }: { number: number; size?: number }) {
  const Icon = PHASE_ICONS[(number - 1) % PHASE_ICONS.length]
  return (
    <span
      className={[styles.phaseArt, styles[`phaseArt_${((number - 1) % 6) + 1}`]].join(' ')}
      style={{ width: size, height: size }}
      aria-label={PHASE_LABELS[(number - 1) % PHASE_LABELS.length]}
      role="img"
    >
      <span className={styles.phaseArtGlow} aria-hidden="true" />
      <Icon size={Math.round(size * 0.36)} />
      <small>{String(number).padStart(2, '0')}</small>
    </span>
  )
}

export function ProgressRing({
  value,
  size = 126,
  stroke = 11,
  label,
  sublabel,
  children,
}: {
  value: number
  size?: number
  stroke?: number
  label?: string
  sublabel?: string
  children?: ReactNode
}) {
  const uid = useId().replace(/:/g, '')
  const gradient = `${uid}-ring`
  const radius = (size - stroke) / 2
  const circumference = 2 * Math.PI * radius
  const normalized = Math.max(0, Math.min(100, value))
  const offset = circumference - (normalized / 100) * circumference

  return (
    <div
      className={styles.progressRing}
      style={{ width: size, height: size }}
      role="img"
      aria-label={label ?? `${Math.round(normalized)}%`}
    >
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <defs>
          <linearGradient id={gradient} x1="0" y1="0" x2={size} y2={size}>
            <stop stopColor="#B6A4FF" />
            <stop offset=".42" stopColor="#6C3BFF" />
            <stop offset="1" stopColor="#2775FF" />
          </linearGradient>
        </defs>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(108, 59, 255, .11)"
          strokeWidth={stroke}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#${gradient})`}
          strokeWidth={stroke}
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          className={styles.progressRingValue}
        />
      </svg>
      <span className={styles.progressRingCenter}>
        {children ?? (
          <>
            <strong>{Math.round(normalized)}%</strong>
            {sublabel && <small>{sublabel}</small>}
          </>
        )}
      </span>
    </div>
  )
}

export function BrandMark({
  compact = false,
  light = false,
  className = '',
}: {
  compact?: boolean
  light?: boolean
  className?: string
}) {
  return (
    <span className={[styles.brand, light ? styles.brandLight : '', className].join(' ')}>
      <svg viewBox="0 0 34 38" className={styles.brandMark} aria-hidden="true">
        <defs>
          <linearGradient id="st-brand-fill" x1="5" y1="5" x2="29" y2="32">
            <stop stopColor="#D8CFFF" />
            <stop offset=".45" stopColor="#8B5CFF" />
            <stop offset=".78" stopColor="#56CCF2" />
            <stop offset="1" stopColor="#FFB38A" />
          </linearGradient>
        </defs>
        <path d="M17 2 32 31H2L17 2Z" fill="url(#st-brand-fill)" stroke="rgba(255,255,255,.4)" />
        <path d="M17 2v29" stroke="rgba(255,255,255,.32)" />
        <path d="M9.5 31 17 14l7.5 17" stroke="rgba(255,255,255,.22)" />
      </svg>
      {!compact && (
        <span className={styles.brandType}>
          Prisma<span>.</span>AI
        </span>
      )}
    </span>
  )
}
