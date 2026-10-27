import {
  ArrowRightIcon,
  CheckIcon,
  LockIcon,
  PlayIcon,
  SparkIcon,
} from '@/design-system/Icons'
import { PhaseArt } from '@/areas/student/components/StudentVisuals'
import { AppShell } from './AppShell'
import {
  PREVIEW_PHASES,
  phaseProgress,
} from './studentPreviewData'
import type { PreviewMission, PreviewPhase } from './studentPreviewData'

const PHASE_STATUS_LABELS: Record<PreviewPhase['status'], string> = {
  completed: 'Concluída',
  in_progress: 'Em andamento',
  locked: 'Bloqueada',
}

const MISSION_LABELS: Record<PreviewMission['status'], string> = {
  completed: 'Concluída',
  in_progress: 'Em andamento',
  available: 'Disponível',
  locked: 'Bloqueada',
}

function MissionIcon({ status }: { status: PreviewMission['status'] }) {
  if (status === 'completed') return <CheckIcon size={12} />
  if (status === 'in_progress') return <PlayIcon size={12} />
  if (status === 'available') return <ArrowRightIcon size={12} />
  return <LockIcon size={11} />
}

export function JourneyScreen() {
  return (
    <AppShell active="journey">
      <div className="pl-app-page">
      <header className="pl-app-journey-hero">
        <div className="pl-app-journey-copy">
          <span className="pl-app-eyebrow">Minha jornada</span>
          <h1>
            Seu caminho, <span>missão por missão.</span>
          </h1>
          <p>
            Cada trilha aprofunda uma parte da sua relação com o dinheiro. As
              missões abrem conforme você conclui a anterior — sem pressa e sem
              atalhos.
            </p>
            <div className="pl-app-chip-row">
              <span className="pl-app-chip is-purple">
                <SparkIcon size={10} />
                Trilha 3 em andamento
              </span>
              <span className="pl-app-chip">12 trilhas</span>
            </div>
        </div>

        <div className="pl-app-journey-action">
          <span>Próxima missão</span>
          <strong>Antes de confirmar</strong>
          <span className="pl-app-primary-action">
            Começar agora
            <ArrowRightIcon size={13} />
          </span>
        </div>
      </header>

      <section className="pl-app-timeline" aria-label="Trilhas da jornada">
        {PREVIEW_PHASES.slice(0, 3).map((phase, index) => {
          const progress = phaseProgress(phase)
          const next = phase.missions.find(
            (mission) => mission.status === 'available' || mission.status === 'in_progress',
          )

          return (
            <article
              key={phase.number}
              className={`pl-app-timeline-phase is-${phase.status}`}
            >
              <div className="pl-app-timeline-rail" aria-hidden="true">
                <span className="pl-app-timeline-dot">
                  {phase.status === 'completed' ? (
                    <CheckIcon size={12} />
                  ) : phase.status === 'locked' ? (
                    <LockIcon size={11} />
                  ) : (
                    String(phase.number).padStart(2, '0')
                  )}
                </span>
                {index < 2 && <span className="pl-app-timeline-line" />}
              </div>

              <div className="pl-app-timeline-body">
                <div className="pl-app-timeline-head">
                  <div className="pl-app-timeline-identity">
                    <PhaseArt number={phase.number} size={52} />
                    <div>
                      <span className="pl-app-phase-kicker">
                        Trilha {String(phase.number).padStart(2, '0')}
                      </span>
                      <h2>{phase.name}</h2>
                      <p>{phase.description}</p>
                    </div>
                  </div>
                  <span className={`pl-app-phase-badge is-${phase.status}`}>
                    {phase.status === 'locked' && <LockIcon size={9} />}
                    {PHASE_STATUS_LABELS[phase.status]}
                  </span>
                </div>

                <div className="pl-app-timeline-progress">
                  <div className="pl-app-track">
                    <span style={{ width: `${progress.percent}%` }} />
                  </div>
                  <span>
                    {progress.completed} de {progress.total} missões
                  </span>
                </div>

                <div className="pl-app-mission-list">
                  {phase.missions.map((mission) => (
                    <div
                      key={mission.number}
                      className={`pl-app-mission-row is-${mission.status}`}
                    >
                      <span className={`pl-app-mission-state is-${mission.status}`}>
                        <MissionIcon status={mission.status} />
                      </span>
                      <span className="pl-app-mission-info">
                        <strong>
                          {mission.number}. {mission.name}
                        </strong>
                        <small>
                          {MISSION_LABELS[mission.status]}
                          {mission.score != null ? ` · ${mission.score} pts` : ''}
                        </small>
                      </span>
                      {mission.status !== 'locked' && (
                        <ArrowRightIcon size={13} className="pl-app-mission-arrow" />
                      )}
                    </div>
                  ))}
                </div>

                {next && phase.status !== 'locked' && (
                  <div className="pl-app-timeline-footer">
                    <span>
                      Próxima: <strong>{next.name}</strong>
                    </span>
                    <span className="pl-app-card-link">
                      Continuar
                      <ArrowRightIcon size={11} />
                    </span>
                  </div>
                )}
              </div>
            </article>
          )
        })}
      </section>
      </div>
    </AppShell>
  )
}
