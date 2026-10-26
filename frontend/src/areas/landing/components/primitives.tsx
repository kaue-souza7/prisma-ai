import type { CSSProperties, ReactNode, PointerEvent } from 'react'
import { useRef } from 'react'
import {
  motion,
  useMotionValue,
  useReducedMotion,
  useSpring,
} from 'framer-motion'

interface RevealProps {
  children: ReactNode
  className?: string
  delay?: number
  y?: number
  once?: boolean
}

export function Reveal({
  children,
  className = '',
  delay = 0,
  y = 28,
  once = true,
}: RevealProps) {
  const reduced = useReducedMotion()

  return (
    <motion.div
      className={className}
      initial={reduced ? false : { opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once, amount: 0.18 }}
      transition={{ duration: 0.72, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  )
}

interface SpotlightCardProps {
  children: ReactNode
  className?: string
  style?: CSSProperties
}

export function SpotlightCard({ children, className = '', style }: SpotlightCardProps) {
  const ref = useRef<HTMLDivElement>(null)

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    const element = ref.current
    if (!element) return
    const bounds = element.getBoundingClientRect()
    element.style.setProperty('--spot-x', `${event.clientX - bounds.left}px`)
    element.style.setProperty('--spot-y', `${event.clientY - bounds.top}px`)
    element.style.setProperty('--spot-opacity', '1')
  }

  function handlePointerLeave() {
    ref.current?.style.setProperty('--spot-opacity', '0')
  }

  return (
    <div
      ref={ref}
      className={`pl-spotlight-card ${className}`}
      style={style}
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
    >
      {children}
    </div>
  )
}

interface TiltProps {
  children: ReactNode
  className?: string
  max?: number
}

export function Tilt({ children, className = '', max = 7 }: TiltProps) {
  const ref = useRef<HTMLDivElement>(null)
  const reduced = useReducedMotion()
  const rotateX = useMotionValue(0)
  const rotateY = useMotionValue(0)
  const springX = useSpring(rotateX, { stiffness: 140, damping: 22 })
  const springY = useSpring(rotateY, { stiffness: 140, damping: 22 })

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    if (reduced) return
    const element = ref.current
    if (!element) return
    const bounds = element.getBoundingClientRect()
    const x = (event.clientX - bounds.left) / bounds.width - 0.5
    const y = (event.clientY - bounds.top) / bounds.height - 0.5
    rotateY.set(x * max * 2)
    rotateX.set(y * max * -2)
  }

  function handlePointerLeave() {
    rotateX.set(0)
    rotateY.set(0)
  }

  return (
    <motion.div
      ref={ref}
      className={`pl-tilt ${className}`}
      style={{
        rotateX: springX,
        rotateY: springY,
        transformPerspective: 1400,
        transformStyle: 'preserve-3d',
      }}
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
    >
      {children}
    </motion.div>
  )
}

interface MagneticProps {
  children: ReactNode
  className?: string
  strength?: number
}

export function Magnetic({ children, className = '', strength = 10 }: MagneticProps) {
  const reduced = useReducedMotion()
  const x = useMotionValue(0)
  const y = useMotionValue(0)
  const springX = useSpring(x, { stiffness: 220, damping: 18 })
  const springY = useSpring(y, { stiffness: 220, damping: 18 })

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    if (reduced) return
    const element = event.currentTarget
    const bounds = element.getBoundingClientRect()
    x.set(((event.clientX - bounds.left) / bounds.width - 0.5) * strength * 2)
    y.set(((event.clientY - bounds.top) / bounds.height - 0.5) * strength * 2)
  }

  function handlePointerLeave() {
    x.set(0)
    y.set(0)
  }

  return (
    <motion.div
      className={`pl-magnetic ${className}`}
      style={{ x: springX, y: springY }}
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
    >
      {children}
    </motion.div>
  )
}

interface SectionHeadingProps {
  eyebrow: string
  title: ReactNode
  description?: ReactNode
  align?: 'left' | 'center'
  className?: string
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = 'left',
  className = '',
}: SectionHeadingProps) {
  return (
    <div className={`pl-section-heading pl-section-heading--${align} ${className}`}>
      <Reveal>
        <p className="pl-eyebrow">
          <span className="pl-eyebrow-dot" aria-hidden="true" />
          {eyebrow}
        </p>
      </Reveal>
      <Reveal delay={0.08}>
        <h2 className="pl-section-title">{title}</h2>
      </Reveal>
      {description && (
        <Reveal delay={0.14}>
          <p className="pl-section-copy">{description}</p>
        </Reveal>
      )}
    </div>
  )
}
