import { useRef } from 'react'
import { Link } from 'react-router-dom'
import {
  motion,
  useReducedMotion,
  useScroll,
  useTransform,
} from 'framer-motion'
import { ArrowRightIcon, SparkIcon } from '@/design-system/Icons'
import { Magnetic, Tilt } from './primitives'
import { ParticleField } from '@/design-system/brand/ParticleField'
import { PrismArt } from '@/design-system/brand/PrismArt'
import { ProductPreview } from './ProductPreview'

const container = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.09, delayChildren: 0.18 },
  },
}

const line = {
  hidden: { opacity: 0, y: 34, filter: 'blur(12px)' },
  show: {
    opacity: 1,
    y: 0,
    filter: 'blur(0px)',
    transition: { duration: 0.9, ease: [0.22, 1, 0.36, 1] as const },
  },
}

export function HeroSection() {
  const ref = useRef<HTMLElement>(null)
  const reduced = useReducedMotion()
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start start', 'end start'],
  })
  const stageY = useTransform(scrollYProgress, [0, 1], [0, 92])
  const stageRotate = useTransform(scrollYProgress, [0, 1], [0, -2.5])
  const lightY = useTransform(scrollYProgress, [0, 1], [0, 160])

  return (
    <section className="pl-hero" id="inicio" ref={ref}>
      <div className="pl-hero-bg" aria-hidden="true">
        <div className="pl-hero-grid" />
        <motion.div className="pl-hero-aurora pl-hero-aurora--one" style={reduced ? undefined : { y: lightY }} />
        <motion.div className="pl-hero-aurora pl-hero-aurora--two" style={reduced ? undefined : { y: lightY }} />
        <div className="pl-hero-noise" />
        <ParticleField count={42} />
      </div>

      <div className="pl-container pl-hero-inner">
        <motion.div
          className="pl-hero-copy"
          variants={container}
          initial={reduced ? false : 'hidden'}
          animate="show"
        >
          <motion.p className="pl-hero-eyebrow" variants={line}>
            <span className="pl-live-dot" aria-hidden="true" />
            Educação financeira para jovens adultos
            <span className="pl-hero-eyebrow-tag">visão do produto</span>
          </motion.p>

          <h1 className="pl-hero-title" aria-label="Sua jornada. Suas escolhas. Seu futuro.">
            <motion.span variants={line} className="pl-hero-line">Sua jornada.</motion.span>
            <motion.span variants={line} className="pl-hero-line">Suas escolhas.</motion.span>
            <motion.span variants={line} className="pl-hero-line pl-gradient-text pl-hero-future">
              Seu futuro.
              <span className="pl-hero-underline" aria-hidden="true" />
            </motion.span>
          </h1>

          <motion.p className="pl-hero-copy-text" variants={line}>
            Doze trilhas de aprendizagem prática — do primeiro salário à proteção digital.
            Missões reais, simulações e agentes de IA que acompanham o seu raciocínio.
          </motion.p>

          <motion.div className="pl-hero-actions" variants={line}>
            <Magnetic>
              <Link to="/register" className="pl-btn pl-btn--primary pl-btn--hero">
                Começar minha jornada
                <span className="pl-btn-icon"><ArrowRightIcon size={18} /></span>
              </Link>
            </Magnetic>
            <a href="#experiencia" className="pl-btn pl-btn--glass pl-btn--hero">
              Ver como funciona
            </a>
          </motion.div>

          <motion.div className="pl-hero-disclaimer" variants={line}>
            <span className="pl-hero-disclaimer-icon"><SparkIcon size={15} /></span>
            <span>
              Telas reais da plataforma com dados de exemplo. Os agentes de IA
              serão ativados conforme a integração com o IBM watsonx Orchestrate
              for validada.
            </span>
          </motion.div>
        </motion.div>

        <motion.div
          className="pl-hero-stage"
          style={reduced ? undefined : { y: stageY, rotateZ: stageRotate }}
          initial={reduced ? false : { opacity: 0, scale: 0.92, x: 36 }}
          animate={{ opacity: 1, scale: 1, x: 0 }}
          transition={{ duration: 1.2, delay: 0.25, ease: [0.22, 1, 0.36, 1] }}
        >
          <PrismArt className="pl-hero-prism" />
          <div className="pl-hero-orbit pl-hero-orbit--one" aria-hidden="true" />
          <div className="pl-hero-orbit pl-hero-orbit--two" aria-hidden="true" />

          <Tilt className="pl-hero-tilt">
            <ProductPreview />
          </Tilt>

          <div className="pl-hero-stage-label">
            <span />
            Tela do produto · dados de exemplo
          </div>
        </motion.div>
      </div>

      <div className="pl-container pl-hero-foot">
        <div className="pl-hero-proof">
          <span>12 trilhas de aprendizagem</span>
          <span>45 missões práticas</span>
          <span>Agentes de IA</span>
        </div>
        <a href="#sobre" className="pl-scroll-cue">
          Conheça a jornada
          <span className="pl-scroll-cue-line" aria-hidden="true" />
        </a>
      </div>
    </section>
  )
}
