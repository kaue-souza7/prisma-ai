import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { usersApi } from '@/api'
import { Button } from '@/design-system'
import { CheckIcon, ShieldIcon, SparkIcon } from '@/design-system/Icons'
import { useSessionStore } from '@/store/session'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import type { Trail } from '@/types/student'
import { BrandMark, PrismMascot } from './components/StudentVisuals'
import styles from './Onboarding.module.css'

const GOALS = [
  { value: 'primeiro_salario', label: 'Organizar meu primeiro salário' },
  { value: 'dividas', label: 'Sair das dívidas' },
  { value: 'reserva', label: 'Criar uma reserva para imprevistos' },
  { value: 'credito_juros', label: 'Entender crédito e juros' },
  { value: 'investimentos', label: 'Aprender a investir melhor' },
  { value: 'protecao_digital', label: 'Evitar golpes e proteger meus dados' },
  { value: 'outro', label: 'Outro objetivo' },
]

const KNOWLEDGE_LEVELS = [
  { value: 'beginner', label: 'Estou começando', hint: 'Quero aprender o básico com calma.' },
  { value: 'intermediate', label: 'Já tenho alguma base', hint: 'Conheço alguns conceitos, mas quero organizar melhor.' },
  { value: 'advanced', label: 'Me sinto confiante', hint: 'Quero aprofundar e revisar decisões.' },
]

const LIFE_CONTEXTS = [
  { value: 'primeiro_emprego', label: 'Estou no primeiro emprego' },
  { value: 'ja_trabalho', label: 'Já trabalho há um tempo' },
  { value: 'autonomo_freelancer', label: 'Trabalho por conta própria' },
  { value: 'estudante_sem_renda', label: 'Estudo e ainda não tenho renda' },
]

const URGENCIES = [
  { value: 'agora_preciso', label: 'Preciso resolver algo agora' },
  { value: 'aprendizado_continuo', label: 'Quero aprender com constância' },
]

const PACE_LABELS: Record<string, string> = {
  supported: 'No seu ritmo, com mais apoio',
  steady: 'Ritmo equilibrado',
  accelerated: 'Ritmo mais rápido',
}

const CONSENT_VERSION = '2026-10-21'

export function OnboardingPage() {
  useDocumentTitle('Onboarding — Prisma.AI')
  const navigate = useNavigate()
  const user = useSessionStore((state) => state.user)
  const profile = useSessionStore((state) => state.profile)
  const setProfile = useSessionStore((state) => state.setProfile)
  const [step, setStep] = useState(1)
  const [goalCategory, setGoalCategory] = useState('')
  const [customGoal, setCustomGoal] = useState('')
  const [knowledgeLevel, setKnowledgeLevel] = useState('')
  const [lifeContext, setLifeContext] = useState('')
  const [urgency, setUrgency] = useState('')
  const [consent, setConsent] = useState(false)
  const [trail, setTrail] = useState<Trail | null>(null)
  const [loading, setLoading] = useState(false)
  const [trailLoading, setTrailLoading] = useState(false)
  const [error, setError] = useState('')

  const personalGoal = goalCategory === 'outro' ? customGoal.trim() : (
    GOALS.find((goal) => goal.value === goalCategory)?.label ?? ''
  )

  function persistProfile(nextTrail: Trail | null) {
    setProfile({
      personal_goal: personalGoal,
      knowledge_level: knowledgeLevel,
      onboarding_completed: true,
      consent_given: true,
      preferences: {
        ...(profile?.preferences ?? {}),
        goal_category: goalCategory,
        life_context: lifeContext || null,
        urgency: urgency || null,
        onboarding_version: 2,
      },
      trail: nextTrail,
    })
  }

  async function handleSubmit() {
    if (!consent || !personalGoal || !knowledgeLevel) return
    setLoading(true)
    setError('')

    try {
      const response = await usersApi.completeOnboarding({
        personal_goal: personalGoal,
        knowledge_level: knowledgeLevel,
        consent_version: CONSENT_VERSION,
        life_context: lifeContext || null,
        urgency: urgency || null,
        preferences: {
          goal_category: goalCategory,
          life_context: lifeContext || null,
          urgency: urgency || null,
          onboarding_version: 2,
        },
      })

      const nextTrail = response.data.trail ?? null
      setTrail(nextTrail)
      persistProfile(nextTrail)
      setStep(4)
    } catch (err: unknown) {
      const apiError = err as { response?: { data?: { error?: { message?: string } } } }
      setError(
        apiError.response?.data?.error?.message ||
          'Não foi possível concluir seu onboarding. Tente novamente.',
      )
    } finally {
      setLoading(false)
    }
  }

  async function useStandardTrail() {
    setTrailLoading(true)
    setError('')
    try {
      const response = await usersApi.setTrailPreference('standard')
      setTrail(response.data)
      persistProfile(response.data)
    } catch {
      setError('Não foi possível alterar a trilha agora. Tente novamente.')
    } finally {
      setTrailLoading(false)
    }
  }

  return (
    <main className={`student-app ${styles.shell}`}>
      <aside className={styles.visualPanel}>
        <BrandMark />
        <div className={styles.visualCopy}>
          <span className={styles.visualEyebrow}>Bem-vindo ao seu espaço</span>
          <h2>Sua jornada começa com contexto.</h2>
          <p>
            Objetivo, ponto de partida e consentimento. Com isso, a experiência
            fica mais útil e respeitosa com o seu ritmo.
          </p>
        </div>
        <div className={styles.visualArt} aria-hidden="true">
          <span className={styles.visualOrb} />
          <PrismMascot size={250} />
        </div>
        <div className={styles.visualPoints}>
          <span><CheckIcon size={13} /> Sem dados bancários</span>
          <span><CheckIcon size={13} /> Você pode mudar depois</span>
          <span><CheckIcon size={13} /> Consentimento explícito</span>
        </div>
      </aside>

      <div className={styles.contentPanel}>
        <header className={styles.header}>
          <span className={styles.eyebrow}>Seu ponto de partida</span>
          <h1>Vamos personalizar sua jornada.</h1>
          <p>
            São poucos passos. Suas escolhas ajudam a montar uma trilha inicial e
            adaptar exemplos e recomendações — você pode mudar de ideia depois.
          </p>
          <ol className={styles.steps} aria-label="Etapas do onboarding">
            {[1, 2, 3, 4].map((item) => (
              <li
                key={item}
                className={[
                  styles.step,
                  step === item ? styles.stepActive : '',
                  step > item ? styles.stepDone : '',
                ].join(' ')}
                aria-current={step === item ? 'step' : undefined}
              >
                <span>{step > item ? <CheckIcon size={14} /> : item}</span>
                {item === 1
                  ? 'Boas-vindas'
                  : item === 2
                    ? 'Sobre você'
                    : item === 3
                      ? 'Consentimento'
                      : 'Sua trilha'}
              </li>
            ))}
          </ol>
        </header>

        <section className={styles.card}>
          {step === 1 && (
            <div className={styles.stepContent}>
              <span className={styles.iconBadge} aria-hidden="true">
                <SparkIcon size={24} />
              </span>
              <h2>Um espaço para aprender fazendo</h2>
              <p>
                Aqui você vai resolver situações do dia a dia, receber feedback e
                revisar conceitos no seu ritmo. O Mentor é um assistente
                educacional: ele ajuda a pensar, mas não toma decisões financeiras
                por você.
              </p>
              <ul className={styles.plainList}>
                <li>Sem ranking público e sem cobrança para aprender.</li>
                <li>Nenhum dado bancário é solicitado.</li>
                <li>Seu progresso fica salvo para continuar depois.</li>
              </ul>
              <Button fullWidth onClick={() => setStep(2)}>
                Começar
              </Button>
            </div>
          )}

          {step === 2 && (
            <div className={styles.stepContent}>
              <h2>O que você quer entender melhor?</h2>
              <p className={styles.muted}>
                Escolha o objetivo que mais combina com o seu momento.
                {user?.email ? ` Sua conta: ${user.email}.` : ''}
              </p>

              <div className={styles.goalGrid} role="radiogroup" aria-label="Objetivo principal">
                {GOALS.map((goal) => (
                  <label
                    key={goal.value}
                    className={[
                      styles.goalOption,
                      goalCategory === goal.value ? styles.optionSelected : '',
                    ].join(' ')}
                  >
                    <input
                      type="radio"
                      name="goal"
                      value={goal.value}
                      checked={goalCategory === goal.value}
                      onChange={() => setGoalCategory(goal.value)}
                    />
                    <span>{goal.label}</span>
                  </label>
                ))}
              </div>

              {goalCategory === 'outro' && (
                <label className={styles.field}>
                  <span>Qual é o seu objetivo?</span>
                  <input
                    value={customGoal}
                    onChange={(event) => setCustomGoal(event.target.value)}
                    maxLength={200}
                    placeholder="Ex.: organizar o dinheiro do meu primeiro emprego"
                  />
                </label>
              )}

              <h2 className={styles.secondHeading}>Como você se sente hoje?</h2>
              <div className={styles.levelGrid} role="radiogroup" aria-label="Nível de conhecimento">
                {KNOWLEDGE_LEVELS.map((level) => (
                  <label
                    key={level.value}
                    className={[
                      styles.levelOption,
                      knowledgeLevel === level.value ? styles.optionSelected : '',
                    ].join(' ')}
                  >
                    <input
                      type="radio"
                      name="knowledge"
                      value={level.value}
                      checked={knowledgeLevel === level.value}
                      onChange={() => setKnowledgeLevel(level.value)}
                    />
                    <strong>{level.label}</strong>
                    <small>{level.hint}</small>
                  </label>
                ))}
              </div>

              <h2 className={styles.secondHeading}>Qual é o seu momento?</h2>
              <p className={styles.muted}>
                Isso ajuda o Catalisador a escolher o ponto de partida. É opcional.
              </p>
              <div className={styles.compactGrid} role="radiogroup" aria-label="Contexto de vida">
                {LIFE_CONTEXTS.map((context) => (
                  <label
                    key={context.value}
                    className={[
                      styles.compactOption,
                      lifeContext === context.value ? styles.optionSelected : '',
                    ].join(' ')}
                  >
                    <input
                      type="radio"
                      name="life_context"
                      value={context.value}
                      checked={lifeContext === context.value}
                      onChange={() => setLifeContext(context.value)}
                    />
                    <span>{context.label}</span>
                  </label>
                ))}
              </div>

              <h2 className={styles.secondHeading}>Qual é a sua urgência?</h2>
              <div className={styles.compactGrid} role="radiogroup" aria-label="Urgência">
                {URGENCIES.map((item) => (
                  <label
                    key={item.value}
                    className={[
                      styles.compactOption,
                      urgency === item.value ? styles.optionSelected : '',
                    ].join(' ')}
                  >
                    <input
                      type="radio"
                      name="urgency"
                      value={item.value}
                      checked={urgency === item.value}
                      onChange={() => setUrgency(item.value)}
                    />
                    <span>{item.label}</span>
                  </label>
                ))}
              </div>

              <div className={styles.actions}>
                <Button variant="ghost" onClick={() => setStep(1)}>
                  Voltar
                </Button>
                <Button
                  onClick={() => setStep(3)}
                  disabled={!personalGoal || !knowledgeLevel}
                >
                  Continuar
                </Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className={styles.stepContent}>
              <span className={styles.iconBadge} aria-hidden="true">
                <ShieldIcon size={24} />
              </span>
              <h2>Seus dados, suas escolhas</h2>
              <p>
                Usamos seu objetivo, seu nível de conhecimento e seu progresso para
                personalizar a experiência e calcular conquistas. Não vendemos
                dados e não pedimos informações bancárias.
              </p>

              <div className={styles.consentBox}>
                <label className={styles.consentLabel}>
                  <input
                    type="checkbox"
                    checked={consent}
                    onChange={(event) => setConsent(event.target.checked)}
                  />
                  <span>
                    Li e concordo com o tratamento dos meus dados para esta
                    finalidade educacional, conforme a política de privacidade.
                    Posso revogar o consentimento pelos canais de atendimento.
                  </span>
                </label>
              </div>

              <p className={styles.legalNote}>
                Versão do consentimento: {CONSENT_VERSION}. A base legal e os
                prazos de retenção estão em revisão jurídica antes do lançamento
                do piloto.
              </p>

              {error && (
                <p className={styles.error} role="alert">
                  {error}
                </p>
              )}

              <div className={styles.actions}>
                <Button variant="ghost" onClick={() => setStep(2)} disabled={loading}>
                  Voltar
                </Button>
                <Button onClick={handleSubmit} disabled={!consent} loading={loading}>
                  Montar minha trilha
                </Button>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className={styles.stepContent}>
              <span className={styles.iconBadge} aria-hidden="true">
                <SparkIcon size={24} />
              </span>
              <h2>Sua trilha inicial está pronta.</h2>
              <p className={styles.muted}>
                O Catalisador organizou as trilhas a partir do seu objetivo. Você
                pode seguir esta sugestão ou usar a ordem padrão.
              </p>

              {trail ? (
                <>
                  <div className={styles.trailSummary}>
                    <p>{trail.rationale}</p>
                    <div className={styles.trailMeta}>
                      <span>{PACE_LABELS[trail.pace] ?? 'Ritmo equilibrado'}</span>
                      <span>{trail.focus_areas.slice(0, 2).join(' · ')}</span>
                    </div>
                  </div>

                  <ol className={styles.trailList} aria-label="Ordem sugerida das trilhas">
                    {trail.phases.map((phase, index) => (
                      <li key={phase.number}>
                        <span className={styles.trailPosition}>{index + 1}</span>
                        <div>
                          <strong>
                            Trilha {phase.number} · {phase.name}
                          </strong>
                          {phase.description && <small>{phase.description}</small>}
                        </div>
                        {index === 0 && (
                          <span className={styles.trailStart}>Começa aqui</span>
                        )}
                      </li>
                    ))}
                  </ol>

                  {trail.source !== 'standard' && (
                    <button
                      type="button"
                      className={styles.textAction}
                      onClick={useStandardTrail}
                      disabled={trailLoading}
                    >
                      {trailLoading ? 'Alterando...' : 'Prefiro a ordem padrão das trilhas'}
                    </button>
                  )}
                </>
              ) : (
                <p className={styles.muted}>
                  Sua trilha será exibida na jornada. Você pode ajustá-la depois no
                  seu perfil.
                </p>
              )}

              {error && (
                <p className={styles.error} role="alert">
                  {error}
                </p>
              )}

              <div className={styles.actions}>
                <Button variant="ghost" onClick={() => setStep(3)}>
                  Voltar
                </Button>
                <Button onClick={() => navigate('/student', { replace: true })}>
                  Começar jornada
                </Button>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  )
}
