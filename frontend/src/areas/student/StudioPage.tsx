import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { journeyApi, progressApi, studioApi } from '@/api'
import { Button } from '@/design-system'
import {
  ArrowRightIcon,
  CheckIcon,
  ChatIcon,
  SparkIcon,
} from '@/design-system/Icons'
import { RichText } from '@/shared/RichText'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import { useSessionStore } from '@/store/session'
import type {
  GeneratedContent,
  MissionWithProgress,
  PhaseJourney,
  StudioContent,
  StudioFormat,
  StudioQuestion,
} from '@/types/student'
import { CoinsDisplay } from './components/CoinsDisplay'
import styles from './Studio.module.css'

const FORMAT_OPTIONS: Array<{
  value: StudioFormat
  label: string
  cost: number
  emoji: string
  description: string
}> = [
  {
    value: 'revisao',
    label: 'Revisão narrativa',
    cost: 30,
    emoji: '📖',
    description: 'Um texto do Mentor explicando os conceitos no seu estilo.',
  },
  {
    value: 'flashcards',
    label: 'Flashcards',
    cost: 20,
    emoji: '🃏',
    description: 'Cartões de frente e verso para revisar em qualquer lugar.',
  },
  {
    value: 'exercicios',
    label: 'Exercícios extras',
    cost: 25,
    emoji: '✏️',
    description: 'Questões novas para praticar e alimentar o Analista.',
  },
]

const FORMAT_LABELS: Record<string, string> = {
  revisao: 'Revisão narrativa',
  flashcards: 'Flashcards',
  exercicios: 'Exercícios extras',
}

function isCoursedPhase(phase: PhaseJourney) {
  return (
    phase.status === 'in_progress' ||
    phase.status === 'completed' ||
    phase.missions.some(
      (mission) =>
        mission.progress !== null ||
        mission.status === 'in_progress' ||
        mission.status === 'completed',
    )
  )
}

function isCoursedMission(mission: MissionWithProgress) {
  return (
    mission.progress !== null ||
    mission.status === 'in_progress' ||
    mission.status === 'completed'
  )
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function apiErrorMessage(error: unknown, fallback: string) {
  const apiError = error as {
    response?: { data?: { error?: { message?: string } } }
  }
  return apiError.response?.data?.error?.message ?? fallback
}

function formatLabel(format: string) {
  return FORMAT_LABELS[format] ?? format
}

export function StudioPage() {
  useDocumentTitle('Estúdio de Prismas — Prisma.AI')
  const coins = useSessionStore((state) => state.coins)
  const setCoins = useSessionStore((state) => state.setCoins)
  const [phases, setPhases] = useState<PhaseJourney[]>([])
  const [library, setLibrary] = useState<GeneratedContent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)
  const [tab, setTab] = useState<'create' | 'library'>('create')
  const [phaseId, setPhaseId] = useState<number | ''>('')
  const [missionId, setMissionId] = useState<number | ''>('')
  const [format, setFormat] = useState<StudioFormat>('flashcards')
  const [styleHint, setStyleHint] = useState('')
  const [notice, setNotice] = useState('')
  const [requesting, setRequesting] = useState(false)
  const [generation, setGeneration] = useState<GeneratedContent | null>(null)
  const [libraryLoading, setLibraryLoading] = useState(false)

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')
    Promise.all([journeyApi.getOverview(), progressApi.getSummary()])
      .then(([overviewResponse, summaryResponse]) => {
        if (!active) return
        const available = overviewResponse.data.phases.filter(isCoursedPhase)
        setPhases(available)
        setCoins(summaryResponse.data.coins)
        setPhaseId(available[0]?.phase.id ?? '')
      })
      .catch(() => {
        if (!active) return
        setError(
          'Não foi possível abrir o Estúdio. Verifique sua conexão e tente novamente.',
        )
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    studioApi
      .getLibrary()
      .then((libraryResponse) => {
        if (active) setLibrary(libraryResponse.data.items)
      })
      .catch(() => {
        // A criação continua disponível mesmo se a biblioteca falhar.
      })
    return () => {
      active = false
    }
  }, [reloadKey, setCoins])

  const selectedPhase = useMemo(
    () => phases.find((phase) => phase.phase.id === phaseId) ?? null,
    [phases, phaseId],
  )
  const missionOptions = useMemo(
    () =>
      (selectedPhase?.missions ?? []).filter(isCoursedMission),
    [selectedPhase],
  )
  const selectedFormat =
    FORMAT_OPTIONS.find((option) => option.value === format) ?? FORMAT_OPTIONS[0]
  const cost = selectedFormat.cost
  const insufficient = coins < cost

  async function refreshLibrary() {
    const response = await studioApi.getLibrary()
    setLibrary(response.data.items)
  }

  async function refreshGeneration(id: number): Promise<GeneratedContent | null> {
    try {
      const generationResponse = await studioApi.getGeneration(id)
      setGeneration(generationResponse.data)
      try {
        const summaryResponse = await progressApi.getSummary()
        setCoins(summaryResponse.data.coins)
      } catch {
        // O conteúdo atualiza mesmo se o saldo falhar em sincronizar.
      }
      return generationResponse.data
    } catch {
      setNotice('Não foi possível atualizar este conteúdo.')
      return null
    }
  }

  async function handleGenerate() {
    if (!phaseId || requesting) return
    setRequesting(true)
    setNotice('')
    try {
      const response = await studioApi.generate({
        format,
        phase_id: Number(phaseId),
        mission_id: missionId ? Number(missionId) : null,
        style_hint: styleHint.trim() || null,
      })
      setGeneration(response.data)
      setTab('create')
      try {
        const summaryResponse = await progressApi.getSummary()
        setCoins(summaryResponse.data.coins)
      } catch {
        // A geração já foi concluída; o saldo será corrigido no próximo load.
      }
      refreshLibrary().catch(() => {
        // A biblioteca é secundária nesta resposta.
      })
    } catch (err: unknown) {
      setNotice(
        apiErrorMessage(
          err,
          'Não foi possível gerar o conteúdo agora. Tente novamente.',
        ),
      )
    } finally {
      setRequesting(false)
    }
  }

  async function handleOpenLibraryItem(item: GeneratedContent) {
    setLibraryLoading(true)
    setNotice('')
    try {
      const response = await studioApi.getGeneration(item.id)
      setGeneration(response.data)
      setTab('create')
    } catch {
      setNotice('Não foi possível abrir este conteúdo da biblioteca.')
    } finally {
      setLibraryLoading(false)
    }
  }

  if (loading) {
    return (
      <div className={`st-app-page ${styles.loadingPage}`}>
        <div className="st-skeleton" />
        <div className={styles.loadingGrid}>
          <div className="st-skeleton" />
          <div className="st-skeleton" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={`st-app-page ${styles.errorPage}`}>
        <div className={styles.errorCard} role="alert">
          <h1>O Estúdio não abriu.</h1>
          <p>{error}</p>
          <Button onClick={() => setReloadKey((value) => value + 1)}>
            Tentar novamente
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className={`st-app-page ${styles.page}`}>
      <header className={styles.header}>
        <div className={styles.headerCopy}>
          <span className="st-eyebrow">Estúdio de Prismas</span>
          <h1>
            Transforme <span>Prismas</span> em revisão do seu jeito.
          </h1>
          <p>
            Escolha um módulo que você já cursou, diga como quer aprender e
            peça ao Mentor uma revisão personalizada. O conteúdo fica salvo na
            sua biblioteca para sempre.
          </p>
        </div>
        <div className={styles.headerAside}>
          <CoinsDisplay coins={coins} showLabel />
          <Link to="/student/journey" className={styles.headerLink}>
            Continuar jornada
            <ArrowRightIcon size={15} />
          </Link>
        </div>
      </header>

      <div className={styles.tabs} role="tablist" aria-label="Seções do Estúdio">
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'create'}
          className={tab === 'create' ? styles.tabActive : styles.tab}
          onClick={() => setTab('create')}
        >
          <SparkIcon size={15} />
          Criar
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'library'}
          className={tab === 'library' ? styles.tabActive : styles.tab}
          onClick={() => {
            setTab('library')
            refreshLibrary().catch(() =>
              setNotice('Não foi possível carregar sua biblioteca.'),
            )
          }}
        >
          Minha biblioteca
          <span className={styles.tabCount}>{library.length}</span>
        </button>
      </div>

      {notice && (
        <div className={styles.notice} role="status">
          <ChatIcon size={18} />
          <p>{notice}</p>
        </div>
      )}

      {tab === 'create' ? (
        <>
          {phases.length === 0 ? (
            <section className={styles.emptyState}>
              <span aria-hidden="true"><SparkIcon size={26} /></span>
              <h2>Seu Estúdio abre depois da primeira missão.</h2>
              <p>
                Conclua ou comece um módulo para que o Mentor conheça o
                conteúdo que você pode revisar.
              </p>
              <Link to="/student/journey" className={styles.primaryLink}>
                Ir para a jornada
                <ArrowRightIcon size={15} />
              </Link>
            </section>
          ) : (
            <section className={styles.builder} aria-label="Criar revisão">
              <div className={styles.form}>
                <div className={styles.fieldRow}>
                  <label className={styles.field}>
                    <span>Fase</span>
                    <select
                      value={phaseId}
                      onChange={(event) => {
                        setPhaseId(Number(event.target.value))
                        setMissionId('')
                      }}
                    >
                      {phases.map((phase) => (
                        <option key={phase.phase.id} value={phase.phase.id}>
                          Fase {phase.phase.number} · {phase.phase.name}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className={styles.field}>
                    <span>Módulo</span>
                    <select
                      value={missionId}
                      onChange={(event) =>
                        setMissionId(
                          event.target.value ? Number(event.target.value) : '',
                        )
                      }
                    >
                      <option value="">Fase inteira</option>
                      {missionOptions.map((mission) => (
                        <option key={mission.mission.id} value={mission.mission.id}>
                          {mission.mission.number}. {mission.mission.name}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                <fieldset className={styles.formatFieldset}>
                  <legend>Formato da revisão</legend>
                  <div className={styles.formatGrid}>
                    {FORMAT_OPTIONS.map((option) => (
                      <button
                        key={option.value}
                        type="button"
                        className={
                          format === option.value
                            ? styles.formatCardActive
                            : styles.formatCard
                        }
                        onClick={() => setFormat(option.value)}
                        aria-pressed={format === option.value}
                      >
                        <span className={styles.formatEmoji} aria-hidden="true">
                          {option.emoji}
                        </span>
                        <strong>{option.label}</strong>
                        <small>{option.description}</small>
                        <span className={styles.formatCost}>◆ {option.cost}</span>
                      </button>
                    ))}
                  </div>
                </fieldset>

                <label className={styles.field}>
                  <span>Personalize o estilo (opcional)</span>
                  <input
                    value={styleHint}
                    onChange={(event) => setStyleHint(event.target.value)}
                    maxLength={500}
                    placeholder="ex.: analogia com doces, linguagem de games, exemplos de futebol..."
                  />
                </label>

                <div className={styles.generateRow}>
                  <Button
                    onClick={handleGenerate}
                    disabled={requesting || !phaseId}
                  >
                    {requesting ? 'Preparando revisão...' : `Gerar por ◆ ${cost}`}
                  </Button>
                  <span className={styles.balanceHint}>
                    Seu saldo: <strong>◆ {coins}</strong>
                  </span>
                </div>

                {insufficient && (
                  <p className={styles.warning}>
                    Você tem {coins} Prismas e esta revisão custa {cost}.{' '}
                    <Link to="/student/journey">Conclua módulos para ganhar mais.</Link>
                  </p>
                )}

                {requesting && (
                  <div className={styles.generatingState} role="status">
                    <span aria-hidden="true">◆</span>
                    <div>
                      <strong>O Mentor está organizando sua revisão...</strong>
                      <p>
                        Ele usa apenas o conteúdo aprovado dos módulos que você
                        já cursou.
                      </p>
                    </div>
                  </div>
                )}
              </div>

              <aside className={styles.sideCard}>
                <span className="st-eyebrow">Como funciona</span>
                <h2>Você escolhe. O Mentor organiza.</h2>
                <ul>
                  <li>
                    <CheckIcon size={15} />
                    O conteúdo vem apenas dos módulos que você já cursou.
                  </li>
                  <li>
                    <CheckIcon size={15} />
                    O backend monta o contexto; a IA não acessa o banco.
                  </li>
                  <li>
                    <CheckIcon size={15} />
                    Cada geração fica na sua biblioteca pessoal.
                  </li>
                  <li>
                    <CheckIcon size={15} />
                    Exercícios extras viram evidências para o Analista.
                  </li>
                </ul>
                <p className={styles.sideNote}>
                  Enquanto o Mentor não estiver ativado, o Estúdio não consome
                  Prismas: você só acumula.
                </p>
              </aside>
            </section>
          )}

          {generation && (
            <section className={styles.resultSection}>
              <div className="st-section-heading">
                <div>
                  <span className="st-eyebrow">Conteúdo gerado</span>
                  <h2>
                    {generation.mission_name ??
                      generation.phase_name ??
                      'Sua revisão'}
                  </h2>
                  <p>
                    {formatLabel(generation.format)}
                    {generation.style_hint
                      ? ` · estilo: ${generation.style_hint}`
                      : ''}
                  </p>
                </div>
                <span className="st-chip">◆ {generation.coins_spent}</span>
              </div>
              <GenerationView
                key={generation.id}
                generation={generation}
                onRefresh={refreshGeneration}
              />
            </section>
          )}
        </>
      ) : (
        <section className={styles.librarySection}>
          <div className="st-section-heading">
            <div>
              <span className="st-eyebrow">Minha biblioteca</span>
              <h2>Revisões que você já criou.</h2>
              <p>Todo conteúdo gerado fica aqui, pronto para reabrir.</p>
            </div>
            <button
              type="button"
              className={styles.refreshButton}
              onClick={() =>
                refreshLibrary().catch(() =>
                  setNotice('Não foi possível carregar sua biblioteca.'),
                )
              }
            >
              Atualizar
            </button>
          </div>

          {libraryLoading ? (
            <div className={styles.libraryLoading} role="status">
              Abrindo conteúdo...
            </div>
          ) : library.length === 0 ? (
            <div className={styles.emptyState}>
              <span aria-hidden="true"><SparkIcon size={26} /></span>
              <h2>Sua biblioteca está pronta para a primeira revisão.</h2>
              <p>
                Crie flashcards, uma revisão narrativa ou exercícios extras e
                eles aparecerão aqui.
              </p>
              <button
                type="button"
                className={styles.primaryLink}
                onClick={() => setTab('create')}
              >
                Criar minha primeira revisão
                <ArrowRightIcon size={15} />
              </button>
            </div>
          ) : (
            <div className={styles.libraryGrid}>
              {library.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  className={styles.libraryCard}
                  onClick={() => handleOpenLibraryItem(item)}
                >
                  <span className={styles.libraryFormat}>
                    {formatLabel(item.format)}
                  </span>
                  <strong>
                    {item.mission_name ?? item.phase_name ?? 'Sua revisão'}
                  </strong>
                  <p>
                    {item.phase_name}
                    {item.mission_name ? ` · ${item.mission_name}` : ''}
                  </p>
                  <small>
                    {item.style_hint
                      ? `Estilo: ${item.style_hint}`
                      : 'Sem estilo personalizado'}{' '}
                    · {formatDate(item.created_at)} · ◆ {item.coins_spent}
                  </small>
                </button>
              ))}
            </div>
          )}
        </section>
      )}
    </div>
  )
}

function GenerationView({
  generation,
  onRefresh,
}: {
  generation: GeneratedContent
  onRefresh: (id: number) => Promise<GeneratedContent | null>
}) {
  if (generation.format === 'revisao') {
    return <RevisaoView content={generation.content} />
  }
  if (generation.format === 'flashcards') {
    return <FlashcardsView content={generation.content} />
  }
  return <ExerciciosView generation={generation} onRefresh={onRefresh} />
}

function EmptyGenerated({ message }: { message?: string }) {
  return (
    <div className={styles.emptyGenerated}>
      <ChatIcon size={20} />
      <p>
        {message ??
          'Ainda não há conteúdo disponível. Tente gerar novamente em outro formato.'}
      </p>
    </div>
  )
}

function RevisaoView({ content }: { content: StudioContent }) {
  const sections = content.sections ?? []
  return (
    <article className={styles.generatedCard}>
      <span className="st-eyebrow">Revisão narrativa</span>
      <h3>{content.title ?? 'Sua revisão'}</h3>
      {content.message && <p className={styles.generatedMessage}>{content.message}</p>}
      {sections.length === 0 ? (
        <EmptyGenerated message={content.message} />
      ) : (
        sections.map((section) => (
          <section key={section.title} className={styles.revisionSection}>
            <h4>{section.title}</h4>
            <RichText text={section.body} />
          </section>
        ))
      )}
      {content.summary && content.summary.length > 0 && (
        <div className={styles.summaryBox}>
          <strong>Resumo para levar</strong>
          <ul>
            {content.summary.map((item) => (
              <li key={item}>
                <CheckIcon size={13} />
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  )
}

function FlashcardsView({ content }: { content: StudioContent }) {
  const cards = content.cards ?? []
  const [index, setIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)

  if (cards.length === 0) {
    return (
      <article className={styles.generatedCard}>
        <span className="st-eyebrow">Flashcards</span>
        <EmptyGenerated message={content.message} />
      </article>
    )
  }

  const safeIndex = Math.min(index, cards.length - 1)
  const card = cards[safeIndex]

  return (
    <article className={styles.generatedCard}>
      <div className={styles.generatedHead}>
        <span className="st-eyebrow">Flashcards</span>
        <span className={styles.generatedCount}>
          {safeIndex + 1} / {cards.length}
        </span>
      </div>
      <button
        type="button"
        className={[styles.flashcard, flipped ? styles.flashcardBack : ''].join(' ')}
        onClick={() => setFlipped((value) => !value)}
        aria-label={flipped ? 'Mostrar frente do cartão' : 'Mostrar verso do cartão'}
      >
        <small>{flipped ? 'Verso' : 'Frente'}</small>
        <strong>{flipped ? card.back : card.front}</strong>
        <span>Clique no cartão para virar</span>
      </button>
      <div className={styles.cardNav}>
        <Button
          variant="ghost"
          onClick={() => {
            setIndex((value) => Math.max(0, value - 1))
            setFlipped(false)
          }}
          disabled={safeIndex === 0}
        >
          Anterior
        </Button>
        <Button
          onClick={() => {
            setIndex((value) => Math.min(cards.length - 1, value + 1))
            setFlipped(false)
          }}
          disabled={safeIndex === cards.length - 1}
        >
          Próximo
        </Button>
      </div>
    </article>
  )
}

function ExerciciosView({
  generation,
  onRefresh,
}: {
  generation: GeneratedContent
  onRefresh: (id: number) => Promise<GeneratedContent | null>
}) {
  const questions = generation.content.questions ?? []
  const [index, setIndex] = useState(() => {
    const first = questions.findIndex((question) => !question.user_response)
    return first >= 0 ? first : 0
  })
  const [selected, setSelected] = useState('')
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [reward, setReward] = useState(0)

  const question: StudioQuestion | undefined = questions[index]
  const allDone =
    questions.length > 0 && questions.every((item) => item.user_response)

  if (!question) {
    return (
      <article className={styles.generatedCard}>
        <span className="st-eyebrow">Exercícios extras</span>
        <EmptyGenerated message={generation.content.message} />
      </article>
    )
  }

  const answered = Boolean(question.user_response)
  const responseData = question.user_response as Record<string, unknown> | undefined
  const chosen = String(
    responseData?.selected_option ?? responseData?.choice ?? '',
  )
  const savedText = String(responseData?.text ?? '')
  const hasOptions = Boolean(question.options?.length)

  async function handleSubmit() {
    if (answered || submitting) return
    if (hasOptions && !selected) {
      setError('Escolha uma alternativa antes de confirmar.')
      return
    }
    if (!hasOptions && !text.trim()) {
      setError('Escreva sua resposta antes de confirmar.')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      const response = await studioApi.submitExercise(
        generation.id,
        index,
        hasOptions ? { selected_option: selected } : { text: text.trim() },
      )
      setReward(response.data.coins_earned)
      await onRefresh(generation.id)
      setSelected('')
      setText('')
    } catch (err: unknown) {
      setError(
        apiErrorMessage(
          err,
          'Não foi possível enviar sua resposta. Tente novamente.',
        ),
      )
    } finally {
      setSubmitting(false)
    }
  }

  function goToNext() {
    const next = questions.findIndex((item) => !item.user_response)
    if (next >= 0) {
      setIndex(next)
      setSelected('')
      setText('')
    }
  }

  return (
    <article className={styles.generatedCard}>
      <div className={styles.generatedHead}>
        <span className="st-eyebrow">Exercícios extras</span>
        <span className={styles.generatedCount}>
          {index + 1} / {questions.length}
        </span>
      </div>

      {reward > 0 && (
        <div className={styles.rewardNote} role="status">
          +{reward} <span aria-hidden="true">◆</span> Prismas por concluir os
          exercícios.
        </div>
      )}

      <h3>{question.prompt}</h3>

      {hasOptions ? (
        <div className={styles.options} role="radiogroup" aria-label={question.prompt}>
          {(question.options ?? []).map((option, optionIndex) => {
            const isChosenWrong =
              answered && question.is_correct === false && chosen === option.value
            const isRevealedCorrect =
              answered &&
              question.is_correct === false &&
              question.correct_answer === option.value
            const isChosenCorrect =
              answered && question.is_correct === true && chosen === option.value
            return (
              <label
                key={option.value}
                className={[
                  styles.option,
                  chosen === option.value ? styles.optionSelected : '',
                  isChosenWrong ? styles.optionWrong : '',
                  isRevealedCorrect || isChosenCorrect ? styles.optionCorrect : '',
                ].join(' ')}
              >
                <input
                  type="radio"
                  name={`studio-${generation.id}-${index}`}
                  value={option.value}
                  aria-label={option.label}
                  checked={chosen === option.value || selected === option.value}
                  onChange={() => {
                    setSelected(option.value)
                    setError('')
                  }}
                  disabled={answered}
                />
                <span className={styles.optionLetter}>
                  {String.fromCharCode(65 + optionIndex)}
                </span>
                <span>{option.label}</span>
              </label>
            )
          })}
        </div>
      ) : (
        <label className={styles.openAnswer}>
          <span className={styles.srOnly}>Sua resposta</span>
          <textarea
            value={answered ? savedText : text}
            onChange={(event) => {
              setText(event.target.value)
              setError('')
            }}
            rows={6}
            maxLength={2000}
            disabled={answered}
            placeholder="Escreva com as suas palavras..."
          />
        </label>
      )}

      {answered && (
        <div
          className={[
            styles.feedback,
            question.is_correct === false ? styles.feedbackWrong : styles.feedbackCorrect,
          ].join(' ')}
          role="status"
        >
          <ChatIcon size={18} />
          <div>
            <strong>
              {question.is_correct === true
                ? 'Resposta correta'
                : question.is_correct === false
                  ? 'Feedback do Mentor'
                  : 'Resposta registrada'}
            </strong>
            <p>{question.feedback ?? 'Resposta registrada.'}</p>
          </div>
        </div>
      )}

      {answered && question.is_correct === false && question.correct_answer && (
        <p className={styles.correctReveal}>
          A alternativa correta está destacada em verde.
        </p>
      )}

      {error && (
        <p className={styles.formError} role="alert">
          {error}
        </p>
      )}

      <div className={styles.exerciseFooter}>
        {questions.length > 1 ? (
          <div className={styles.exerciseNav}>
            <Button
              variant="ghost"
              onClick={() => {
                setIndex((value) => Math.max(0, value - 1))
                setSelected('')
                setText('')
              }}
              disabled={index === 0}
            >
              Anterior
            </Button>
            <Button
              variant="ghost"
              onClick={() => {
                setIndex((value) => Math.min(questions.length - 1, value + 1))
                setSelected('')
                setText('')
              }}
              disabled={index === questions.length - 1}
            >
              Próxima
            </Button>
          </div>
        ) : (
          <span />
        )}
        <div className={styles.exerciseActions}>
          {!answered && (
            <Button onClick={handleSubmit} disabled={submitting}>
              {submitting ? 'Confirmando...' : 'Confirmar resposta'}
            </Button>
          )}
          {answered && !allDone && (
            <Button onClick={goToNext}>Próxima questão</Button>
          )}
          {allDone && (
            <div className={styles.completeNote}>
              <CheckIcon size={17} />
              <span>Conjunto concluído. As respostas já estão no seu progresso.</span>
            </div>
          )}
        </div>
      </div>
    </article>
  )
}
