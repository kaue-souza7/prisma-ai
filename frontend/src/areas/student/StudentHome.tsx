import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { journeyApi, progressApi } from '@/api'
import { Button } from '@/design-system'
import { ArrowRightIcon, CheckIcon, LockIcon, SparkIcon } from '@/design-system/Icons'
import { useSessionStore } from '@/store/session'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import type {
  JourneyOverview,
  MissionStatus,
  MissionWithProgress,
  PhaseJourney,
  ProgressSummary,
} from '@/types/student'
import {
  AGENT_META,
  AgentAvatar,
  PhaseArt,
  PrismMascot,
  ProgressRing,
} from './components/StudentVisuals'
import { displayName, pluralize } from './format'
import styles from './Home.module.css'

const STATUS_LABELS: Record<MissionStatus, string> = {
  locked: 'Bloqueada',
  available: 'Disponível',
  in_progress: 'Em andamento',
  completed: 'Concluída',
}

const PHASE_STATUS: Record<string, string> = {
  locked: 'Bloqueada',
  available: 'Disponível',
  in_progress: 'Em andamento',
  completed: 'Concluída',
}

function findNextMission(phases: PhaseJourney[]): MissionWithProgress | null {
  for (const phase of phases) {
    const mission = phase.missions.find(
      (item) => item.status === 'in_progress' || item.status === 'available',
    )
    if (mission) return mission
  }
  return null
}

function findCurrentPhase(phases: PhaseJourney[]) {
  return (
    phases.find((phase) => phase.status === 'in_progress') ??
    phases.find((phase) => phase.status === 'available') ??
    [...phases].reverse().find((phase) => phase.status === 'completed') ??
    null
  )
}

function phaseProgress(phase: PhaseJourney) {
  const required = phase.missions.filter((item) => item.mission.is_required)
  if (!required.length) return 0
  const done = required.filter((item) => item.status === 'completed').length
  return Math.round((done / required.length) * 100)
}

export function StudentHome() {
  useDocumentTitle('Início — Prisma.AI')
  const user = useSessionStore((state) => state.user)
  const [summary, setSummary] = useState<ProgressSummary | null>(null)
  const [overview, setOverview] = useState<JourneyOverview | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    setLoading(true)
    setError('')
    Promise.all([progressApi.getSummary(), journeyApi.getOverview()])
      .then(([summaryRes, overviewRes]) => {
        setSummary(summaryRes.data)
        setOverview(overviewRes.data)
      })
      .catch((err) => {
        setError(
          err.response?.data?.error?.message ||
            'Não foi possível carregar seu progresso. Verifique sua conexão e tente novamente.',
        )
      })
      .finally(() => setLoading(false))
  }, [reloadKey])

  if (loading) {
    return (
      <div className={`st-app-page ${styles.loadingPage}`}>
        <div className={`st-skeleton ${styles.loadingHero}`} />
        <div className={styles.loadingGrid}>
          <div className="st-skeleton" />
          <div className="st-skeleton" />
        </div>
      </div>
    )
  }

  if (error || !summary || !overview) {
    return (
      <div className={`st-app-page ${styles.errorPage}`}>
        <div className={styles.errorCard} role="alert">
          <span className={styles.errorIcon} aria-hidden="true">
            <SparkIcon size={22} />
          </span>
          <div>
            <h1>Não conseguimos abrir seu painel.</h1>
            <p>{error || 'Tente novamente em instantes.'}</p>
          </div>
          <Button onClick={() => setReloadKey((value) => value + 1)}>
            Tentar novamente
          </Button>
        </div>
      </div>
    )
  }

  const name = displayName(user?.email)
  const phases: PhaseJourney[] = overview.phases
  const trail = overview.trail
  const recommendation = overview.recommendation
  const nextMission = findNextMission(phases)
  const currentPhase = findCurrentPhase(phases)
  const completed = summary.missions_completed
  const totalPoints = summary.total_points
  const hasNextLevel = summary.next_level_points !== null
  const levelRange = hasNextLevel
    ? Math.max(summary.next_level_points! - summary.current_level_points, 1)
    : 1
  const levelPercent = hasNextLevel
    ? Math.max(
        0,
        Math.min(
          100,
          ((totalPoints - summary.current_level_points) / levelRange) * 100,
        ),
      )
    : 100
  const recentAchievements = summary.achievements.slice(0, 3)

  return (
    <div className={`st-app-page ${styles.page}`}>
      <header className={styles.topline}>
        <div>
          <span className="st-eyebrow">Seu espaço de aprendizagem</span>
          <h1>
            Olá, {name}. <span>Vamos dar o próximo passo?</span>
          </h1>
          <p>
            {currentPhase
              ? `Você está na fase ${currentPhase.phase.number}, ${currentPhase.phase.name}. Continue de onde parou e transforme conhecimento em decisões melhores.`
              : 'Sua jornada financeira começa com uma decisão de cada vez.'}
          </p>
        </div>
        <div className={styles.contextPill}>
          <span className={styles.contextDot} />
          <span>
            {currentPhase ? `Fase ${currentPhase.phase.number} de 6` : 'Jornada pronta'}
          </span>
        </div>
      </header>

      {trail && (
        <section className={styles.trailStrip} aria-label="Sua trilha personalizada">
          <div className={styles.trailIdentity}>
            <AgentAvatar agent="catalyst" size={38} />
            <div>
              <span className="st-eyebrow">Sua trilha</span>
              <strong>
                {trail.source === 'standard' ? 'Ordem padrão' : 'Personalizada pelo Catalisador'}
              </strong>
            </div>
          </div>
          <div className={styles.trailPath} aria-label="Ordem das fases">
            {trail.phases.map((phase, index) => (
              <span key={phase.number} className={styles.trailStep}>
                <small>{index + 1}</small>
                {phase.name}
              </span>
            ))}
          </div>
          <p className={styles.trailRationale}>{trail.rationale}</p>
        </section>
      )}

      <section className={styles.heroGrid} aria-label="Próximo passo e progresso">
        <article className={styles.nextCard}>
          <div className={styles.nextGlow} aria-hidden="true" />
          <div className={styles.nextCopy}>
            <span className={styles.nextEyebrow}>
              <SparkIcon size={13} />
              {nextMission
                ? nextMission.status === 'in_progress'
                  ? 'Continue sua missão'
                  : 'Seu próximo passo'
                : 'Jornada concluída'}
            </span>
            {nextMission ? (
              <>
                <h2>{nextMission.mission.name}</h2>
                <p>
                  {nextMission.mission.description ??
                    'Uma nova situação para praticar e consolidar o que você já sabe.'}
                </p>
                <div className={styles.nextMeta}>
                  <span>{nextMission.mission.number}.ª missão da fase</span>
                  <span>
                    {nextMission.mission.is_required ? 'Obrigatória' : 'Opcional'}
                  </span>
                  <span>Até 100 pts</span>
                </div>
                {recommendation && (
                  <div className={styles.catalystNote}>
                    <AgentAvatar agent="catalyst" size={26} />
                    <span>
                      <strong>Catalisador</strong>
                      {recommendation.message}
                    </span>
                  </div>
                )}
                <div className={styles.nextActions}>
                  <Link
                    to={`/student/learn/${nextMission.mission.id}`}
                    className={styles.primaryAction}
                  >
                    {nextMission.status === 'in_progress' ? 'Continuar missão' : 'Começar agora'}
                    <ArrowRightIcon size={16} />
                  </Link>
                  <Link to="/student/journey" className={styles.secondaryAction}>
                    Ver toda a jornada
                  </Link>
                </div>
              </>
            ) : (
              <>
                <h2>Você concluiu o que está disponível.</h2>
                <p>
                  {recommendation?.message ??
                    'Seu progresso está salvo. As próximas fases entram quando o conteúdo for publicado.'}
                </p>
                <div className={styles.nextActions}>
                  <Link to="/student/progress" className={styles.primaryAction}>
                    Ver meu progresso
                    <ArrowRightIcon size={16} />
                  </Link>
                </div>
              </>
            )}
          </div>

          <div className={styles.nextArt} aria-hidden="true">
            <span className={styles.artOrb} />
            <span className={styles.artRing} />
            <PrismMascot size={236} />
            {nextMission && (
              <div className={styles.floatingBadge}>
                <span className={styles.floatingIcon}>
                  <CheckIcon size={13} />
                </span>
                <span>
                  <small>Missão {nextMission.mission.number}</small>
                  <strong>{STATUS_LABELS[nextMission.status]}</strong>
                </span>
              </div>
            )}
          </div>
        </article>

        <aside className={styles.progressCard}>
          <div className={styles.progressTop}>
            <div>
              <span className="st-eyebrow">Seu momento</span>
              <h2>{summary.level_name}</h2>
              <p>Nível {summary.level} de 5</p>
            </div>
            <ProgressRing value={levelPercent} size={118} stroke={10}>
              <strong>{totalPoints}</strong>
              <small>pontos</small>
            </ProgressRing>
          </div>

          <div className={styles.levelTrack}>
            <span style={{ width: `${levelPercent}%` }} />
          </div>
          <p className={styles.levelHint}>
            {hasNextLevel
              ? `Faltam ${summary.next_level_points! - totalPoints} pontos para o próximo nível.`
              : 'Você chegou ao nível máximo desta jornada.'}
          </p>

          <div className={styles.miniStats}>
            <div>
              <strong>{completed}</strong>
              <span>{pluralize(completed, 'missão concluída', 'missões concluídas')}</span>
            </div>
            <div>
              <strong>{summary.achievements.length}</strong>
              <span>{pluralize(summary.achievements.length, 'conquista', 'conquistas')}</span>
            </div>
          </div>

          <Link to="/student/progress" className="st-link-arrow">
            Ver competências e conquistas
            <ArrowRightIcon size={14} />
          </Link>
        </aside>
      </section>

      <section className={styles.phasesSection}>
        <div className="st-section-heading">
          <div>
            <span className="st-eyebrow">Mapa da jornada</span>
            <h2>Seis fases, uma evolução contínua.</h2>
            <p>Cada fase conecta um conceito novo a decisões do dia a dia.</p>
          </div>
          <Link to="/student/journey" className="st-link-arrow">
            Abrir jornada completa
            <ArrowRightIcon size={14} />
          </Link>
        </div>

        <div className={styles.phaseGrid}>
          {phases.map((item) => {
            const progress = phaseProgress(item)
            const isCurrent = item.phase.id === currentPhase?.phase.id
            const availableMission = item.missions.find(
              (mission) => mission.status === 'available' || mission.status === 'in_progress',
            )
            return (
              <Link
                key={item.phase.id}
                to={
                  availableMission
                    ? `/student/learn/${availableMission.mission.id}`
                    : '/student/journey'
                }
                className={[
                  styles.phaseCard,
                  isCurrent ? styles.phaseCurrent : '',
                  item.status === 'locked' ? styles.phaseLocked : '',
                ].join(' ')}
              >
                <div className={styles.phaseTop}>
                  <PhaseArt number={item.phase.number} size={58} />
                  <span
                    className={[
                      styles.phaseBadge,
                      styles[`phaseBadge_${item.status}`],
                    ].join(' ')}
                  >
                    {item.status === 'locked' && <LockIcon size={11} />}
                    {PHASE_STATUS[item.status]}
                  </span>
                </div>
                <div className={styles.phaseCopy}>
                  <span>Fase {String(item.phase.number).padStart(2, '0')}</span>
                  <h3>{item.phase.name}</h3>
                  <p>{item.phase.description}</p>
                  {availableMission && (
                    <small className={styles.phaseNext}>
                      Próxima: {availableMission.mission.name}
                    </small>
                  )}
                </div>
                <div className={styles.phaseBottom}>
                  <div className={styles.phaseTrack} aria-hidden="true">
                    <span style={{ width: `${progress}%` }} />
                  </div>
                  <small>
                    {item.missions.length
                      ? `${item.missions.filter((mission) => mission.status === 'completed').length}/${item.missions.length} missões`
                      : 'Em preparação'}
                  </small>
                </div>
              </Link>
            )
          })}
        </div>
      </section>

      <section className={styles.bottomGrid}>
        <article className={styles.agentsCard}>
          <div className="st-section-heading">
            <div>
              <span className="st-eyebrow">Seus agentes</span>
              <h2>Companhia para cada momento.</h2>
              <p>Identidades diferentes, um objetivo: apoiar seu aprendizado.</p>
            </div>
          </div>
          <div className={styles.agentList}>
            {(['catalyst', 'mentor', 'analyst'] as const).map((agent) => {
              const meta = AGENT_META[agent]
              return (
                <div key={agent} className={styles.agentRow}>
                  <AgentAvatar agent={agent} size={40} />
                  <div>
                    <strong>{meta.name}</strong>
                    <span>{meta.role}</span>
                  </div>
                  <span className={styles.agentState}>
                    {agent === 'mentor' ? 'Em preparação' : 'Ativo'}
                  </span>
                </div>
              )
            })}
          </div>
          <Link to="/student/mentor" className="st-link-arrow">
            {nextMission ? 'Conversar com o Mentor' : 'Conhecer os agentes'}
            <ArrowRightIcon size={14} />
          </Link>
        </article>

        <article className={styles.achievementsCard}>
          <div className={styles.achievementsHeader}>
            <div>
              <span className="st-eyebrow">Conquistas</span>
              <h2>Marcos da sua jornada.</h2>
            </div>
            <Link to="/student/progress" className="st-link-arrow">
              Ver todas
            </Link>
          </div>
          {recentAchievements.length ? (
            <div className={styles.achievementList}>
              {recentAchievements.map((achievement) => (
                <div key={achievement.key} className={styles.achievementRow}>
                  <span className={styles.trophy} aria-hidden="true">
                    <SparkIcon size={15} />
                  </span>
                  <div>
                    <strong>{achievement.name}</strong>
                    <span>
                      {new Date(achievement.earned_at).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className={styles.emptyAchievements}>
              <span aria-hidden="true"><SparkIcon size={22} /></span>
              <p>
                Sua primeira conquista aparece depois do onboarding e da
                primeira missão.
              </p>
            </div>
          )}
          <div className={styles.achievementFooter}>
            <span className={styles.footerIcon} aria-hidden="true">
              <CheckIcon size={13} />
            </span>
            <span>
              {pluralize(summary.missions_completed, 'missão concluída', 'missões concluídas')} até agora
            </span>
          </div>
        </article>
      </section>
    </div>
  )
}
