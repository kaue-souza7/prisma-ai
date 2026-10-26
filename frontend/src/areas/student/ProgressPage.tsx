import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { progressApi } from '@/api'
import { Button } from '@/design-system'
import {
  ArrowRightIcon,
  CheckIcon,
  SparkIcon,
  TrophyIcon,
} from '@/design-system/Icons'
import type { ProgressSummary } from '@/types/student'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import { AgentAvatar, ProgressRing } from './components/StudentVisuals'
import { pluralize } from './format'
import styles from './Progress.module.css'

const COMPETENCY_LABELS = {
  not_started: 'Ainda não iniciada',
  developing: 'Em desenvolvimento',
  demonstrated: 'Demonstrada',
} as const

export function ProgressPage() {
  useDocumentTitle('Conquistas e progresso — Prisma.AI')
  const [summary, setSummary] = useState<ProgressSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    setLoading(true)
    setError('')
    progressApi
      .getSummary()
      .then((response) => setSummary(response.data))
      .catch(() => setError('Não foi possível carregar seu progresso. Tente novamente.'))
      .finally(() => setLoading(false))
  }, [reloadKey])

  if (loading) {
    return (
      <div className={`st-app-page ${styles.loadingPage}`}>
        <div className={`st-skeleton ${styles.loadingHero}`} />
        <div className={styles.loadingGrid}>
          <div className="st-skeleton" />
          <div className="st-skeleton" />
          <div className="st-skeleton" />
        </div>
      </div>
    )
  }

  if (error || !summary) {
    return (
      <div className={`st-app-page ${styles.errorPage}`}>
        <div className={styles.errorCard} role="alert">
          <h1>Seu progresso não carregou.</h1>
          <p>{error || 'Tente novamente em instantes.'}</p>
          <Button onClick={() => setReloadKey((value) => value + 1)}>
            Tentar novamente
          </Button>
        </div>
      </div>
    )
  }

  const hasNextLevel = summary.next_level_points !== null
  const range = hasNextLevel
    ? Math.max(summary.next_level_points! - summary.current_level_points, 1)
    : 1
  const progressPercent = hasNextLevel
    ? Math.min(
        100,
        Math.max(
          0,
          ((summary.total_points - summary.current_level_points) / range) * 100,
        ),
      )
    : 100
  const reinforcementTopics = summary.competencies.filter(
    (competency) => competency.reinforcement_suggested,
  )
  const demonstrated = summary.competencies.filter(
    (competency) => competency.status === 'demonstrated',
  ).length

  return (
    <div className={`st-app-page ${styles.page}`}>
      <header className={styles.header}>
        <div>
          <span className="st-eyebrow">Conquistas e progresso</span>
          <h1>
            Seu aprendizado em <span>evidências.</span>
          </h1>
          <p>
            Pontos mostram constância. As competências mostram o que você já
            consegue fazer com o conhecimento.
          </p>
        </div>
        <Link to="/student/journey" className={styles.headerAction}>
          Continuar jornada
          <ArrowRightIcon size={15} />
        </Link>
      </header>

      <section className={styles.heroGrid} aria-label="Nível e resumo">
        <article className={styles.levelCard}>
          <div className={styles.levelGlow} aria-hidden="true" />
          <div className={styles.levelCopy}>
            <span className={styles.levelKicker}>Seu nível atual</span>
            <h2>{summary.level_name}</h2>
            <p>Nível {summary.level} de 5</p>
            <div className={styles.levelPoints}>
              <strong>{summary.total_points}</strong>
              <span>pontos acumulados</span>
            </div>
            <div className={styles.levelTrack}>
              <span style={{ width: `${progressPercent}%` }} />
            </div>
            <p className={styles.levelHint}>
              {hasNextLevel
                ? `Faltam ${summary.next_level_points! - summary.total_points} pontos para o próximo nível.`
                : 'Você chegou ao nível máximo desta jornada.'}
            </p>
          </div>
          <div className={styles.levelRing}>
            <ProgressRing value={progressPercent} size={152} stroke={12}>
              <strong>{Math.round(progressPercent)}%</strong>
              <small>até o próximo</small>
            </ProgressRing>
          </div>
        </article>

        <div className={styles.statsColumn}>
          <div className={styles.statCard}>
            <span className={styles.statIcon}><CheckIcon size={17} /></span>
            <strong>{summary.missions_completed}</strong>
            <span>{pluralize(summary.missions_completed, 'missão concluída', 'missões concluídas')}</span>
          </div>
          <div className={styles.statCard}>
            <span className={styles.statIcon}><SparkIcon size={17} /></span>
            <strong>{demonstrated}</strong>
            <span>{pluralize(demonstrated, 'competência demonstrada', 'competências demonstradas')}</span>
          </div>
          <div className={styles.statCard}>
            <span className={styles.statIcon}><TrophyIcon size={17} /></span>
            <strong>{summary.achievements.length}</strong>
            <span>{pluralize(summary.achievements.length, 'conquista', 'conquistas')}</span>
          </div>
          <Link to="/student/studio" className={`${styles.statCard} ${styles.coinCard}`}>
            <span className={`${styles.statIcon} ${styles.coinIcon}`} aria-hidden="true">◆</span>
            <strong>{summary.coins ?? 0}</strong>
            <span>Prismas · Ir para o Estúdio</span>
          </Link>
        </div>
      </section>

      {summary.analyst_insight && (
        <section
          className={[
            styles.analystInsight,
            summary.analyst_insight.severity === 'attention'
              ? styles.insightAttention
              : summary.analyst_insight.severity === 'positive'
                ? styles.insightPositive
                : '',
          ].join(' ')}
          aria-label="Recomendação do Analista de Progresso"
        >
          <AgentAvatar agent="analyst" size={44} />
          <div>
            <span className="st-eyebrow">Analista de Progresso</span>
            <strong>
              {summary.analyst_insight.severity === 'attention'
                ? 'Um ponto para revisar com calma.'
                : summary.analyst_insight.severity === 'positive'
                  ? 'Seu aprendizado está deixando evidências.'
                  : 'Continue construindo suas evidências.'}
            </strong>
            <p>{summary.analyst_insight.message}</p>
          </div>
          <Link to="/student/journey" className="st-link-arrow">
            {summary.analyst_insight.action === 'review' ? 'Revisar' : 'Continuar'}
            <ArrowRightIcon size={13} />
          </Link>
        </section>
      )}

      <section className={styles.section} aria-labelledby="competencies-title">
        <div className="st-section-heading">
          <div>
            <span className="st-eyebrow">Competências</span>
            <h2 id="competencies-title">O que você já demonstra.</h2>
            <p>Evidências acumuladas a partir das suas respostas.</p>
          </div>
          <span className="st-chip st-chip--mint">
            {pluralize(demonstrated, 'competência demonstrada', 'competências demonstradas')}
          </span>
        </div>

        {summary.competencies.length === 0 ? (
          <div className={styles.empty}>
            <span aria-hidden="true"><SparkIcon size={22} /></span>
            <div>
              <strong>Suas competências começam na primeira missão.</strong>
              <p>Responda às atividades para construir evidências de aprendizagem.</p>
            </div>
            <Link to="/student/journey" className="st-link-arrow">
              Ir para a jornada
              <ArrowRightIcon size={13} />
            </Link>
          </div>
        ) : (
          <div className={styles.competencyGrid}>
            {summary.competencies.map((competency) => (
              <article
                key={competency.code ?? competency.name}
                className={[
                  styles.competencyCard,
                  styles[`competency_${competency.status}`],
                ].join(' ')}
              >
                <div className={styles.competencyTop}>
                  <span className={styles.competencyCode}>{competency.code}</span>
                  <span className={styles.competencyStatus}>
                    {COMPETENCY_LABELS[competency.status]}
                  </span>
                </div>
                <h3>{competency.name}</h3>
                <div className={styles.competencyMeta}>
                  <span>{pluralize(competency.correct_count, 'acerto', 'acertos')}</span>
                  <span>{pluralize(competency.incorrect_count, 'revisão', 'revisões')}</span>
                </div>
                {competency.reinforcement_suggested && (
                  <span className={styles.reinforcement}>Reforço sugerido</span>
                )}
              </article>
            ))}
          </div>
        )}

        {!summary.analyst_insight && reinforcementTopics.length > 0 && (
          <div className={styles.reinforcementBox}>
            <AgentAvatar agent="analyst" size={44} />
            <div>
              <span className="st-eyebrow">Analista de Progresso</span>
              <strong>Um ponto para revisar com calma.</strong>
              <p>
                Você encontrou dificuldade em{' '}
                {reinforcementTopics.map((item) => item.name).join(', ')}. Volte
                ao conteúdo da missão e tente novamente — errar faz parte do
                processo.
              </p>
            </div>
            <Link to="/student/journey" className="st-link-arrow">
              Revisar
              <ArrowRightIcon size={13} />
            </Link>
          </div>
        )}
      </section>

      <section className={styles.section} aria-labelledby="achievements-title">
        <div className="st-section-heading">
          <div>
            <span className="st-eyebrow">Conquistas</span>
            <h2 id="achievements-title">Marcos que contam sua história.</h2>
          </div>
        </div>

        {summary.achievements.length === 0 ? (
          <div className={styles.empty}>
            <span aria-hidden="true"><TrophyIcon size={22} /></span>
            <div>
              <strong>Ainda não há conquistas.</strong>
              <p>Conclua o onboarding e sua primeira missão para começar.</p>
            </div>
          </div>
        ) : (
          <div className={styles.achievementGrid}>
            {summary.achievements.map((achievement) => (
              <article key={achievement.key} className={styles.achievementCard}>
                <span className={styles.achievementIcon} aria-hidden="true">
                  <TrophyIcon size={20} />
                </span>
                <div>
                  <span>Conquista</span>
                  <h3>{achievement.name}</h3>
                  <p>
                    {new Date(achievement.earned_at).toLocaleDateString('pt-BR', {
                      day: '2-digit',
                      month: 'long',
                      year: 'numeric',
                    })}
                  </p>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
