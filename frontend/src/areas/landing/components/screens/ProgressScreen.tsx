import {
  ArrowRightIcon,
  CheckIcon,
  SparkIcon,
  TrophyIcon,
} from '@/design-system/Icons'
import {
  AgentAvatar,
  ProgressRing,
} from '@/areas/student/components/StudentVisuals'
import { AppShell } from './AppShell'
import {
  PREVIEW_ACHIEVEMENTS,
  PREVIEW_COMPETENCIES,
  PREVIEW_PROGRESS,
} from './studentPreviewData'

const COMPETENCY_LABELS = {
  demonstrated: 'Demonstrada',
  developing: 'Em desenvolvimento',
  not_started: 'Ainda não iniciada',
} as const

export function ProgressScreen() {
  const reinforcementTopics = PREVIEW_COMPETENCIES.filter(
    (competency) => competency.reinforcement,
  )

  return (
    <AppShell active="progress">
      <div className="pl-app-page">
      <header className="pl-app-progress-head">
        <div>
          <span className="pl-app-eyebrow">Conquistas e progresso</span>
          <h1>
            Seu aprendizado em <span>evidências.</span>
          </h1>
          <p>
            Pontos mostram constância. As competências mostram o que você já
            consegue fazer com o conhecimento.
          </p>
        </div>
        <span className="pl-app-outline-action">
          Continuar jornada
          <ArrowRightIcon size={13} />
        </span>
      </header>

      <section className="pl-app-progress-hero" aria-label="Nível e resumo">
        <article className="pl-app-level-card">
          <div className="pl-app-level-glow" aria-hidden="true" />
          <div className="pl-app-level-copy">
            <span className="pl-app-level-kicker">Seu nível atual</span>
            <h2>{PREVIEW_PROGRESS.levelName}</h2>
            <p>Nível {PREVIEW_PROGRESS.level} de 5</p>
            <div className="pl-app-level-points">
              <strong>{PREVIEW_PROGRESS.points}</strong>
              <span>pontos acumulados</span>
            </div>
            <div className="pl-app-level-track is-on-dark">
              <span style={{ width: `${PREVIEW_PROGRESS.progressPercent}%` }} />
            </div>
            <p className="pl-app-level-hint is-on-dark">
              Faltam {PREVIEW_PROGRESS.nextLevelPoints - PREVIEW_PROGRESS.points}{' '}
              pontos para o próximo nível.
            </p>
          </div>
          <div className="pl-app-level-ring">
            <ProgressRing value={PREVIEW_PROGRESS.progressPercent} size={140} stroke={11}>
              <strong>{Math.round(PREVIEW_PROGRESS.progressPercent)}%</strong>
              <small>até o próximo</small>
            </ProgressRing>
          </div>
        </article>

        <div className="pl-app-stats-column">
          <div className="pl-app-stat-card">
            <span className="pl-app-stat-icon"><CheckIcon size={15} /></span>
            <strong>{PREVIEW_PROGRESS.missionsCompleted}</strong>
            <span>missões concluídas</span>
          </div>
          <div className="pl-app-stat-card">
            <span className="pl-app-stat-icon"><SparkIcon size={15} /></span>
            <strong>{PREVIEW_PROGRESS.demonstratedCompetencies}</strong>
            <span>competências demonstradas</span>
          </div>
          <div className="pl-app-stat-card">
            <span className="pl-app-stat-icon"><TrophyIcon size={15} /></span>
            <strong>{PREVIEW_PROGRESS.achievementsCount}</strong>
            <span>conquistas</span>
          </div>
        </div>
      </section>

      <section className="pl-app-section">
        <div className="pl-app-section-head">
          <div>
            <span className="pl-app-eyebrow">Competências</span>
            <h2>O que você já demonstra.</h2>
            <p>Evidências acumuladas a partir das suas respostas.</p>
          </div>
          <span className="pl-app-chip is-mint">
            {PREVIEW_PROGRESS.demonstratedCompetencies} competências demonstradas
          </span>
        </div>

        <div className="pl-app-competency-grid">
          {PREVIEW_COMPETENCIES.map((competency) => (
            <article
              key={competency.code}
              className={`pl-app-competency-card is-${competency.status}`}
            >
              <div className="pl-app-competency-top">
                <span className="pl-app-competency-code">{competency.code}</span>
                <span className="pl-app-competency-status">
                  {COMPETENCY_LABELS[competency.status]}
                </span>
              </div>
              <h3>{competency.name}</h3>
              <div className="pl-app-competency-meta">
                <span>{competency.correct} acertos</span>
                <span>{competency.incorrect} revisões</span>
              </div>
              {competency.reinforcement && (
                <span className="pl-app-reinforcement">Reforço sugerido</span>
              )}
            </article>
          ))}
        </div>

        {reinforcementTopics.length > 0 && (
          <div className="pl-app-reinforcement-box">
            <AgentAvatar agent="analyst" size={40} />
            <div>
              <span className="pl-app-eyebrow">Analista de Progresso</span>
              <strong>Um ponto para revisar com calma.</strong>
              <p>
                Você encontrou dificuldade em{' '}
                {reinforcementTopics.map((item) => item.name.toLowerCase()).join(', ')}.
                Volte ao conteúdo da missão e tente novamente — errar faz parte
                do processo.
              </p>
            </div>
            <span className="pl-app-card-link">
              Revisar
              <ArrowRightIcon size={11} />
            </span>
          </div>
        )}
      </section>

      <section className="pl-app-section">
        <div className="pl-app-section-head">
          <div>
            <span className="pl-app-eyebrow">Conquistas</span>
            <h2>Marcos que contam sua história.</h2>
          </div>
        </div>
        <div className="pl-app-achievement-grid">
          {PREVIEW_ACHIEVEMENTS.map((achievement) => (
            <article className="pl-app-achievement-card" key={achievement.key}>
              <span className="pl-app-achievement-icon">
                <TrophyIcon size={17} />
              </span>
              <div>
                <span>Conquista</span>
                <h3>{achievement.name}</h3>
                <p>{achievement.date}</p>
              </div>
            </article>
          ))}
        </div>
      </section>
      </div>
    </AppShell>
  )
}
