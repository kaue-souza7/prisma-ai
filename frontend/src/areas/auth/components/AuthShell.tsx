import { useEffect, useRef } from 'react'
import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { MotionConfig, motion, useReducedMotion } from 'framer-motion'
import { ArrowUpRightIcon, LockIcon } from '@/design-system/Icons'
import { Logo } from '@/design-system/brand/Logo'
import { ParticleField } from '@/design-system/brand/ParticleField'
import styles from './AuthShell.module.css'

export type AuthMode = 'login' | 'register' | 'support'

interface AuthShellProps {
  mode: AuthMode
  documentTitle: string
  eyebrow: string
  heading: ReactNode
  description: ReactNode
  visual: ReactNode
  footer?: ReactNode
  children: ReactNode
}

export function GradientWord({ children }: { children: ReactNode }) {
  return <span className={styles.gradientWord}>{children}</span>
}

export function AuthShell({
  mode,
  documentTitle,
  eyebrow,
  heading,
  description,
  visual,
  footer,
  children,
}: AuthShellProps) {
  const reduced = useReducedMotion()
  const initialTitle = useRef('')
  const headingRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    const html = document.documentElement
    html.classList.add('prisma-auth-html')
    initialTitle.current = document.title

    return () => {
      html.classList.remove('prisma-auth-html')
      document.title = initialTitle.current
    }
  }, [])

  useEffect(() => {
    document.title = documentTitle
    const frame = window.requestAnimationFrame(() => {
      headingRef.current?.focus({ preventScroll: true })
    })

    return () => window.cancelAnimationFrame(frame)
  }, [documentTitle])

  const year = new Date().getFullYear()

  return (
    <MotionConfig reducedMotion="user">
      <div className={`prisma-brand ${styles.shell} ${styles[`shell--${mode}`]}`}>
        <a href="#auth-content" className={styles.skipLink}>
          Pular para o formulário
        </a>

        <div className={styles.ambient} aria-hidden="true">
          <div className={styles.grid} />
          <div className={`${styles.aurora} ${styles.auroraOne}`} />
          <div className={`${styles.aurora} ${styles.auroraTwo}`} />
          <div className={`${styles.aurora} ${styles.auroraThree}`} />
          <div className={styles.noise} />
          <div className={styles.particles}>
            <ParticleField count={26} />
          </div>
        </div>

        <header className={styles.topbar}>
          <Logo />

          <div className={styles.topMeta}>
            <span className={styles.secureBadge}>
              <LockIcon size={12} />
              Ambiente protegido
            </span>
            <Link to="/" className={styles.backLink} aria-label="Voltar para o site do Prisma.AI">
              <span>Voltar ao site</span>
              <ArrowUpRightIcon size={14} />
            </Link>
          </div>
        </header>

        <main id="auth-content" className={styles.main}>
          <div className={styles.layout}>
            <motion.section
              className={styles.formColumn}
              initial={reduced ? false : { opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.72, ease: [0.22, 1, 0.36, 1] }}
            >
              <div className={styles.formHalo} aria-hidden="true" />

              <div className={styles.card}>
                <div className={styles.cardContent}>
                  <div className={styles.header}>
                    <span className={styles.eyebrow}>
                      <span className={styles.eyebrowDot} aria-hidden="true" />
                      {eyebrow}
                    </span>
                    <h1 className={styles.title} ref={headingRef} tabIndex={-1}>
                      {heading}
                    </h1>
                    <p className={styles.description}>{description}</p>
                  </div>

                  {children}
                </div>
              </div>

              {footer && <div className={styles.belowCard}>{footer}</div>}
            </motion.section>

            <motion.aside
              className={styles.visualColumn}
              aria-hidden="true"
              initial={reduced ? false : { opacity: 0, x: 30, scale: 0.97 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              transition={{ duration: 1, delay: 0.16, ease: [0.22, 1, 0.36, 1] }}
            >
              {visual}
            </motion.aside>
          </div>
        </main>

        <footer className={styles.pageFooter}>
          <span>© {year} Prisma.AI</span>
          <span className={styles.footerSignature}>Seu dinheiro. Suas escolhas. Seu futuro.</span>
        </footer>
      </div>
    </MotionConfig>
  )
}
