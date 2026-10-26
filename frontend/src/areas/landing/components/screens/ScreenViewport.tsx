import { useLayoutEffect, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import './preview-screens.css'

export const SCREEN_WIDTH = 1200
export const SCREEN_HEIGHT = 840

/**
 * Moldura de uma "captura" da aplicação: o conteúdo é desenhado no tamanho
 * real do desktop (1200 × 840) e reduzido por transform para caber no card.
 */
export function ScreenViewport({
  label,
  children,
  width = SCREEN_WIDTH,
  height = SCREEN_HEIGHT,
}: {
  label: string
  children: ReactNode
  width?: number
  height?: number
}) {
  const viewportRef = useRef<HTMLDivElement>(null)
  const [scale, setScale] = useState(0)

  useLayoutEffect(() => {
    const viewport = viewportRef.current
    if (!viewport) return

    const updateScale = () => {
      setScale(viewport.clientWidth / width)
    }

    updateScale()

    if (typeof ResizeObserver === 'undefined') return

    const observer = new ResizeObserver(updateScale)
    observer.observe(viewport)
    return () => observer.disconnect()
  }, [width])

  return (
    <div
      ref={viewportRef}
      className="pl-screen"
      role="img"
      aria-label={label}
      style={{ aspectRatio: `${width} / ${height}` }}
    >
      <div
        className="pl-screen-canvas"
        style={{ width, height, transform: `scale(${scale})` }}
        aria-hidden="true"
      >
        {children}
      </div>
    </div>
  )
}
