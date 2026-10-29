import { useEffect, useRef, useState } from 'react'
import type { AgentKey } from '@/areas/student/components/StudentVisuals'
import { PrismMascot } from '@/areas/student/components/StudentVisuals'
import styles from './Mascot3D.module.css'

const CHARACTER_BY_AGENT: Record<AgentKey, string> = {
  catalyst: 'catalisador',
  mentor: 'mentor',
  analyst: 'analista',
}

const TONE_BY_AGENT: Record<AgentKey, 'catalyst' | 'mentor' | 'analyst'> = {
  catalyst: 'catalyst',
  mentor: 'mentor',
  analyst: 'analyst',
}

const LABEL_BY_AGENT: Record<AgentKey, string> = {
  catalyst: 'Mascote 3D do Catalisador',
  mentor: 'Mascote 3D do Mentor',
  analyst: 'Mascote 3D do Analista de Progresso',
}

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
).replace(/\/$/, '')
const MODEL_BASE_URL = `${API_BASE}/static/mascotes`

interface MascotViewerInstance {
  showCharacter: (
    characterId: string,
    options?: { reset?: boolean },
  ) => Promise<unknown>
  triggerAnimation: (animationId: string, priority?: number) => unknown
  destroy: () => void
}

export interface Mascot3DProps {
  agent: AgentKey
  /** ID da animação do catálogo, ex.: C-03, M-07, A-05. */
  animation?: string
  priority?: number
  size?: number
  className?: string
  /** Ativa o piso escuro do demo original (desligado no tema do app). */
  showFloor?: boolean
}

/**
 * Renderiza o mascote 3D real (GLB via Three.js) com fallback estático.
 *
 * Os GLBs são servidos pelo backend existente em `/static/mascotes`. Em
 * ambientes sem WebGL (ou durante o carregamento), o SVG do PrismMascot
 * mantém a identidade visual sem quebrar a página.
 */
export function Mascot3D({
  agent,
  animation,
  priority,
  size = 220,
  className = '',
  showFloor = false,
}: Mascot3DProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const viewerRef = useRef<MascotViewerInstance | null>(null)
  const [ready, setReady] = useState(false)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    // jsdom não implementa WebGL; os testes usam o fallback estático.
    if (import.meta.env.MODE === 'test') {
      setFailed(true)
      return
    }

    let cancelled = false
    const container = containerRef.current
    if (!container) return

    async function init() {
      try {
        const module = await import('./viewer/MascotViewer.js')
        const Viewer = module.MascotViewer as unknown as new (options: {
          container: HTMLElement
          modelBaseUrl: string
          reducedMotion: boolean | null
          fade: number
          pixelRatio: number
          showFloor: boolean
        }) => MascotViewerInstance

        const viewer = new Viewer({
          container: container!,
          modelBaseUrl: MODEL_BASE_URL,
          reducedMotion: null,
          fade: 0.25,
          pixelRatio: Math.min(window.devicePixelRatio || 1, 2),
          showFloor,
        })
        viewerRef.current = viewer
        await viewer.showCharacter(CHARACTER_BY_AGENT[agent], { reset: true })

        if (cancelled) {
          viewer.destroy()
          viewerRef.current = null
          return
        }
        setReady(true)
      } catch (error) {
        console.warn('Mascote 3D indisponível; usando fallback estático.', error)
        if (!cancelled) setFailed(true)
      }
    }

    void init()

    return () => {
      cancelled = true
      viewerRef.current?.destroy()
      viewerRef.current = null
    }
  }, [agent, showFloor])

  useEffect(() => {
    if (!ready || !animation || !viewerRef.current) return
    try {
      viewerRef.current.triggerAnimation(animation, priority)
    } catch (error) {
      console.warn(`Animação ${animation} não pôde ser executada.`, error)
    }
  }, [animation, priority, ready])

  return (
    <div
      className={[styles.stage, className].join(' ')}
      style={{
        width: size,
        maxWidth: '100%',
        aspectRatio: '1 / 1',
        flex: '0 0 auto',
      }}
      role="img"
      aria-label={LABEL_BY_AGENT[agent]}
    >
      <div ref={containerRef} className={styles.canvasHost} />
      {(!ready || failed) && (
        <div className={styles.fallback} aria-hidden="true">
          <PrismMascot size={size} tone={TONE_BY_AGENT[agent]} floating={false} />
        </div>
      )}
    </div>
  )
}
