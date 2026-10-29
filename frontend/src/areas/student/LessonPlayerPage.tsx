import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { journeyApi } from '@/api'
import { Button } from '@/design-system'
import {
  ArrowLeftIcon,
  ArrowRightIcon,
  ChatIcon,
  CheckIcon,
  CloseIcon,
  LockIcon,
  SparkIcon,
  TrophyIcon,
  VolumeIcon,
  VolumeOffIcon,
} from '@/design-system/Icons'
import { RichText } from '@/shared/RichText'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import { useLearningEffects } from '@/shared/useLearningEffects'
import { useSessionStore } from '@/store/session'
import type {
  Activity,
  AgentInsight,
  CatalystRecommendation,
  Lesson,
  LessonStep,
} from '@/types/student'
import { Mascot3D } from '@/features/mascots/Mascot3D'
import { AGENT_META, AgentAvatar } from './components/StudentVisuals'
import { MentorChat } from './components/MentorChat'
import styles from './LessonPlayer.module.css'

interface SubmitResult {
  is_correct: boolean | null
  correct_answer?: string | null
  score: number
  feedback: string
  feedback_agent?: 'mentor' | 'analyst' | string
  evaluation_status?: 'correct' | 'incorrect' | 'ambiguous' | 'unavailable' | string | null
  attempt_number: number
  reinforcement?: AgentInsight | null
  mission_completed: boolean
  attempt_finished?: boolean
  points_earned: number
  coins_earned?: number
  new_achievements: string[]
  score_percent?: number | null
  passed?: boolean | null
  must_retry?: boolean | null
  can_retry_optionally?: boolean | null
  mission_insight?: AgentInsight | null
  next_step?: CatalystRecommendation | null
  trail_celebration?: CatalystRecommendation | null
}

function agentKey(value?: string | null) {
  return value && value in AGENT_META ? (value as keyof typeof AGENT_META) : 'mentor'
}

function optionLetter(index: number) {
  return String.fromCharCode(65 + index)
}

export function LessonPlayerPage() {
  const { missionId } = useParams()
  const navigate = useNavigate()
  const id = Number(missionId)
  const effects = useLearningEffects()
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [stepIndex, setStepIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [errorStatus, setErrorStatus] = useState<number | null>(null)
  const [started, setStarted] = useState(false)
  const [exitOpen, setExitOpen] = useState(false)
  const [completion, setCompletion] = useState<SubmitResult | null>(null)
  const [celebrated, setCelebrated] = useState(false)
  const [mentorOpen, setMentorOpen] = useState(false)
  const [mentorQuestion, setMentorQuestion] = useState('')
  const [retrying, setRetrying] = useState(false)
  const [coinBurst, setCoinBurst] = useState<number | null>(null)
  const addCoins = useSessionStore((state) => state.addCoins)

  useDocumentTitle(lesson ? `${lesson.mission.name} — Prisma.AI` : 'Módulo — Prisma.AI')

  useEffect(() => {
    if (coinBurst === null) return
    const timer = window.setTimeout(() => setCoinBurst(null), 2000)
    return () => window.clearTimeout(timer)
  }, [coinBurst])

  useEffect(() => {
    if (!Number.isFinite(id)) {
      setError('Módulo inválido.')
      setErrorStatus(400)
      setLoading(false)
      return
    }
    setLoading(true)
    setError('')
    journeyApi
      .getLesson(id)
      .then((response) => {
        setLesson(response.data)
        setStepIndex(response.data.current_step)
        setStarted(response.data.status !== 'available')
      })
      .catch((err: unknown) => {
        const apiError = err as {
          response?: { status?: number; data?: { error?: { message?: string } } }
        }
        setErrorStatus(apiError.response?.status ?? null)
        setError(
          apiError.response?.data?.error?.message ||
            'Não foi possível abrir este módulo. Tente novamente.',
        )
      })
      .finally(() => setLoading(false))
  }, [id])

  const step = lesson?.steps.find((item) => item.index === stepIndex) ?? null
  const totalSteps = lesson?.steps.length ?? 0
  const completedCount = lesson?.completed_steps.length ?? 0
  const progressPercent = totalSteps ? Math.round((completedCount / totalSteps) * 100) : 0
  const missionCompleted = lesson?.status === 'completed'

  useEffect(() => {
    if (step?.type === 'summary' && !celebrated) {
      setCelebrated(true)
      effects.play('complete')
    }
  }, [step?.type, celebrated, effects])

  async function saveStep(stepToSave: number) {
    setSaving(true)
    try {
      const response = await journeyApi.saveLessonStep(id, stepToSave)
      setLesson((current) =>
        current
          ? {
              ...current,
              current_step: response.data.current_step,
              completed_steps: response.data.completed_steps,
            }
          : current,
      )
      setStepIndex(response.data.current_step)
      effects.play('tap')
    } catch {
      setError('Não foi possível salvar seu progresso. Tente novamente.')
    } finally {
      setSaving(false)
    }
  }

  async function handleStart() {
    setSaving(true)
    setError('')
    try {
      await journeyApi.startMission(id)
      setStarted(true)
      // O conjunto de perguntas é sorteado no start; recarrega a lição para
      // exibir as atividades da tentativa atual, não as do carregamento inicial.
      const refreshed = await journeyApi.getLesson(id)
      setLesson(refreshed.data)
      const response = await journeyApi.saveLessonStep(id, stepIndex)
      setLesson((current) =>
        current
          ? {
              ...current,
              current_step: response.data.current_step,
              completed_steps: response.data.completed_steps,
              progress: current.progress
                ? { ...current.progress, status: 'in_progress' }
                : {
                    mission_id: id,
                    status: 'in_progress',
                    score: null,
                    score_percent: null,
                    attempts: 1,
                    started_at: new Date().toISOString(),
                    completed_at: null,
                  },
            }
          : current,
      )
      setStepIndex(response.data.current_step)
      effects.play('tap')
    } catch {
      setError('Não foi possível iniciar o módulo. Tente novamente.')
    } finally {
      setSaving(false)
    }
  }

  function handleActivityResult(result: SubmitResult) {
    const earned = result.coins_earned ?? 0
    if (earned > 0) {
      addCoins(earned)
      setCoinBurst(earned)
    }

    setLesson((current) => {
      if (!current || !step) return current
      const completed = new Set(current.completed_steps)
      // Acerto e erro contam igualmente como etapa respondida.
      completed.add(step.index)
      return {
        ...current,
        completed_steps: [...completed].sort((a, b) => a - b),
        steps: current.steps.map((item) =>
          item.index === step.index
            ? {
                ...item,
                completed: true,
                user_response: {
                  is_correct: result.is_correct,
                  feedback: result.feedback,
                  attempt_number: result.attempt_number,
                  response_data: {},
                  correct_answer: result.correct_answer ?? null,
                },
              }
            : item,
        ),
      }
    })

    if (result.attempt_finished || result.mission_completed) {
      const passedNow = result.passed === true || result.mission_completed
      setCompletion(result)
      setLesson((current) =>
        current
          ? {
              ...current,
              status: passedNow ? 'completed' : current.status,
              progress: {
                mission_id: id,
                status: passedNow ? 'completed' : 'in_progress',
                score: passedNow
                  ? result.points_earned || current.progress?.score || 0
                  : current.progress?.score ?? null,
                score_percent:
                  result.score_percent ?? current.progress?.score_percent ?? null,
                attempts: current.progress?.attempts ?? 1,
                started_at: current.progress?.started_at ?? new Date().toISOString(),
                completed_at: passedNow ? new Date().toISOString() : null,
              },
            }
          : current,
      )
    }
  }

  async function handleRetry(voluntary: boolean) {
    setRetrying(true)
    setError('')
    try {
      await journeyApi.retryMission(id, voluntary)
      const response = await journeyApi.getLesson(id)
      setLesson(response.data)
      setStepIndex(response.data.current_step)
      setCompletion(null)
      setCelebrated(false)
      effects.play('tap')
    } catch (err: unknown) {
      const apiError = err as { response?: { data?: { error?: { message?: string } } } }
      setError(
        apiError.response?.data?.error?.message ||
          'Não foi possível reiniciar este módulo. Tente novamente.',
      )
    } finally {
      setRetrying(false)
    }
  }

  function handleExit() {
    if (missionCompleted) {
      navigate('/student/journey')
      return
    }
    setExitOpen(true)
  }

  function openMentor(question = '') {
    setMentorQuestion(question)
    setMentorOpen(true)
  }

  if (loading) {
    return (
      <div className={`student-app ${styles.loadingScreen}`}>
        <BrandLike />
        <div className={styles.loadingOrb} />
        <p>Preparando seu módulo...</p>
      </div>
    )
  }

  if (errorStatus === 403) {
    return (
      <div className={`student-app ${styles.fullScreen}`}>
        <div className={styles.lockedScreen}>
          <span className={styles.lockedIcon}><LockIcon size={24} /></span>
          <span className="st-eyebrow">Módulo bloqueado</span>
          <h1>Termine a etapa anterior primeiro.</h1>
          <p>{error}</p>
          <Link to="/student/journey" className={styles.primaryButton}>
            Voltar para a jornada
          </Link>
        </div>
      </div>
    )
  }

  if (error && !lesson) {
    return (
      <div className={`student-app ${styles.fullScreen}`}>
        <div className={styles.errorScreen} role="alert">
          <h1>Não conseguimos abrir este módulo.</h1>
          <p>{error}</p>
          <Button onClick={() => window.location.reload()}>Tentar novamente</Button>
          <Link to="/student/journey" className={styles.textLink}>Voltar para a jornada</Link>
        </div>
      </div>
    )
  }

  if (!lesson || !step) return null

  const currentAgent = agentKey(step.agent)
  const isIntro = step.type === 'intro'
  const isSummary = step.type === 'summary'
  const isQuestion = step.type === 'question' || step.type === 'scenario'

  return (
    <div className={`student-app ${styles.shell}`} data-phase={lesson.phase.number}>
      <header className={styles.topbar}>
        <button
          type="button"
          className={styles.exitButton}
          onClick={handleExit}
          aria-label="Sair do módulo"
        >
          <CloseIcon size={18} />
        </button>

        <div className={styles.topbarCenter}>
          <span className={styles.topbarBrand}>Prisma.AI</span>
          <div className={styles.topProgress}>
            <div className={styles.topProgressTrack}>
              <span style={{ width: `${progressPercent}%` }} />
            </div>
            <span>Etapa {stepIndex + 1} de {totalSteps}</span>
          </div>
        </div>

        <div className={styles.topbarActions}>
          <button
            type="button"
            className={styles.mentorButton}
            onClick={() => openMentor()}
            aria-label="Perguntar ao Mentor"
            title="Perguntar ao Mentor"
          >
            <ChatIcon size={18} />
          </button>
          <button
            type="button"
            className={styles.soundButton}
            onClick={effects.toggle}
            aria-pressed={effects.enabled}
            aria-label={effects.enabled ? 'Desativar efeitos sonoros' : 'Ativar efeitos sonoros'}
            title={effects.enabled ? 'Efeitos ativados' : 'Efeitos desativados'}
          >
            {effects.enabled ? <VolumeIcon size={18} /> : <VolumeOffIcon size={18} />}
          </button>
        </div>
      </header>

      {saving && <span className={styles.saving}>Salvando...</span>}
      {coinBurst !== null && (
        <span className={styles.coinBurst} role="status" aria-live="polite">
          +{coinBurst} <span aria-hidden="true">◆</span>
        </span>
      )}
      {error && (
        <p className={styles.pageError} role="alert">
          {error}
        </p>
      )}

      <main className={styles.stage}>
        <div key={step.index} className={`${styles.stepCard} ${styles[`step_${step.type}`] ?? ''}`}>
          {isIntro && (
            <IntroStep
              lesson={lesson}
              step={step}
              started={started}
              loading={saving}
              onStart={handleStart}
              onContinue={() => saveStep(step.index)}
            />
          )}

          {step.type === 'reading' && (
            <ReadingStep
              lesson={lesson}
              step={step}
              loading={saving}
              onContinue={() => saveStep(step.index)}
            />
          )}

          {isQuestion && (
            <QuestionStep
              key={step.index}
              step={step}
              totalSteps={totalSteps}
              missionId={id}
              effects={effects}
              onResult={handleActivityResult}
              onContinue={() => saveStep(step.index)}
              onAskMentor={openMentor}
            />
          )}

          {isSummary && (
            <SummaryStep
              lesson={lesson}
              step={step}
              completion={completion}
              retrying={retrying}
              onRetry={handleRetry}
              onFinish={() => saveStep(step.index)}
              onAskMentor={openMentor}
            />
          )}
        </div>
      </main>

      <footer className={styles.footer}>
        <span>
          {lesson.phase.number}.{lesson.mission.number} · {lesson.estimated_minutes} min estimados
        </span>
        <span className={styles.footerAgent}>
          <AgentAvatar agent={currentAgent} size={28} />
          {AGENT_META[currentAgent].name}
        </span>
      </footer>

      {exitOpen && (
        <div className={styles.modalOverlay} role="presentation">
          <div
            className={styles.modal}
            role="dialog"
            aria-modal="true"
            aria-labelledby="exit-title"
          >
            <span className={styles.modalIcon} aria-hidden="true">
              <ArrowLeftIcon size={20} />
            </span>
            <h2 id="exit-title">Sair do módulo?</h2>
            <p>
              O progresso das etapas concluídas já foi salvo. Respostas ainda não
              confirmadas não serão registradas.
            </p>
            <div className={styles.modalActions}>
              <Button variant="ghost" onClick={() => setExitOpen(false)}>
                Continuar aprendendo
              </Button>
              <Button onClick={() => navigate('/student/journey')}>
                Sair agora
              </Button>
            </div>
          </div>
        </div>
      )}

      {mentorOpen && (
        <div className={styles.modalOverlay} role="presentation">
          <div
            className={styles.mentorModal}
            role="dialog"
            aria-modal="true"
            aria-label="Conversa com o Mentor"
          >
            <MentorChat
              missionId={id}
              compact
              initialQuestion={mentorQuestion}
              onClose={() => setMentorOpen(false)}
            />
          </div>
        </div>
      )}
    </div>
  )
}

function BrandLike() {
  return (
    <span className={styles.brandLike}>
      <svg viewBox="0 0 34 38" aria-hidden="true">
        <path d="M17 2 32 31H2L17 2Z" fill="url(#lesson-brand)" />
        <defs>
          <linearGradient id="lesson-brand" x1="5" y1="5" x2="29" y2="32">
            <stop stopColor="#D8CFFF" />
            <stop offset=".45" stopColor="#8B5CFF" />
            <stop offset="1" stopColor="#56CCF2" />
          </linearGradient>
        </defs>
      </svg>
      Prisma.AI
    </span>
  )
}

function IntroStep({
  lesson,
  step,
  started,
  loading,
  onStart,
  onContinue,
}: {
  lesson: Lesson
  step: LessonStep
  started: boolean
  loading: boolean
  onStart: () => void
  onContinue: () => void
}) {
  const agent = agentKey(step.agent)
  return (
    <div className={styles.introLayout}>
      <div className={styles.introCopy}>
        <div className={styles.stepKicker}>
          <span className="st-chip st-chip--purple">
            Módulo {lesson.phase.number}.{lesson.mission.number}
          </span>
          <span className="st-chip">{lesson.estimated_minutes} min</span>
          <span className="st-chip">{lesson.steps.length} etapas</span>
        </div>
        <h1>{step.title}</h1>
        <RichText text={step.body ?? ''} className={styles.bodyText} />
        {step.highlights.length > 0 && (
          <ul className={styles.highlights}>
            {step.highlights.map((item) => (
              <li key={item}>
                <span><CheckIcon size={13} /></span>
                {item}
              </li>
            ))}
          </ul>
        )}
        <button
          type="button"
          className={styles.primaryButton}
          onClick={started ? onContinue : onStart}
          disabled={loading}
        >
          {started ? 'Continuar' : 'Começar módulo'}
          <ArrowRightIcon size={16} />
        </button>
        <p className={styles.introNote}>
          Você pode sair a qualquer momento. O progresso é salvo etapa por etapa.
        </p>
      </div>
      <div className={styles.introArt} aria-hidden="true">
        <span className={styles.introOrb} />
        <span className={styles.introRing} />
        <Mascot3D
          agent={agent}
          animation={agent === 'mentor' ? 'M-02' : agent === 'analyst' ? 'A-02' : 'C-03'}
          size={260}
        />
        <div className={styles.agentFloating}>
          <AgentAvatar agent={agent} size={40} />
          <span>
            <strong>{AGENT_META[agent].name}</strong>
            <small>{AGENT_META[agent].role}</small>
          </span>
        </div>
      </div>
    </div>
  )
}

function ReadingStep({
  lesson,
  step,
  loading,
  onContinue,
}: {
  lesson: Lesson
  step: LessonStep
  loading: boolean
  onContinue: () => void
}) {
  const agent = agentKey(step.agent ?? 'mentor')
  const typeLabel =
    step.content_type === 'example'
      ? 'Exemplo prático'
      : step.content_type === 'tip'
        ? 'Dica para levar'
        : 'Entenda o conceito'
  return (
    <div className={styles.readingLayout}>
      <div className={styles.readingMeta}>
        <AgentAvatar agent={agent} size={46} />
        <div>
          <span>{typeLabel}</span>
          <strong>{AGENT_META[agent].name}</strong>
        </div>
        <span className={styles.stepNumber}>
          {step.index + 1}/{lesson.steps.length}
        </span>
      </div>
      <h1>{step.title}</h1>
      <RichText text={step.body ?? ''} className={styles.bodyTextLarge} />
      <div className={styles.readingFooter}>
        <span>Leia com calma. Você pode voltar à jornada quando quiser.</span>
        <button type="button" className={styles.primaryButton} onClick={onContinue} disabled={loading}>
          Continuar
          <ArrowRightIcon size={16} />
        </button>
      </div>
    </div>
  )
}

function QuestionStep({
  step,
  totalSteps,
  missionId,
  effects,
  onResult,
  onContinue,
  onAskMentor,
}: {
  step: LessonStep
  totalSteps: number
  missionId: number
  effects: ReturnType<typeof useLearningEffects>
  onResult: (result: SubmitResult) => void
  onContinue: () => void
  onAskMentor: (question?: string) => void
}) {
  const activity = step.activity as Activity
  const isOpenText = activity.activity_type === 'open_text'
  const isSimulation = step.type === 'scenario' || activity.activity_type === 'simulation'
  const options = activity.content.options ?? []
  const previous = step.user_response
  const [selected, setSelected] = useState(() => {
    const data = previous?.response_data as Record<string, unknown> | undefined
    return String(data?.selected_option ?? data?.choice ?? '')
  })
  const [text, setText] = useState(() => {
    const data = previous?.response_data as Record<string, unknown> | undefined
    return String(data?.text ?? '')
  })
  const [result, setResult] = useState<SubmitResult | null>(
    previous
      ? {
          is_correct: previous.is_correct,
          correct_answer: previous.correct_answer ?? null,
          score: 0,
          feedback: previous.feedback,
          evaluation_status: previous.evaluation_status ?? undefined,
          attempt_number: previous.attempt_number,
          mission_completed: false,
          points_earned: 0,
          new_achievements: [],
        }
      : null,
  )
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const mentorQuestion = result?.reinforcement
    ? `Pode me ajudar a revisar ${result.reinforcement.competencies[0] ?? 'este conceito'}?`
    : result?.is_correct === false
      ? 'Pode explicar por que a minha resposta não estava completa?'
      : 'Pode me dar um retorno sobre a minha resposta?'

  const evaluationStatus =
    result?.evaluation_status ??
    (result?.is_correct === true
      ? 'correct'
      : result?.is_correct === false
        ? 'incorrect'
        : 'unavailable')
  const isCorrectResult = evaluationStatus === 'correct'
  const isIncorrectResult = evaluationStatus === 'incorrect'
  const isAmbiguousResult = evaluationStatus === 'ambiguous'
  const isUnavailableResult = evaluationStatus === 'unavailable' && isOpenText

  async function handleSubmit() {
    if (result || submitting) return
    if (isOpenText && !text.trim()) {
      setError('Escreva sua resposta antes de enviar.')
      return
    }
    if (!isOpenText && !selected) {
      setError('Escolha uma alternativa antes de enviar.')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      const response = await journeyApi.submitResponse(
        missionId,
        activity.id,
        isOpenText
          ? { text: text.trim() }
          : isSimulation
            ? { choice: selected }
            : { selected_option: selected },
      )
      setResult(response.data)
      onResult(response.data)
      if (response.data.is_correct === false) effects.play('incorrect')
      else effects.play('correct')
    } catch {
      setError('Não foi possível enviar sua resposta. Tente novamente.')
    } finally {
      setSubmitting(false)
    }
  }

  function handleRevise() {
    setResult(null)
    setError('')
    effects.play('tap')
  }

  return (
    <div className={styles.questionLayout}>
      <div className={styles.questionMeta}>
        <span className={styles.questionType}>
          {isOpenText ? 'Resposta aberta' : isSimulation ? 'Decisão de cenário' : 'Verificação'}
        </span>
        <span className={styles.stepNumber}>
          {step.index + 1}/{totalSteps}
        </span>
      </div>

      {isSimulation && activity.content.scenario && (
        <div className={styles.scenarioBox}>
          <span>Cenário</span>
          <p>{activity.content.scenario}</p>
        </div>
      )}

      <h1>{activity.content.prompt}</h1>
      {activity.content.hint && <p className={styles.hint}>{activity.content.hint}</p>}

      {isOpenText ? (
        <label className={styles.openAnswer}>
          <span className={styles.srOnly}>Sua resposta</span>
          <textarea
            value={text}
            onChange={(event) => {
              setText(event.target.value)
              setError('')
            }}
            maxLength={activity.content.max_length ?? 2000}
            disabled={result !== null || submitting}
            rows={6}
            placeholder="Escreva com as suas palavras..."
          />
          <small>{text.length}/{activity.content.max_length ?? 2000}</small>
        </label>
      ) : (
        <div className={styles.options} role="radiogroup" aria-label={activity.content.prompt}>
          {options.map((option, index) => (
            <label
              key={option.value}
              className={[
                styles.option,
                selected === option.value ? styles.optionSelected : '',
                result?.is_correct === false && selected === option.value
                  ? styles.optionWrong
                  : '',
                (result?.is_correct === true && selected === option.value) ||
                (result?.is_correct === false && result.correct_answer === option.value)
                  ? styles.optionCorrect
                  : '',
              ].join(' ')}
            >
              <input
                type="radio"
                name={`lesson-${activity.id}`}
                value={option.value}
                aria-label={option.label}
                checked={selected === option.value}
                onChange={() => {
                  setSelected(option.value)
                  setError('')
                }}
                disabled={result !== null || submitting}
              />
              <span className={styles.optionLetter}>{optionLetter(index)}</span>
              <span>{option.label}</span>
            </label>
          ))}
        </div>
      )}

      {error && <p className={styles.questionError} role="alert">{error}</p>}

      {submitting && isOpenText && (
        <div className={styles.mentorAnalyzing} role="status" aria-live="polite">
          <div className={styles.analyzingMascot} aria-hidden="true">
            <Mascot3D agent="mentor" animation="M-03" size={88} />
          </div>
          <div>
            <span className={styles.feedbackKicker}>Mentor</span>
            <strong>Analisando sua resposta...</strong>
            <p>
              Estou comparando o que você escreveu com os critérios desta
              atividade.
            </p>
            <span className={styles.analyzingDots} aria-hidden="true">
              <i />
              <i />
              <i />
            </span>
          </div>
        </div>
      )}

      {result && (
        <div
          className={[
            styles.feedback,
            isIncorrectResult
              ? styles.feedbackWrong
              : isCorrectResult
                ? styles.feedbackCorrect
                : styles.feedbackNeutral,
          ].join(' ')}
          role="status"
          aria-live="polite"
        >
          <Mascot3D
            agent="mentor"
            animation={isCorrectResult ? 'M-10' : isIncorrectResult ? 'M-07' : 'M-08'}
            size={80}
          />
          <div>
            <span className={styles.feedbackKicker}>
              {isCorrectResult
                ? 'Resposta correta'
                : isIncorrectResult
                  ? 'Feedback do Mentor'
                  : isAmbiguousResult
                    ? 'Preciso de mais contexto'
                    : isUnavailableResult
                      ? 'Avaliação indisponível'
                      : 'Resposta registrada'}
            </span>
            <strong>
              {isCorrectResult
                ? 'Você aplicou o conceito.'
                : isIncorrectResult
                  ? 'Vale revisar o raciocínio.'
                  : isAmbiguousResult
                    ? 'Complementa sua resposta?'
                    : isUnavailableResult
                      ? 'Sua resposta foi registrada.'
                      : 'Obrigado por compartilhar.'}
            </strong>
            <p>{result.feedback}</p>
          </div>
        </div>
      )}

      {result?.is_correct === false && result.correct_answer && (
        <p className={styles.correctReveal} role="status">
          A resposta correta está destacada em verde.
        </p>
      )}

      {result?.reinforcement && (
        <div className={styles.analystNote} role="status">
          <AgentAvatar agent="analyst" size={40} />
          <div>
            <span className={styles.feedbackKicker}>Analista de Progresso</span>
            <p>{result.reinforcement.message}</p>
          </div>
        </div>
      )}

      <div className={styles.questionFooter}>
        {!result && (
          <button
            type="button"
            className={styles.primaryButton}
            onClick={handleSubmit}
            disabled={submitting}
          >
            {submitting
              ? isOpenText
                ? 'Mentor analisando...'
                : 'Confirmando...'
              : 'Confirmar resposta'}
            {!submitting && <ArrowRightIcon size={16} />}
          </button>
        )}
        {result && (
          <button type="button" className={styles.primaryButton} onClick={onContinue}>
            Continuar
            <ArrowRightIcon size={16} />
          </button>
        )}
        {isAmbiguousResult && (
          <button
            type="button"
            className={styles.secondaryButton}
            onClick={handleRevise}
          >
            Reescrever resposta
          </button>
        )}
        {result && (
          <button
            type="button"
            className={styles.secondaryButton}
            onClick={() => onAskMentor(mentorQuestion)}
          >
            <ChatIcon size={15} />
            Pedir ajuda ao Mentor
          </button>
        )}
      </div>
    </div>
  )
}

function SummaryStep({
  lesson,
  step,
  completion,
  retrying,
  onRetry,
  onFinish,
  onAskMentor,
}: {
  lesson: Lesson
  step: LessonStep
  completion: SubmitResult | null
  retrying: boolean
  onRetry: (voluntary: boolean) => void
  onFinish: () => void
  onAskMentor: (question?: string) => void
}) {
  const passed = completion?.passed ?? lesson.passed ?? lesson.status === 'completed'
  const scorePercent =
    completion?.score_percent ??
    lesson.score_percent ??
    lesson.progress?.score_percent ??
    null
  const activitySteps = lesson.steps.filter((item) => item.activity !== null)
  const pendingActivities = activitySteps.some((item) => item.user_response === null)
  const finished =
    completion?.attempt_finished === true ||
    lesson.attempt_finished === true ||
    scorePercent !== null ||
    lesson.status === 'completed'
  const mustRetry =
    completion?.must_retry ??
    lesson.must_retry ??
    (!passed && finished && !pendingActivities)
  const canRetryOptionally =
    completion?.can_retry_optionally ??
    lesson.can_retry_optionally ??
    (passed && (scorePercent ?? 0) >= 90)
  const points = completion?.points_earned || lesson.progress?.score || 0
  const achievements = completion?.new_achievements ?? []
  // O `next_step` do submit já conhece o próximo módulo liberado; o `lesson`
  // carregado no início da tentativa ainda o via bloqueado.
  const nextMission =
    lesson.next_mission ??
    (completion?.next_step?.mission_id
      ? {
          id: completion.next_step.mission_id,
          number: 0,
          name: completion.next_step.mission_name ?? 'Próximo módulo',
        }
      : null)
  const insight = completion?.mission_insight ?? lesson.mission_insight ?? null
  const nextStep = completion?.next_step ?? lesson.next_step ?? null
  const trailCelebration = completion?.trail_celebration ?? null

  useEffect(() => {
    onFinish()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className={styles.summaryLayout}>
      {passed && (
        <div className={styles.confetti} aria-hidden="true">
          {Array.from({ length: 16 }).map((_, index) => (
            <span key={index} style={{ ['--i' as string]: index }} />
          ))}
        </div>
      )}

      <div className={styles.summaryContent}>
        <div className={styles.summaryArt} aria-hidden="true">
          <Mascot3D
            agent="catalyst"
            animation={trailCelebration ? 'C-12' : passed ? 'C-11' : 'C-10'}
            size={190}
          />
        </div>

        <span className="st-eyebrow">
          {passed ? 'Módulo concluído' : finished ? 'Resultado do módulo' : 'Resumo do módulo'}
        </span>
        <h1>{step.title}</h1>
        <RichText text={step.body ?? ''} className={styles.summaryBody} />

        {scorePercent !== null && (
          <div
            className={[
              styles.resultPanel,
              passed ? styles.resultPassed : styles.resultFailed,
            ].join(' ')}
            role="status"
          >
            <span className={styles.resultPercent}>{Math.round(scorePercent)}%</span>
            <div>
              <strong>{passed ? 'Aprovado ✓' : 'Refaça para avançar ✗'}</strong>
              <span>Aproveitamento do módulo</span>
            </div>
          </div>
        )}

        <div className={styles.summaryStats}>
          <div>
            <span>Pontos</span>
            <strong>{passed ? `+${points}` : '—'}</strong>
          </div>
          <div>
            <span>Etapas</span>
            <strong>{lesson.steps.length}</strong>
          </div>
          <div>
            <span>Tempo estimado</span>
            <strong>{lesson.estimated_minutes} min</strong>
          </div>
        </div>

        {step.highlights.length > 0 && (
          <ul className={styles.summaryHighlights}>
            {step.highlights.map((item) => (
              <li key={item}>
                <span><CheckIcon size={13} /></span>
                {item}
              </li>
            ))}
          </ul>
        )}

        {lesson.competencies.length > 0 && (
          <div className={styles.competencies}>
            <span>Competências trabalhadas</span>
            <div>
              {lesson.competencies.map((competency) => (
                <span key={competency.code ?? competency.name}>
                  {competency.name}
                </span>
              ))}
            </div>
          </div>
        )}

        {insight && (
          <div
            className={[
              styles.summaryInsight,
              insight.severity === 'attention' ? styles.summaryInsightAttention : '',
            ].join(' ')}
          >
            <AgentAvatar agent="analyst" size={38} />
            <div>
              <span className={styles.feedbackKicker}>Analista de Progresso</span>
              <p>{insight.message}</p>
            </div>
          </div>
        )}

        {trailCelebration && (
          <div className={styles.summaryCatalyst}>
            <AgentAvatar agent="catalyst" size={34} />
            <div>
              <span className={styles.feedbackKicker}>
                {trailCelebration.badge_label ?? 'Trilha concluída'}
              </span>
              <p>{trailCelebration.celebration_message ?? trailCelebration.message}</p>
              {trailCelebration.next_step_message && (
                <p>{trailCelebration.next_step_message}</p>
              )}
            </div>
          </div>
        )}

        {nextStep && (
          <div className={styles.summaryCatalyst}>
            <AgentAvatar agent="catalyst" size={34} />
            <p>{nextStep.message}</p>
          </div>
        )}

        {achievements.length > 0 && (
          <div className={styles.achievementBox}>
            <TrophyIcon size={18} />
            <span>Novas conquistas: {achievements.join(', ')}</span>
          </div>
        )}

        <div className={styles.summaryActions}>
          {mustRetry && (
            <button
              type="button"
              className={styles.primaryButton}
              onClick={() => onRetry(false)}
              disabled={retrying}
            >
              {retrying ? 'Preparando nova tentativa...' : 'Refazer módulo'}
              {!retrying && <ArrowRightIcon size={16} />}
            </button>
          )}
          {!mustRetry && passed && nextMission && (
            <Link
              to={`/student/learn/${nextMission.id}`}
              className={styles.primaryButton}
            >
              Próximo módulo: {nextMission.name}
              <ArrowRightIcon size={16} />
            </Link>
          )}
          {!mustRetry && (!passed || !nextMission) && (
            <Link to="/student/journey" className={styles.primaryButton}>
              Voltar para a jornada
            </Link>
          )}
          {passed && (
            <button
              type="button"
              className={styles.secondaryButton}
              onClick={() => onRetry(true)}
              disabled={retrying}
            >
              {canRetryOptionally
                ? 'Refazer por vontade'
                : 'Refazer módulo (opcional)'}
            </button>
          )}
          {mustRetry && (
            <Link to="/student/journey" className={styles.secondaryButton}>
              Voltar para a jornada
            </Link>
          )}
          <button
            type="button"
            className={styles.secondaryButton}
            onClick={() => onAskMentor('Quero conversar sobre o que aprendi neste módulo.')}
          >
            <ChatIcon size={15} />
            Conversar com o Mentor sobre este módulo
          </button>
        </div>

        {pendingActivities && (
          <p className={styles.summaryWarning}>
            Ainda há atividades pendentes. Volte ao módulo para concluir.
          </p>
        )}
      </div>
    </div>
  )
}
