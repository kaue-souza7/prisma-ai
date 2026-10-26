import { useRef } from 'react'
import { motion, useReducedMotion, useScroll, useSpring } from 'framer-motion'
import { CompassPathIcon, LayersIcon, TargetIcon } from '@/design-system/Icons'
import { Reveal, SectionHeading } from './primitives'

const steps = [
  {
    number: '01',
    icon: CompassPathIcon,
    title: 'Onboarding: seu ponto de partida',
    description:
      'Responda algumas perguntas rápidas, defina uma meta pessoal e descubra por qual fase começar. Nenhum dado bancário solicitado.',
    tag: 'Contexto e objetivos',
  },
  {
    number: '02',
    icon: LayersIcon,
    title: 'Missões, simulações e feedback',
    description:
      'Pratique decisões financeiras em cenários fictícios, receba feedback contextual e conte com o Mentor quando tiver dúvidas.',
    tag: 'Prática guiada',
  },
  {
    number: '03',
    icon: TargetIcon,
    title: 'Avance por competências demonstradas',
    description:
      'O progresso depende do que você aprende, não do tempo gasto. Conquistas, pontos e próximas fases se desbloqueiam conforme você avança.',
    tag: 'Progresso visível',
  },
]

export function HowItWorksSection() {
  const ref = useRef<HTMLElement>(null)
  const reduced = useReducedMotion()
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start 75%', 'end 55%'],
  })
  const progress = useSpring(scrollYProgress, {
    stiffness: 90,
    damping: 24,
    restDelta: 0.001,
  })

  return (
    <section className="pl-section pl-how" id="como-funciona" ref={ref}>
      <div className="pl-section-glow pl-section-glow--right" aria-hidden="true" />
      <div className="pl-container">
        <SectionHeading
          eyebrow="Como funciona"
          title={<>Três passos. Seis fases. <span className="pl-gradient-text">Uma nova relação</span> com o dinheiro.</>}
          description="Uma jornada progressiva com critérios claros de progressão. O foco está no que você aprende e consegue aplicar — não no tempo que passou na plataforma."
          align="center"
        />

        <div className="pl-process">
          <div className="pl-process-line" aria-hidden="true">
            <motion.span
              className="pl-process-line-fill"
              style={{ scaleX: reduced ? 1 : progress }}
            />
          </div>
          <div className="pl-process-line-mobile" aria-hidden="true">
            <motion.span
              style={{ scaleY: reduced ? 1 : progress }}
            />
          </div>

          {steps.map((step, index) => {
            const Icon = step.icon
            return (
              <Reveal key={step.number} className="pl-process-step-wrap" delay={index * 0.1}>
                <article className="pl-process-step">
                  <div className="pl-process-number">
                    <span>{step.number}</span>
                    <span className="pl-process-node"><Icon size={18} /></span>
                  </div>
                  <div className="pl-process-card">
                    <span className="pl-process-tag">{step.tag}</span>
                    <h3>{step.title}</h3>
                    <p>{step.description}</p>
                  </div>
                </article>
              </Reveal>
            )
          })}
        </div>

        <Reveal className="pl-how-note" delay={0.18}>
          <span className="pl-how-note-line" aria-hidden="true" />
          Você não precisa ter conhecimento prévio. A jornada começa do zero
          e constrói sua autonomia financeira passo a passo.
        </Reveal>
      </div>
    </section>
  )
}
