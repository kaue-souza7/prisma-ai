import { useCallback, useEffect, useRef, useState } from 'react'

type EffectKind = 'tap' | 'correct' | 'incorrect' | 'complete'

const STORAGE_KEY = 'ell-learning-effects'

export function useLearningEffects() {
  const [enabled, setEnabled] = useState(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) === '1'
    } catch {
      return false
    }
  })
  const audioRef = useRef<AudioContext | null>(null)

  useEffect(() => {
    return () => {
      audioRef.current?.close().catch(() => undefined)
      audioRef.current = null
    }
  }, [])

  const play = useCallback(
    (kind: EffectKind) => {
      if (!enabled) return

      if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
        const pattern = kind === 'incorrect' ? 18 : kind === 'complete' ? [18, 40, 18] : 12
        navigator.vibrate(pattern)
      }

      const AudioContextClass =
        window.AudioContext ??
        (window as typeof window & { webkitAudioContext?: typeof AudioContext })
          .webkitAudioContext
      if (!AudioContextClass) return

      if (!audioRef.current) {
        audioRef.current = new AudioContextClass()
      }
      const context = audioRef.current
      if (context.state === 'suspended') {
        context.resume().catch(() => undefined)
      }

      const notes =
        kind === 'correct'
          ? [523.25, 659.25]
          : kind === 'complete'
            ? [523.25, 659.25, 783.99]
            : kind === 'incorrect'
              ? [220, 196]
              : [440]

      notes.forEach((frequency, index) => {
        const oscillator = context.createOscillator()
        const gain = context.createGain()
        const start = context.currentTime + index * 0.085
        const duration = kind === 'complete' ? 0.2 : 0.13
        oscillator.type = kind === 'incorrect' ? 'sine' : 'triangle'
        oscillator.frequency.value = frequency
        gain.gain.setValueAtTime(0.0001, start)
        gain.gain.exponentialRampToValueAtTime(0.055, start + 0.015)
        gain.gain.exponentialRampToValueAtTime(0.0001, start + duration)
        oscillator.connect(gain)
        gain.connect(context.destination)
        oscillator.start(start)
        oscillator.stop(start + duration + 0.02)
      })
    },
    [enabled],
  )

  const toggle = useCallback(() => {
    setEnabled((current) => {
      const next = !current
      try {
        localStorage.setItem(STORAGE_KEY, next ? '1' : '0')
      } catch {
        // Preferência em memória quando o armazenamento local não está disponível.
      }
      return next
    })
  }, [])

  return { enabled, toggle, play }
}
