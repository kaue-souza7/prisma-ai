import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { journeyApi } from '@/api'
import { Button } from '@/design-system'
import {
  ArrowRightIcon,
  CheckIcon,
  LockIcon,
  PlayIcon,
  SparkIcon,
} from '@/design-system/Icons'
import type { JourneyOverview, MissionStatus, MissionWithProgress, PhaseJourney } from '@/types/student'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import { AgentAvatar, PhaseArt } from './components/StudentVisuals'
import styles from './Journey.module.css'

const STATUS_LABELS: Record<MissionStatus, string> = {
  locked: 'Bloqueada',
  available: 'Disponível',
  in_progress: 'Em andamento',
  completed: 'Concluída',
}

const PHASE_LABELS: Record<string, string> = {
  locked: 'Bloqueada',
  available: 'Disponível',
  in_progress: 'Em andamento',
  completed: 'Concluída',
}

function firstActionableMission(phases: PhaseJourney[]): MissionWithProgress | null {
  for (const phase of phases) {
    const mission = phase.missions.find(
      (item) => item.status === 'in_progress' || item.status === 'available',
    )
    if (mission) return mission
  }
  return null
}

function MissionStateIcon({ status }: { status: MissionStatus }) {
  if (status === 'completed') return <CheckIcon size={14} />
  if (status === 'in_progress') return <PlayIcon size={14} />
  if (status === 'available') return <ArrowRightIcon size={14} />
  return <LockIcon size={13} />
}

export function JourneyPage() {
  useDocumentTitle('Minha jornada — Prisma.AI')
  const [phases, setPhases] = useState<PhaseJourney[]>([])
  const [overview, setOverview] = useState<JourneyOverview | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    setLoading(true)
    setError('')
    journeyApi
      .getOverview()
      .then((response) => {
        setOverview(response.data)
        setPhases(response.data.phases)
      })
      .catch(() => setError('Não foi possível carregar sua jornada. Tente novamente.'))
      .finally(() => setLoading(false))
  }, [reloadKey])

  if (loading) {
    return (
      <div className={`st-app-page ${styles.loadingPage}`}>
        <div className={`st-skeleton ${styles.loadingHeader}`} />
        {[1, 2, 3].map((item) => (
          <div key={item} className={`st-skeleton ${styles.loadingCard}`} />
        ))}
      </div>
    )
  }

  if (error) {    return (
      <div className={`st-app-page ${styles.errorPage}`}>
        <div className={styles.errorCard} role="alert">
          <h1>Não conseguimos abrir sua jornada.</h1>
          <p>{error}</p>
          <Button onClick={() => setReloadKey((value) => value + 1)}>
            Tentar novamente
          </Button>
        </div>
      </div>
    )
  }

  const nextMission = firstActionableMission(phases)
  const currentPhase =
    phases.find((phase) => phase.status === 'in_progress') ??
    phases.find((phase) => phase.status === 'available')
  const recommendation = overview?.recommendation
  const trail = overview?.trail

  return (
    <div className={`st-app-page ${styles.page}`}>
      <header className={styles.hero}>
        <div className={styles.heroCopy}>
          <span className="st-eyebrow">Minha jornada</span>
          <h1>
            Seu caminho, <span>missão por missão.</span>
          </h1>
          <p>
            A ordem das trilhas vem do seu objetivo. Dentro de cada trilha, as missões
            abrem conforme você conclui a anterior — sem pressa e sem atalhos.
          </p>
          <div className={styles.heroMeta}>
            <span className="st-chip st-chip--purple">
              <SparkIcon size={12} />
              {currentPhase
                ? currentPhase.status === 'in_progress'
                  ? `Trilha ${currentPhase.phase.number} em andamento`
                  : `Trilha ${currentPhase.phase.number} é seu ponto de partida`
                : 'Jornada concluída'}
            </span>
            <span className="st-chip">12 trilhas</span>
          </div>
          {recommendation && (
            <div className={styles.catalystLine}>
              <AgentAvatar agent="catalyst" size={28} />
              <span>
                <strong>Catalisador</strong>
                {recommendation.message}
              </span>
            </div>
          )}
        </div>
        {nextMission && (
          <div className={styles.heroAction}>
            <span>Próxima missão</span>
            <strong>{nextMission.mission.name}</strong>
            <Link
              to={`/student/learn/${nextMission.mission.id}`}
              className={styles.primaryAction}
            >
              {nextMission.status === 'in_progress' ? 'Continuar missão' : 'Começar agora'}
              <ArrowRightIcon size={16} />
            </Link>
          </div>
        )}
      </header>

      {trail && (
        <section className={styles.trailBanner} aria-label="Sua trilha personalizada">
          <div className={styles.trailHeader}>
            <div>
              <span className="st-eyebrow">Sua jornada</span>
              <h2>
                {trail.source === 'standard'
                  ? 'Ordem padrão das 12 trilhas'
                  : 'Personalizada a partir do seu objetivo'}
              </h2>
            </div>
            <span className={styles.trailPace}>{trail.pace === 'accelerated' ? 'Ritmo acelerado' : trail.pace === 'supported' ? 'Com mais apoio' : 'Ritmo equilibrado'}</span>
          </div>
          <div className={styles.trailPath}>
            {trail.phases.map((phase, index) => (
              <span key={phase.number} className={styles.trailStep}>
                <small>{index + 1}</small>
                Trilha {phase.number} · {phase.name}
              </span>
            ))}
          </div>
          <p className={styles.trailRationale}>{trail.rationale}</p>
        </section>
      )}

      <section className={styles.timeline} aria-label="Trilhas da jornada">
        {phases.map((phase, index) => {
          const total = phase.missions.length
          const completed = phase.missions.filter(
            (mission) => mission.status === 'completed',
          ).length
          const progress = total ? Math.round((completed / total) * 100) : 0
          const actionable = phase.missions.find(
            (mission) => mission.status === 'available' || mission.status === 'in_progress',
          )

          return (
            <article
              key={phase.phase.id}
              className={[
                styles.phaseCard,
                phase.status === 'locked' ? styles.phaseLocked : '',
                phase.status === 'in_progress' ? styles.phaseCurrent : '',
                phase.status === 'completed' ? styles.phaseDone : '',
              ].join(' ')}
            >
              <div className={styles.timelineRail} aria-hidden="true">
                <span className={styles.timelineDot}>
                  {phase.status === 'completed' ? (
                    <CheckIcon size={14} />
                  ) : phase.status === 'locked' ? (
                    <LockIcon size={13} />
                  ) : (
                    String(phase.phase.number).padStart(2, '0')
                  )}
                </span>
                {index < phases.length - 1 && <span className={styles.timelineLine} />}
              </div>

              <div className={styles.phaseBody}>
                <div className={styles.phaseHead}>
                  <div className={styles.phaseIdentity}>
                    <PhaseArt number={phase.phase.number} size={66} />
                    <div>
                      <span className={styles.phaseKicker}>
                        Trilha {String(phase.phase.number).padStart(2, '0')}
                      </span>
                      <h2>{phase.phase.name}</h2>
                      <p>{phase.phase.description}</p>
                    </div>
                  </div>
                  <span
                    className={[
                      styles.phaseBadge,
                      styles[`phaseBadge_${phase.status}`],
                    ].join(' ')}
                  >
                    {phase.status === 'locked' && <LockIcon size={11} />}
                    {PHASE_LABELS[phase.status]}
                  </span>
                </div>

                <div className={styles.phaseProgress}>
                  <div className={styles.progressTrack}>
                    <span style={{ width: `${progress}%` }} />
                  </div>
                  <span>
                    {total ? `${completed} de ${total} missões` : 'Em preparação'}
                  </span>
                </div>

                {total === 0 ? (
                  <div className={styles.emptyPhase}>
                    <span aria-hidden="true"><LockIcon size={15} /></span>
                    <p>
                      Esta trilha será liberada em uma próxima etapa da jornada.
                      O mapa mostra o horizonte completo do seu aprendizado.
                    </p>
                  </div>
                ) : (
                  <ul className={styles.missionList}>
                    {phase.missions.map(({ mission, progress: missionProgress, status }) => {
                      const content = (
                        <>
                          <span className={[styles.missionState, styles[`missionState_${status}`]].join(' ')}>
                            <MissionStateIcon status={status} />
                          </span>
                          <span className={styles.missionInfo}>
                            <span className={styles.missionName}>
                              {mission.number}. {mission.name}
                            </span>
                            <span className={styles.missionMeta}>
                              {STATUS_LABELS[status]}
                              {missionProgress?.score != null
                                ? ` · ${missionProgress.score} pts`
                                : ''}
                              {!mission.is_required ? ' · opcional' : ''}
                            </span>
                          </span>
                          {status !== 'locked' && (
                            <ArrowRightIcon size={15} className={styles.missionArrow} />
                          )}
                        </>
                      )

                      return (
                        <li key={mission.id}>
                          {status === 'locked' ? (
                            <div className={`${styles.missionRow} ${styles.missionLocked}`}>
                              {content}
                            </div>
                          ) : (
                            <Link
                              to={`/student/learn/${mission.id}`}
                              className={styles.missionRow}
                            >
                              {content}
                            </Link>
                          )}
                        </li>
                      )
                    })}
                  </ul>
                )}

                {actionable && phase.status !== 'locked' && (
                  <div className={styles.phaseFooter}>
                    <span>
                      Próxima: <strong>{actionable.mission.name}</strong>
                    </span>
                    <Link
                      to={`/student/learn/${actionable.mission.id}`}
                      className="st-link-arrow"
                    >
                      Continuar
                      <ArrowRightIcon size={13} />
                    </Link>
                  </div>
                )}
              </div>
            </article>
          )
        })}
      </section>
    </div>
  )
}
