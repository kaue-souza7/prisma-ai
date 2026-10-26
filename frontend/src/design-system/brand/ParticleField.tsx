import { useEffect, useRef } from 'react'
import { useReducedMotion } from 'framer-motion'

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  alpha: number
  color: string
}

const COLORS = ['#6C3BFF', '#2775FF', '#FF6B6B', '#FCA048']

export function ParticleField({ count = 55 }: { count?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const reduced = useReducedMotion()

  useEffect(() => {
    if (reduced) return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    let raf = 0
    let particles: Particle[] = []
    let visible = true

    const resize = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
    }
    resize()

    const spawn = () => {
      particles = Array.from({ length: count }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        radius: Math.random() * 2.2 + 0.6,
        alpha: Math.random() * 0.5 + 0.2,
        color: COLORS[Math.floor(Math.random() * COLORS.length)],
      }))
    }
    spawn()

    const draw = () => {
      if (!visible) {
        raf = 0
        return
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      for (const p of particles) {
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0) p.x = canvas.width
        if (p.x > canvas.width) p.x = 0
        if (p.y < 0) p.y = canvas.height
        if (p.y > canvas.height) p.y = 0
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
        ctx.fillStyle = p.color
        ctx.globalAlpha = p.alpha
        ctx.fill()
        ctx.globalAlpha = 1
      }
      // Linhas de conexão entre partículas próximas
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < 90) {
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
            ctx.strokeStyle = '#6C3BFF'
            ctx.globalAlpha = (1 - dist / 90) * 0.12
            ctx.lineWidth = 0.8
            ctx.stroke()
            ctx.globalAlpha = 1
          }
        }
      }
      raf = requestAnimationFrame(draw)
    }
    const observer = 'IntersectionObserver' in window
      ? new IntersectionObserver(([entry]) => {
          visible = entry.isIntersecting
          if (visible && raf === 0) draw()
        })
      : null
    observer?.observe(canvas)
    draw()

    window.addEventListener('resize', resize)
    return () => {
      observer?.disconnect()
      if (raf) cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
    }
  }, [count, reduced])

  return (
    <canvas
      ref={canvasRef}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
      aria-hidden="true"
    />
  )
}
