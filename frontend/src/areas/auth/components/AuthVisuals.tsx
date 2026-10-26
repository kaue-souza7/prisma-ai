import type { ReactNode } from 'react'
import { motion, useReducedMotion } from 'framer-motion'
import {
  CheckIcon,
  CompassIcon,
  LockIcon,
  ShieldIcon,
  SparkIcon,
} from '@/design-system/Icons'
import { PrismArt } from '@/design-system/brand/PrismArt'
import styles from './AuthVisuals.module.css'

interface VisualStageProps {
  tone: 'login' | 'register' | 'support'
  eyebrow: string
  title: ReactNode
  description: string
  caption: string
  children: ReactNode
}

function VisualStage({ tone, eyebrow, title, description, caption, children }: VisualStageProps) {
  return (
    <div className={`${styles.stage} ${styles[`stage--${tone}`]}`}>
      <PrismArt className={styles.prism} />
      <div className={styles.orbitOne} aria-hidden="true" />
      <div className={styles.orbitTwo} aria-hidden="true" />
      <div className={styles.orbitThree} aria-hidden="true" />

      <div className={styles.body}>
        <div className={styles.intro}>
          <span className={styles.eyebrow}>
            <span className={styles.eyebrowDot} />
            {eyebrow}
          </span>
          <h2 className={styles.title}>{title}</h2>
          <p className={styles.description}>{description}</p>
        </div>

        {children}
      </div>

      <span className={styles.caption}>
        <span className={styles.captionLine} />
        {caption}
      </span>
    </div>
  )
}

export function LoginVisual() {
  const reduced = useReducedMotion()

  return (
    <VisualStage
      tone="login"
      eyebrow="Sessão segura"
      title={<>Sua jornada continua<br /><span className={styles.accent}>de onde você parou.</span></>}
      description="Retome missões, confira conquistas e pontos, e siga avançando pelas 6 fases de educação financeira."
      caption="Experiência ilustrativa"
    >
      <motion.div
        className={styles.dashboard}
        initial={reduced ? false : { opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.38, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className={styles.dashTop}>
          <span className={styles.dashIcon}>
            <CompassIcon size={18} />
          </span>
          <div className={styles.dashTitle}>
            <small>Trilha em andamento</small>
            <strong>Fase 1 — Primeiro salário</strong>
          </div>
          <span className={styles.dashStatus}>
            <span aria-hidden="true" />
            Em curso
          </span>
        </div>

        <div className={styles.progressMeta}>
          <span>Seu progresso</span>
          <strong>42%</strong>
        </div>
        <div className={styles.progressTrack}>
          <motion.span
            initial={reduced ? false : { width: 0 }}
            animate={{ width: '42%' }}
            transition={{ duration: 1.1, delay: 0.7, ease: [0.22, 1, 0.36, 1] }}
          />
        </div>

        <div className={styles.missionList}>
          <div className={`${styles.mission} ${styles.missionDone}`}>
            <span className={styles.missionIcon}>
              <CheckIcon size={12} />
            </span>
            <div>
              <strong>De onde vem o dinheiro?</strong>
              <small>Concluída · 100 pts</small>
            </div>
          </div>

          <div className={`${styles.mission} ${styles.missionActive}`}>
            <span className={styles.missionIcon}>
              <SparkIcon size={13} />
            </span>
            <div>
              <strong>O que importa primeiro?</strong>
              <small>Em andamento · Mentor disponível</small>
            </div>
            <span className={styles.missionPulse} aria-hidden="true" />
          </div>

          <div className={`${styles.mission} ${styles.missionLocked}`}>
            <span className={styles.missionIcon}>
              <LockIcon size={12} />
            </span>
            <div>
              <strong>Meu primeiro plano</strong>
              <small>Desbloqueada ao concluir a anterior</small>
            </div>
          </div>
        </div>

        <div className={styles.dashNote}>
          <SparkIcon size={13} />
          <span>O Mentor acompanha seu raciocínio nas atividades e responde dúvidas.</span>
        </div>
      </motion.div>

      <div className={`${styles.floatCard} ${styles.floatTop}`}>
        <span className={styles.floatIconGreen}>
          <ShieldIcon size={15} />
        </span>
        <div>
          <small>Acesso protegido</small>
          <strong>Conexão segura</strong>
        </div>
      </div>
    </VisualStage>
  )
}

const phases = Array.from({ length: 6 }, (_, index) => index)

export function RegisterVisual() {
  const reduced = useReducedMotion()

  return (
    <VisualStage
      tone="register"
      eyebrow="Comece pelo começo"
      title={<>Seis fases.<br /><span className={styles.accent}>Dezoito missões práticas.</span></>}
      description="Do primeiro salário à proteção digital — pratique, simule e avance por competências demonstradas."
      caption="Mapa da jornada"
    >
      <motion.div
        className={styles.journey}
        initial={reduced ? false : { opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.38, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className={styles.journeyTop}>
          <span>Mapa da jornada</span>
          <span className={styles.journeyCount}>6 fases</span>
        </div>

        <div className={styles.journeyPath}>
          <div className={styles.pathLine} aria-hidden="true">
            <motion.span
              initial={reduced ? false : { width: 0 }}
              animate={{ width: '11%' }}
              transition={{ duration: 1, delay: 0.75, ease: [0.22, 1, 0.36, 1] }}
            />
          </div>
          {phases.map((phase) => (
            <span
              key={phase}
              className={`${styles.phase} ${phase === 0 ? styles.phaseActive : ''}`}
            >
              <span className={styles.phaseDot}>
                {phase === 0 ? <SparkIcon size={12} /> : String(phase + 1).padStart(2, '0')}
              </span>
            </span>
          ))}
        </div>

        <div className={styles.pathLabels}>
          <span>Início</span>
          <span>Autonomia</span>
        </div>

        <div className={styles.journeyCurrent}>
          <span className={styles.journeyCurrentIcon}>
            <CompassIcon size={17} />
          </span>
          <div>
            <small>Seu primeiro marco</small>
            <strong>Primeiro salário</strong>
          </div>
          <span className={styles.journeyPoints}>Fase 1</span>
        </div>

        <div className={styles.journeyNote}>
          <span>Onboarding guiado</span>
          <span className={styles.dotSep} aria-hidden="true" />
          <span>IBM watsonx</span>
          <span className={styles.dotSep} aria-hidden="true" />
          <span>Sem dados bancários</span>
        </div>
      </motion.div>

      <div className={`${styles.floatCard} ${styles.floatTop}`}>
        <span className={styles.floatIconPurple}>
          <SparkIcon size={15} />
        </span>
        <div>
          <small>Personalização</small>
          <strong>Trilha ajustada ao seu ritmo</strong>
        </div>
      </div>
    </VisualStage>
  )
}

export function SupportVisual() {
  const reduced = useReducedMotion()

  return (
    <VisualStage
      tone="support"
      eyebrow="Segurança em primeiro lugar"
      title={<>Seu acesso,<br /><span className={styles.accent}>no seu controle.</span></>}
      description="Um fluxo seguro para recuperar sua conta e voltar exatamente de onde parou."
      caption="Proteção em cada etapa"
    >
      <motion.div
        className={styles.supportCard}
        initial={reduced ? false : { opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.38, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className={styles.shieldWrap}>
          <span className={styles.shieldRingOne} aria-hidden="true" />
          <span className={styles.shieldRingTwo} aria-hidden="true" />
          <span className={styles.shieldOrb}>
            <ShieldIcon size={30} />
          </span>
        </div>

        <div className={styles.supportList}>
          <div>
            <span className={styles.supportIcon}>
              <LockIcon size={14} />
            </span>
            <div>
              <strong>Link de uso único</strong>
              <small>Proteção contra acessos indevidos</small>
            </div>
          </div>
          <div>
            <span className={styles.supportIcon}>
              <SparkIcon size={14} />
            </span>
            <div>
              <strong>Confirmação segura</strong>
              <small>O link confirma que a solicitação é sua</small>
            </div>
          </div>
          <div>
            <span className={styles.supportIcon}>
              <ShieldIcon size={14} />
            </span>
            <div>
              <strong>Sem dados bancários</strong>
              <small>Nenhuma informação financeira é solicitada</small>
            </div>
          </div>
        </div>
      </motion.div>

      <div className={`${styles.floatCard} ${styles.floatTop}`}>
        <span className={styles.floatIconGreen}>
          <ShieldIcon size={15} />
        </span>
        <div>
          <small>Privacidade por padrão</small>
          <strong>Somente o essencial</strong>
        </div>
      </div>
    </VisualStage>
  )
}
