import { useEffect } from 'react'
import {
  MotionConfig,
  motion,
  useMotionValue,
  useScroll,
  useSpring,
} from 'framer-motion'
import { Navbar } from './components/Navbar'
import { HeroSection } from './components/HeroSection'
import { SolutionSection } from './components/SolutionSection'
import { HowItWorksSection } from './components/HowItWorksSection'
import { AgentsSection } from './components/AgentsSection'
import { ExperienceSection } from './components/ExperienceSection'
import { AutonomySection } from './components/AutonomySection'
import { FinalCTASection } from './components/FinalCTASection'
import { Footer } from './components/Footer'
import './landing.css'

function ScrollProgress() {
  const { scrollYProgress } = useScroll()
  const scaleX = useSpring(scrollYProgress, { stiffness: 110, damping: 28, restDelta: 0.001 })

  return <motion.div className="pl-scroll-progress" style={{ scaleX }} aria-hidden="true" />
}

function CursorGlow() {
  const x = useMotionValue(-300)
  const y = useMotionValue(-300)
  const springX = useSpring(x, { stiffness: 90, damping: 24, mass: 0.5 })
  const springY = useSpring(y, { stiffness: 90, damping: 24, mass: 0.5 })

  useEffect(() => {
    if (!window.matchMedia('(pointer: fine)').matches) return
    const handler = (event: PointerEvent) => {
      x.set(event.clientX)
      y.set(event.clientY)
    }
    window.addEventListener('pointermove', handler, { passive: true })
    return () => window.removeEventListener('pointermove', handler)
  }, [x, y])

  return <motion.div className="pl-cursor-glow" style={{ x: springX, y: springY }} aria-hidden="true" />
}

export function LandingPage() {
  useEffect(() => {
    const html = document.documentElement
    const previousTitle = document.title
    html.classList.add('pl-landing-html')
    document.title = 'Prisma.AI — Educação financeira para jovens adultos'

    return () => {
      html.classList.remove('pl-landing-html')
      document.title = previousTitle
    }
  }, [])

  return (
    <MotionConfig reducedMotion="user">
      <div className="prisma-landing">
        <a href="#conteudo" className="pl-skip-link">Pular para o conteúdo</a>
        <ScrollProgress />
        <CursorGlow />
        <Navbar />
        <main id="conteudo">
          <HeroSection />
          <SolutionSection />
          <HowItWorksSection />
          <AgentsSection />
          <ExperienceSection />
          <AutonomySection />
          <FinalCTASection />
        </main>
        <Footer />
      </div>
    </MotionConfig>
  )
}
