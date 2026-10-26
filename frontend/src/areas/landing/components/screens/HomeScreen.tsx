import {
  ArrowRightIcon,
  CheckIcon,
  LockIcon,
  SparkIcon,
  TrophyIcon,
} from '@/design-system/Icons'
import { PhaseArt, PrismMascot, ProgressRing } from '@/areas/student/components/StudentVisuals'
import { AppShell } from './AppShell'
import {
  PREVIEW_ACHIEVEMENTS,
  PREVIEW_PHASES,
  PREVIEW_PROGRESS,
  PREVIEW_STUDENT,
  phaseProgress,
} from './studentPreviewData'
import type { PreviewPhase } from './studentPreviewData'

const PHASE_STATUS_LABELS: Record<PreviewPhase['status'], string> = {
  completed: 'Concluída',
  in_progress: 'Em andamento',
  locked: 'Bloqueada',
}

export function HomeScreen() {
  const currentPhase = PREVIEW_PHASES.find((phase) => phase.status === 'in_progress')
  const nextMission = currentPhase?.missions.find(
    (mission) => mission.status === 'available' || mission.status === 'in_progress',
  )

  return (
    <AppShell active="home">
      <div className="pl-app-page">
      <header className="pl-app-home-head">
        <div>
          <span className="pl-app-eyebrow">Seu espaço de aprendizagem</span>
          <h1>
            Olá, {PREVIEW_STUDENT.name}. <span>Vamos dar o próximo passo?</span>
          </h1>
          <p>
            Você está na fase 2, Seu dinheiro no digital. Continue de onde parou
            e transforme conhecimento em decisões melhores.
          </p>
        </div>
        <span className="pl-app-context-pill">
          <span className="pl-app-context-dot" />
          Fase 2 de 6
        </span>
      </header>

      <section className="pl-app-home-hero" aria-label="Próximo passo e progresso">
        <article className="pl-app-next-card">
          <div className="pl-app-next-glow" aria-hidden="true" />
          <div className="pl-app-next-copy">
            <span className="pl-app-next-eyebrow">
              <SparkIcon size={11} />
              Seu próximo passo
            </span>
            {nextMission ? (
              <>
                <h2>{nextMission.name}</h2>
                <p>
                  Entenda limite, fechamento, vencimento e fatura, e saiba o que
                  acontece quando você paga só uma parte.
                </p>
                <div className="pl-app-next-meta">
                  <span>{nextMission.number}.ª missão da fase</span>
                  <span>Obrigatória</span>
                  <span>Até 100 pts</span>
                </div>
                <div className="pl-app-next-actions">
                  <span className="pl-app-primary-action">
                    Começar agora
                    <ArrowRightIcon size={14} />
                  </span>
                  <span className="pl-app-secondary-action">Ver toda a jornada</span>
                </div>
              </>
            ) : null}
          </div>

          <div className="pl-app-next-art" aria-hidden="true">
            <span className="pl-app-art-orb" />
            <span className="pl-app-art-ring" />
            <PrismMascot size={186} />
            {nextMission && (
              <span className="pl-app-floating-badge">
                <span className="pl-app-floating-icon">
                  <CheckIcon size={11} />
                </span>
                <span>
                  <small>Missão {nextMission.number}</small>
                  <strong>Disponível</strong>
                </span>
              </span>
            )}
          </div>
        </article>

        <aside className="pl-app-progress-card">
          <div className="pl-app-progress-top">
            <div>
              <span className="pl-app-eyebrow">Seu momento</span>
              <h2>{PREVIEW_PROGRESS.levelName}</h2>
              <p>Nível {PREVIEW_PROGRESS.level} de 5</p>
            </div>
            <ProgressRing value={PREVIEW_PROGRESS.progressPercent} size={102} stroke={9}>
              <strong>{PREVIEW_PROGRESS.points}</strong>
              <small>pontos</small>
            </ProgressRing>
          </div>

          <div className="pl-app-level-track">
            <span style={{ width: `${PREVIEW_PROGRESS.progressPercent}%` }} />
          </div>
          <p className="pl-app-level-hint">
            Faltam {PREVIEW_PROGRESS.nextLevelPoints - PREVIEW_PROGRESS.points} pontos
            para o próximo nível.
          </p>

          <div className="pl-app-mini-stats">
            <div>
              <strong>{PREVIEW_PROGRESS.missionsCompleted}</strong>
              <span>missões concluídas</span>
            </div>
            <div>
              <strong>{PREVIEW_PROGRESS.achievementsCount}</strong>
              <span>conquistas</span>
            </div>
          </div>

          <span className="pl-app-card-link">
            Ver competências e conquistas
            <ArrowRightIcon size={12} />
          </span>
        </aside>
      </section>

      <section className="pl-app-section">
        <div className="pl-app-section-head">
          <div>
            <span className="pl-app-eyebrow">Mapa da jornada</span>
            <h2>Seis fases, uma evolução contínua.</h2>
            <p>Cada fase conecta um conceito novo a decisões do dia a dia.</p>
          </div>
          <span className="pl-app-card-link">
            Abrir jornada completa
            <ArrowRightIcon size={12} />
          </span>
        </div>

        <div className="pl-app-phase-grid">
          {PREVIEW_PHASES.map((phase) => {
            const progress = phaseProgress(phase)
            const next = phase.missions.find(
              (mission) => mission.status === 'available' || mission.status === 'in_progress',
            )
            return (
              <article
                key={phase.number}
                className={[
                  'pl-app-phase-card',
                  phase.status === 'in_progress' ? 'is-current' : '',
                  phase.status === 'locked' ? 'is-locked' : '',
                ].join(' ')}
              >
                <div className="pl-app-phase-top">
                  <PhaseArt number={phase.number} size={46} />
                  <span className={`pl-app-phase-badge is-${phase.status}`}>
                    {phase.status === 'locked' && <LockIcon size={9} />}
                    {PHASE_STATUS_LABELS[phase.status]}
                  </span>
                </div>

                <div className="pl-app-phase-copy">
                  <span>Fase {String(phase.number).padStart(2, '0')}</span>
                  <h3>{phase.name}</h3>
                  <p>{phase.description}</p>
                  {next && <small>Próxima: {next.name}</small>}
                </div>

                <div className="pl-app-phase-bottom">
                  <div className="pl-app-phase-track">
                    <span style={{ width: `${progress.percent}%` }} />
                  </div>
                  <small>
                    {progress.completed}/{progress.total} missões
                  </small>
                </div>
              </article>
            )
          })}
        </div>
      </section>

      <section className="pl-app-home-bottom">
        <article className="pl-app-home-card">
          <div className="pl-app-section-head">
            <div>
              <span className="pl-app-eyebrow">Conquistas</span>
              <h2>Marcos da sua jornada.</h2>
            </div>
          </div>
          <div className="pl-app-achievement-list">
            {PREVIEW_ACHIEVEMENTS.map((achievement) => (
              <div className="pl-app-achievement-row" key={achievement.key}>
                <span className="pl-app-trophy">
                  <TrophyIcon size={13} />
                </span>
                <div>
                  <strong>{achievement.name}</strong>
                  <span>{achievement.date}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>
      </div>
    </AppShell>
  )
}
