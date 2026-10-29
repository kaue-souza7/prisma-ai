import { useEffect, useRef, useState } from 'react'
import type { KeyboardEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { usersApi } from '@/api'
import { Button } from '@/design-system'
import { CheckIcon, ShieldIcon, SparkIcon } from '@/design-system/Icons'
import { useSessionStore } from '@/store/session'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import type { Trail } from '@/types/student'
import { Mascot3D } from '@/features/mascots/Mascot3D'
import { BrandMark } from './components/StudentVisuals'
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

const INCOME_PATTERNS = [
  { value: 'sem_renda', label: 'Ainda não tenho renda' },
  { value: 'variavel', label: 'Minha renda varia bastante' },
  { value: 'fixa', label: 'Tenho uma renda fixa' },
  { value: 'prefiro_nao_dizer', label: 'Prefiro não dizer' },
]

const MAIN_DIFFICULTIES = [
  { value: 'dividas', label: 'Sair das dívidas' },
  { value: 'reserva', label: 'Montar uma reserva' },
  { value: 'gastos', label: 'Controlar os gastos' },
  { value: 'investir', label: 'Começar a investir' },
  { value: 'golpes', label: 'Me proteger de golpes' },
  { value: 'outro', label: 'Outra dificuldade' },
]

const LEARNING_STYLES = [
  { value: 'exemplos', label: 'Exemplos práticos do dia a dia' },
  { value: 'passo_a_passo', label: 'Passo a passo detalhado' },
  { value: 'desafios', label: 'Desafios rápidos' },
]

const PACE_LABELS: Record<string, string> = {
  supported: 'No seu ritmo, com mais apoio',
  steady: 'Ritmo equilibrado',
  accelerated: 'Ritmo mais rápido',
}

const MODE_LABELS: Record<string, string> = {
  express: 'Expresso',
  standard: 'Padrão',
  full: 'Completo',
}

const CONSENT_VERSION = '2026-10-21'

type ChatMessage = { role: 'assistant' | 'user'; content: string }

type QuestionOption = { value: string; label: string; hint?: string }

type FixedQuestion = {
  id: string
  prompt: string
  kind: 'single' | 'text'
  options?: QuestionOption[]
  placeholder?: string
  optional?: boolean
}

const ACKNOWLEDGMENTS: Record<string, string> = {
  goal_category: 'Ótimo, esse é um ponto de partida importante.',
  goal_detail: 'Que legal, isso ajuda a personalizar sua trilha.',
  life_context: 'Entendi, isso muda o ponto de partida da jornada.',
  work_experience: 'Boa, obrigado por compartilhar.',
  income_pattern: 'Entendi, isso ajuda a ajustar o ritmo dos exemplos.',
  main_difficulty: 'Obrigado por confiar; vamos focar nisso.',
  urgency: 'Entendi a sua prioridade.',
  knowledge_level: 'Perfeito, vamos respeitar o seu ritmo.',
  learning_style: 'Boa, vou usar esse estilo nos exemplos.',
  goal_12m: 'Adorei a meta! Vamos construir o caminho.',
}

// D-C1: 10 perguntas fixas para todos os usuários.
const FIXED_QUESTIONS: FixedQuestion[] = [
  {
    id: 'goal_category',
    prompt: 'Qual é o seu objetivo principal hoje?',
    kind: 'single',
    options: GOALS,
  },
  {
    id: 'goal_detail',
    prompt:
      'Me conta em uma frase: o que mudaria na sua vida se você dominasse suas finanças?',
    kind: 'text',
    placeholder: 'Ex.: conseguir sair das dívidas e guardar dinheiro todo mês.',
  },
  {
    id: 'life_context',
    prompt: 'Como está sua situação de trabalho hoje?',
    kind: 'single',
    options: LIFE_CONTEXTS,
  },
  {
    id: 'work_experience',
    prompt: 'Há quanto tempo você trabalha com carteira assinada?',
    kind: 'text',
    placeholder: 'Ex.: 3 anos. Se não se aplicar, pode pular.',
    optional: true,
  },
  {
    id: 'income_pattern',
    prompt: 'Como você descreveria sua renda hoje?',
    kind: 'single',
    options: INCOME_PATTERNS,
  },
  {
    id: 'main_difficulty',
    prompt: 'Qual é a sua maior dificuldade com dinheiro?',
    kind: 'single',
    options: MAIN_DIFFICULTIES,
  },
  {
    id: 'urgency',
    prompt: 'O que você precisa resolver primeiro?',
    kind: 'single',
    options: URGENCIES,
  },
  {
    id: 'knowledge_level',
    prompt: 'Como você se sente em relação a conceitos financeiros?',
    kind: 'single',
    options: KNOWLEDGE_LEVELS,
  },
  {
    id: 'learning_style',
    prompt: 'Como você prefere aprender?',
    kind: 'single',
    options: LEARNING_STYLES,
  },
  {
    id: 'goal_12m',
    prompt: 'Qual é o seu maior sonho financeiro para os próximos 12 meses?',
    kind: 'text',
    placeholder: 'Ex.: montar uma reserva de R$ 5.000.',
  },
]

function labelFor(options: QuestionOption[] | undefined, value: string) {
  return options?.find((option) => option.value === value)?.label ?? value
}

export function OnboardingPage() {
  useDocumentTitle('Onboarding — Prisma.AI')
  const navigate = useNavigate()
  const user = useSessionStore((state) => state.user)
  const profile = useSessionStore((state) => state.profile)
  const setProfile = useSessionStore((state) => state.setProfile)

  const [step, setStep] = useState(1)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [fixedIndex, setFixedIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [adaptiveQuestions, setAdaptiveQuestions] = useState<string[]>([])
  const [adaptiveIndex, setAdaptiveIndex] = useState(0)
  const [adaptiveLoading, setAdaptiveLoading] = useState(false)
  const [textAnswer, setTextAnswer] = useState('')
  const [consent, setConsent] = useState(false)
  const [trail, setTrail] = useState<Trail | null>(null)
  const [catalystAnimation, setCatalystAnimation] = useState('C-01')
  const [loading, setLoading] = useState(false)
  const [trailLoading, setTrailLoading] = useState(false)
  const [error, setError] = useState('')

  const goalCategory = answers.goal_category ?? ''
  const knowledgeLevel = answers.knowledge_level ?? ''
  const lifeContext = answers.life_context ?? ''
  const urgency = answers.urgency ?? ''
  const goalDetail = answers.goal_detail?.trim() ?? ''
  const personalGoal =
    goalCategory === 'outro'
      ? goalDetail || 'Meu objetivo financeiro'
      : labelFor(GOALS, goalCategory) || goalDetail

  const currentQuestion =
    fixedIndex < FIXED_QUESTIONS.length ? FIXED_QUESTIONS[fixedIndex] : null
  const currentPrompt =
    currentQuestion?.id === 'goal_detail' && goalCategory === 'outro'
      ? 'Qual é o seu objetivo? Descreva com suas palavras.'
      : currentQuestion?.prompt ?? ''
  const adaptiveQuestion =
    adaptiveIndex < adaptiveQuestions.length
      ? adaptiveQuestions[adaptiveIndex]
      : null
  const conversationDone =
    fixedIndex >= FIXED_QUESTIONS.length &&
    !adaptiveLoading &&
    adaptiveIndex >= adaptiveQuestions.length
  const chatRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight
    }
  }, [messages, currentPrompt, adaptiveQuestion, adaptiveLoading, conversationDone])

  useEffect(() => {
    if (step === 1) setCatalystAnimation('C-01')
    else if (step === 2 || step === 3) setCatalystAnimation('C-03')
    else setCatalystAnimation('C-05')
  }, [step])

  useEffect(() => {
    if (step !== 2 || messages.length === 0) return
    setCatalystAnimation('C-04')
    const timer = window.setTimeout(() => setCatalystAnimation('C-03'), 1100)
    return () => window.clearTimeout(timer)
  }, [messages.length, step])

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
        onboarding_version: 3,
        fixed_answers: { ...answers },
      },
      trail: nextTrail,
    })
  }

  async function loadAdaptiveQuestions(
    fixedAnswers: Record<string, string>,
    history: ChatMessage[],
  ) {
    setAdaptiveLoading(true)
    setError('')
    try {
      const response = await usersApi.getAdaptiveQuestions({
        fixed_answers: {
          ...fixedAnswers,
          objetivo: fixedAnswers.goal_category ?? '',
          goal_category: fixedAnswers.goal_category ?? '',
          knowledge_level_declared: fixedAnswers.knowledge_level ?? '',
        },
        conversation_history: history,
      })
      setAdaptiveQuestions(response.data.questions ?? [])
    } catch {
      // O onboarding continua mesmo sem perguntas adaptativas.
      setAdaptiveQuestions([])
    } finally {
      setAdaptiveLoading(false)
    }
  }

  function commitFixedAnswer(value: string, label: string) {
    if (!currentQuestion) return
    const nextAnswers = { ...answers, [currentQuestion.id]: value }
    const nextMessages: ChatMessage[] = [
      ...messages,
      { role: 'assistant', content: currentPrompt },
      { role: 'user', content: label },
      {
        role: 'assistant',
        content:
          ACKNOWLEDGMENTS[currentQuestion.id] ?? 'Obrigado por compartilhar.',
      },
    ]
    const nextIndex = fixedIndex + 1

    setAnswers(nextAnswers)
    setMessages(nextMessages)
    setTextAnswer('')
    setFixedIndex(nextIndex)

    if (nextIndex >= FIXED_QUESTIONS.length) {
      void loadAdaptiveQuestions(nextAnswers, nextMessages)
    }
  }

  function handleFixedSingle(option: QuestionOption) {
    commitFixedAnswer(option.value, option.label)
  }

  function handleFixedText() {
    if (!currentQuestion || currentQuestion.kind !== 'text') return
    const answer = textAnswer.trim()
    if (!answer && !currentQuestion.optional) return
    commitFixedAnswer(answer, answer || 'Prefiro não responder')
  }

  function handleAdaptiveSend() {
    if (!adaptiveQuestion || !textAnswer.trim()) return
    setMessages((current) => [
      ...current,
      { role: 'assistant', content: adaptiveQuestion },
      { role: 'user', content: textAnswer.trim() },
      { role: 'assistant', content: 'Obrigado, isso ajuda muito.' },
    ])
    setAdaptiveIndex((current) => current + 1)
    setTextAnswer('')
  }

  function skipAdaptiveQuestion() {
    if (!adaptiveQuestion) return
    setMessages((current) => [
      ...current,
      { role: 'assistant', content: adaptiveQuestion },
      { role: 'user', content: 'Prefiro não responder esta pergunta.' },
      { role: 'assistant', content: 'Tudo bem, obrigado por avisar.' },
    ])
    setAdaptiveIndex((current) => current + 1)
    setTextAnswer('')
  }

  function skipAdaptiveStage() {
    setAdaptiveIndex(adaptiveQuestions.length)
    setTextAnswer('')
  }

  function handleKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key !== 'Enter') return
    event.preventDefault()
    if (currentQuestion) handleFixedText()
    else if (adaptiveQuestion) handleAdaptiveSend()
  }

  async function handleSubmit() {
    if (!consent || !personalGoal || !knowledgeLevel) return
    setLoading(true)
    setError('')

    try {
      const fixedAnswers = {
        ...answers,
        objetivo: goalCategory,
        goal_category: goalCategory,
        knowledge_level_declared: knowledgeLevel,
      }
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
          onboarding_version: 3,
          fixed_answers: fixedAnswers,
        },
        fixed_answers: fixedAnswers,
        conversation_history: messages,
      })

      const nextTrail = response.data.trail ?? null
      setTrail(nextTrail)
      persistProfile(nextTrail)
      setStep(4)
    } catch (err: unknown) {
      const apiError = err as {
        response?: { data?: { error?: { message?: string } } }
      }
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
          <Mascot3D agent="catalyst" animation={catalystAnimation} size={250} />
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
                    ? 'Conversa'
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
              <h2>Vamos conversar.</h2>
              <p className={styles.muted}>
                São 10 perguntas rápidas e, depois, algumas perguntas adaptativas
                para o Catalisador entender o seu momento.
                {user?.email ? ` Sua conta: ${user.email}.` : ''}
              </p>

              <div ref={chatRef} className={styles.chat} aria-live="polite">
                <div className={`${styles.chatMessage} ${styles.chatAssistant}`}>
                  <strong>Catalisador</strong>
                  <span>
                    Oi! Vou te fazer algumas perguntas para montar uma trilha que
                    faça sentido para você. Não existe resposta certa.
                  </span>
                </div>

                {messages.map((message, index) => (
                  <div
                    key={`${message.role}-${index}`}
                    className={[
                      styles.chatMessage,
                      message.role === 'assistant'
                        ? styles.chatAssistant
                        : styles.chatUser,
                    ].join(' ')}
                  >
                    <strong>
                      {message.role === 'assistant' ? 'Catalisador' : 'Você'}
                    </strong>
                    <span>{message.content}</span>
                  </div>
                ))}

                {currentQuestion && (
                  <div className={`${styles.chatMessage} ${styles.chatAssistant}`}>
                    <strong>Catalisador</strong>
                    <span>{currentPrompt}</span>
                  </div>
                )}

                {adaptiveLoading && (
                  <div className={`${styles.chatMessage} ${styles.chatAssistant}`}>
                    <strong>Catalisador</strong>
                    <span>
                      Só um instante — estou preparando algumas perguntas a partir
                      das suas respostas.
                    </span>
                  </div>
                )}

                {!adaptiveLoading && adaptiveQuestion && (
                  <div className={`${styles.chatMessage} ${styles.chatAssistant}`}>
                    <strong>Catalisador</strong>
                    <span>{adaptiveQuestion}</span>
                  </div>
                )}

                {conversationDone && (
                  <div className={`${styles.chatMessage} ${styles.chatAssistant}`}>
                    <strong>Catalisador</strong>
                    <span>
                      Obrigado! Com isso consigo montar uma trilha com a sua cara.
                    </span>
                  </div>
                )}
              </div>

              {currentQuestion?.kind === 'single' && (
                <div className={styles.chatOptions}>
                  {currentQuestion.options?.map((option) => (
                    <button
                      key={option.value}
                      type="button"
                      className={styles.chatOption}
                      onClick={() => handleFixedSingle(option)}
                    >
                      <strong>{option.label}</strong>
                      {option.hint && <small>{option.hint}</small>}
                    </button>
                  ))}
                </div>
              )}

              {currentQuestion?.kind === 'text' && (
                <>
                  <div className={styles.chatComposer}>
                    <input
                      value={textAnswer}
                      onChange={(event) => setTextAnswer(event.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder={currentQuestion.placeholder}
                      aria-label="Sua resposta ao Catalisador"
                    />
                    <Button
                      onClick={handleFixedText}
                      disabled={!textAnswer.trim() && !currentQuestion.optional}
                    >
                      Enviar
                    </Button>
                  </div>
                  {currentQuestion.optional && (
                    <button
                      type="button"
                      className={styles.textAction}
                      onClick={() => commitFixedAnswer('', 'Prefiro não responder')}
                    >
                      Pular esta pergunta
                    </button>
                  )}
                </>
              )}

              {!currentQuestion && !adaptiveLoading && adaptiveQuestion && (
                <>
                  <div className={styles.chatComposer}>
                    <input
                      value={textAnswer}
                      onChange={(event) => setTextAnswer(event.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder="Escreva sua resposta..."
                      aria-label="Sua resposta ao Catalisador"
                    />
                    <Button onClick={handleAdaptiveSend} disabled={!textAnswer.trim()}>
                      Enviar
                    </Button>
                  </div>
                  <div className={styles.chatSkips}>
                    <button
                      type="button"
                      className={styles.textAction}
                      onClick={skipAdaptiveQuestion}
                    >
                      Pular esta pergunta
                    </button>
                    <button
                      type="button"
                      className={styles.textAction}
                      onClick={skipAdaptiveStage}
                    >
                      Pular perguntas adaptativas
                    </button>
                  </div>
                </>
              )}

              {conversationDone && (
                <div className={styles.actions}>
                  <Button variant="ghost" onClick={() => setStep(1)}>
                    Voltar
                  </Button>
                  <Button onClick={() => setStep(3)}>Continuar</Button>
                </div>
              )}

              {error && (
                <p className={styles.error} role="alert">
                  {error}
                </p>
              )}
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
                  {trail.next_message && (
                    <p className={styles.catalystMessage}>{trail.next_message}</p>
                  )}
                  {trail.trail_1_auto_concluded && (
                    <span className={styles.autoBadge}>
                      Trilha 1 dominada no onboarding · +50 XP
                    </span>
                  )}
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
                          {trail.trail_modes?.[String(phase.number)] && (
                            <small>
                              Modo{' '}
                              {MODE_LABELS[trail.trail_modes[String(phase.number)]] ??
                                trail.trail_modes[String(phase.number)]}
                            </small>
                          )}
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
