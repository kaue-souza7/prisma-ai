import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { progressApi, usersApi } from '@/api'
import { ShieldIcon, SparkIcon, TrophyIcon } from '@/design-system/Icons'
import { useSessionStore } from '@/store/session'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import type { ProgressSummary, Trail } from '@/types/student'
import { AgentAvatar } from './components/StudentVisuals'
import { displayName } from './format'
import styles from './Profile.module.css'

const LEVEL_LABELS: Record<string, string> = {
  beginner: 'Estou começando',
  intermediate: 'Já tenho alguma base',
  advanced: 'Me sinto confiante',
}

export function ProfilePage() {
  useDocumentTitle('Meu perfil — Prisma.AI')
  const user = useSessionStore((state) => state.user)
  const profile = useSessionStore((state) => state.profile)
  const [summary, setSummary] = useState<ProgressSummary | null>(null)
  const [trail, setTrail] = useState<Trail | null>(null)
  const [trailLoading, setTrailLoading] = useState(false)
  const [trailError, setTrailError] = useState('')
  const initial = user?.email?.slice(0, 1).toUpperCase() ?? 'P'

  useEffect(() => {
    progressApi
      .getSummary()
      .then((response) => setSummary(response.data))
      .catch(() => setSummary(null))
    usersApi
      .getTrail()
      .then((response) => setTrail(response.data))
      .catch(() => setTrail(null))
  }, [])

  async function switchTrail(mode: 'personalized' | 'standard') {
    setTrailLoading(true)
    setTrailError('')
    try {
      const response = await usersApi.setTrailPreference(mode)
      setTrail(response.data)
    } catch {
      setTrailError('Não foi possível alterar sua trilha agora. Tente novamente.')
    } finally {
      setTrailLoading(false)
    }
  }

  return (
    <div className={`st-app-page ${styles.page}`}>
      <header className={styles.header}>
        <span className="st-eyebrow">Meu perfil</span>
        <h1>
          Seu espaço, <span>suas escolhas.</span>
        </h1>
        <p>
          Preferências, consentimento e o ponto de partida da sua jornada
          financeira.
        </p>
      </header>

      <section className={styles.identityCard}>
        <div className={styles.identityGlow} aria-hidden="true" />
        <div className={styles.avatarLarge} aria-hidden="true">{initial}</div>
        <div className={styles.identityCopy}>
          <span>Estudante</span>
          <h2>{displayName(user?.email)}</h2>
          <p>{user?.email}</p>
          {profile?.personal_goal && (
            <div className={styles.goal}>
              <SparkIcon size={14} />
              <span>{profile.personal_goal}</span>
            </div>
          )}
        </div>
        <div className={styles.identityStats}>
          <div>
            <strong>{summary?.level_name ?? '—'}</strong>
            <span>nível {summary?.level ?? '—'}</span>
          </div>
          <div>
            <strong>{summary?.total_points ?? '—'}</strong>
            <span>pontos</span>
          </div>
          <div>
            <strong>{summary?.missions_completed ?? '—'}</strong>
            <span>
              {summary?.missions_completed === 1 ? 'missão' : 'missões'}
            </span>
          </div>
        </div>
      </section>

      <div className={styles.grid}>
        <section className={styles.card}>
          <div className={styles.cardHead}>
            <span className={styles.cardIcon}><SparkIcon size={18} /></span>
            <div>
              <h2>Minha jornada</h2>
              <p>O contexto que orienta suas recomendações.</p>
            </div>
          </div>
          <dl className={styles.list}>
            <div>
              <dt>Objetivo pessoal</dt>
              <dd>{profile?.personal_goal || 'Ainda não informado'}</dd>
            </div>
            <div>
              <dt>Ponto de partida</dt>
              <dd>{LEVEL_LABELS[profile?.knowledge_level ?? ''] ?? 'Ainda não informado'}</dd>
            </div>
            <div>
              <dt>Onboarding</dt>
              <dd>
                <span className={profile?.onboarding_completed ? styles.ok : styles.pending}>
                  {profile?.onboarding_completed ? 'Concluído' : 'Pendente'}
                </span>
              </dd>
            </div>
          </dl>
          <Link to="/student/progress" className="st-link-arrow">
            Ver competências e conquistas
            <span aria-hidden="true">→</span>
          </Link>
        </section>

        <section className={`${styles.card} ${styles.trailCard}`}>
          <div className={styles.cardHead}>
            <span className={`${styles.cardIcon} ${styles.cardIconWarm}`}>
              <AgentAvatar agent="catalyst" size={30} />
            </span>
            <div>
              <h2>Minha trilha</h2>
              <p>A ordem das trilhas sugerida pelo Catalisador.</p>
            </div>
          </div>
          {trail ? (
            <>
              <p className={styles.trailRationale}>{trail.rationale}</p>
              <div className={styles.trailPath}>
                {trail.phases.map((phase, index) => (
                  <span key={phase.number} className={styles.trailStep}>
                    <small>{index + 1}</small>
                    {phase.name}
                  </span>
                ))}
              </div>
              <span className={styles.trailSource}>
                {trail.source === 'standard'
                  ? 'Ordem padrão'
                  : trail.source === 'ai'
                    ? 'Sugerida por IA'
                    : 'Personalizada por regras'}
              </span>
              <button
                type="button"
                className={styles.trailAction}
                onClick={() => switchTrail(trail.source === 'standard' ? 'personalized' : 'standard')}
                disabled={trailLoading}
              >
                {trailLoading
                  ? 'Alterando...'
                  : trail.source === 'standard'
                    ? 'Voltar à trilha personalizada'
                    : 'Usar a ordem padrão'}
              </button>
            </>
          ) : (
            <>
              <p className={styles.muted}>
                Você ainda não tem uma trilha personalizada. O Catalisador pode
                organizar as trilhas a partir do seu objetivo e nível.
              </p>
              <button
                type="button"
                className={styles.trailAction}
                onClick={() => switchTrail('personalized')}
                disabled={trailLoading}
              >
                {trailLoading ? 'Criando...' : 'Criar minha trilha personalizada'}
              </button>
            </>
          )}
          {trailError && <p className={styles.errorText} role="alert">{trailError}</p>}
        </section>

        <section className={styles.card}>
          <div className={styles.cardHead}>
            <span className={`${styles.cardIcon} ${styles.cardIconMint}`}>
              <ShieldIcon size={18} />
            </span>
            <div>
              <h2>Privacidade e consentimento</h2>
              <p>Você no controle dos seus dados.</p>
            </div>
          </div>
          <div className={styles.consentStatus}>
            <span className={profile?.consent_given ? styles.okDot : styles.pendingDot} />
            <div>
              <strong>
                {profile?.consent_given
                  ? 'Consentimento registrado'
                  : 'Consentimento pendente'}
              </strong>
              <p>
                Usamos seus dados apenas para personalizar a experiência
                educacional. Nenhum dado bancário é solicitado.
              </p>
            </div>
          </div>
          <p className={styles.legal}>
            A política de privacidade e os canais de revogação serão publicados
            antes do piloto. A base legal está em revisão jurídica.
          </p>
        </section>

        <section className={styles.agentCard}>
          <AgentAvatar agent="mentor" size={44} />
          <div>
            <h2>Precisa de ajuda?</h2>
            <p>
              O Mentor vai explicar conceitos e acompanhar seu raciocínio
              quando a integração de IA estiver disponível.
            </p>
          </div>
          <Link to="/student/mentor" className="st-link-arrow">
            Conhecer
          </Link>
        </section>

        <section className={styles.card}>
          <div className={styles.cardHead}>
            <span className={`${styles.cardIcon} ${styles.cardIconWarm}`}>
              <TrophyIcon size={18} />
            </span>
            <div>
              <h2>Conquistas</h2>
              <p>Seus marcos mais recentes.</p>
            </div>
          </div>
          {summary?.achievements.length ? (
            <ul className={styles.achievementList}>
              {summary.achievements.slice(0, 3).map((achievement) => (
                <li key={achievement.key}>
                  <span><TrophyIcon size={14} /></span>
                  <div>
                    <strong>{achievement.name}</strong>
                    <small>
                      {new Date(achievement.earned_at).toLocaleDateString('pt-BR')}
                    </small>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className={styles.muted}>
              Sua primeira conquista aparece depois do onboarding e da primeira
              missão.
            </p>
          )}
        </section>
      </div>
    </div>
  )
}
