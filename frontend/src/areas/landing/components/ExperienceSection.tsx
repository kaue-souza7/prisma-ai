import { useState } from 'react'
import type { ReactElement } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import {
  BookIcon,
  ChartIcon,
  ChatIcon,
  CheckIcon,
  CompassPathIcon,
} from '@/design-system/Icons'
import { JourneyScreen } from './screens/JourneyScreen'
import { LessonScreen } from './screens/LessonScreen'
import { ProgressScreen } from './screens/ProgressScreen'
import { ScreenViewport } from './screens/ScreenViewport'
import { Reveal, SectionHeading } from './primitives'

type TabKey = 'trilha' | 'missao' | 'progresso'

const tabs: Array<{ key: TabKey; label: string; icon: typeof CompassPathIcon }> = [
  { key: 'trilha', label: 'Jornada', icon: CompassPathIcon },
  { key: 'missao', label: 'Minicurso', icon: BookIcon },
  { key: 'progresso', label: 'Progresso', icon: ChartIcon },
]

const screens: Record<
  TabKey,
  { url: string; label: string; screen: ReactElement }
> = {
  trilha: {
    url: 'app.prisma.ai/jornada',
    label: 'Tela de exemplo da jornada do estudante, com as trilhas e missões',
    screen: <JourneyScreen />,
  },
  missao: {
    url: 'app.prisma.ai/minicurso/2.2',
    label: 'Tela de exemplo de um minicurso, com atividade e feedback',
    screen: <LessonScreen />,
  },
  progresso: {
    url: 'app.prisma.ai/progresso',
    label: 'Tela de exemplo de conquistas e progresso do estudante',
    screen: <ProgressScreen />,
  },
}

const fade = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -6 },
  transition: { duration: 0.28, ease: [0.22, 1, 0.36, 1] as const },
}

export function ExperienceSection() {
  const [active, setActive] = useState<TabKey>('trilha')
  const activeScreen = screens[active]

  return (
    <section className="pl-section pl-experience" id="experiencia">
      <div className="pl-experience-glow" aria-hidden="true" />
      <div className="pl-container">
        <div className="pl-experience-layout">
          <div className="pl-experience-copy">
            <SectionHeading
              eyebrow="A experiência"
              title={<>Missões, feedback e <span className="pl-gradient-text">progresso visível.</span></>}
              description="Jornada com trilhas de aprendizagem, minicursos com atividades e feedback contextual, e conquistas que marcam cada avanço real na sua aprendizagem."
            />

            <Reveal delay={0.12}>
              <ul className="pl-experience-list">
                <li><span><CheckIcon size={13} /></span>Trilhas que vão do primeiro salário à proteção digital</li>
                <li><span><CheckIcon size={13} /></span>Atividades com feedback imediato, sem risco real</li>
                <li><span><CheckIcon size={13} /></span>Pontos, conquistas e competências por trilha</li>
              </ul>
            </Reveal>

            <Reveal delay={0.18}>
              <div className="pl-experience-note">
                <span className="pl-experience-note-icon"><ChatIcon size={15} /></span>
                <p>
                  Telas reais do produto com dados de exemplo. Nenhum dado
                  bancário é solicitado nem nenhuma transação real é realizada.
                </p>
              </div>
            </Reveal>
          </div>

          <Reveal className="pl-experience-stage" delay={0.08} y={36}>
            <div className="pl-experience-window">
              <div className="pl-experience-window-top">
                <div className="pl-preview-dots" aria-hidden="true"><span /><span /><span /></div>
                <span className="pl-experience-url">{activeScreen.url}</span>
                <span className="pl-experience-window-badge">Tela do produto</span>
              </div>

              <div className="pl-experience-window-inner">
                <div className="pl-exp-tabs" role="tablist" aria-label="Telas do produto">
                  {tabs.map((tab) => {
                    const Icon = tab.icon
                    const selected = active === tab.key
                    return (
                      <button
                        key={tab.key}
                        id={`pl-exp-tab-${tab.key}`}
                        type="button"
                        role="tab"
                        aria-selected={selected}
                        aria-controls="pl-exp-panel"
                        tabIndex={selected ? 0 : -1}
                        className={selected ? 'is-active' : ''}
                        onClick={() => setActive(tab.key)}
                      >
                        <Icon size={14} />
                        {tab.label}
                      </button>
                    )
                  })}
                </div>

                <div
                  className="pl-exp-panel"
                  id="pl-exp-panel"
                  role="tabpanel"
                  aria-labelledby={`pl-exp-tab-${active}`}
                >
                  <AnimatePresence mode="wait" initial={false}>
                    <motion.div key={active} className="pl-exp-screen" {...fade}>
                      <ScreenViewport label={activeScreen.label}>
                        {activeScreen.screen}
                      </ScreenViewport>
                    </motion.div>
                  </AnimatePresence>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  )
}
