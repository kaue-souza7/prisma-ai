import { useEffect, useRef, useState } from 'react'
import { conversationsApi } from '@/api'
import type { MentorMessage } from '@/types/student'
import { AgentAvatar } from './StudentVisuals'
import { ArrowRightIcon, CheckIcon } from '@/design-system/Icons'
import styles from './MentorChat.module.css'

interface MentorChatProps {
  missionId?: number
  compact?: boolean
  initialQuestion?: string
  onClose?: () => void
}

function nowIso() {
  return new Date().toISOString()
}

function formatTime(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return ''
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

export function MentorChat({
  missionId,
  compact = false,
  initialQuestion = '',
  onClose,
}: MentorChatProps) {
  const [messages, setMessages] = useState<MentorMessage[]>([])
  const [input, setInput] = useState(initialQuestion)
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const [status, setStatus] = useState<'available' | 'preparing' | 'unavailable' | string>('preparing')
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [opening, setOpening] = useState('')
  const listRef = useRef<HTMLDivElement | null>(null)
  const inputRef = useRef<HTMLTextAreaElement | null>(null)

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')
    Promise.all([
      conversationsApi.getMentorContext(missionId),
      conversationsApi.getMentorHistory(),
    ])
      .then(([contextResponse, historyResponse]) => {
        if (!active) return
        const context = contextResponse.data
        setStatus(context.status)
        setSuggestions(context.suggestions)
        setOpening(context.opening_message)

        const conversations = historyResponse.data as Array<{
          mission_id: number | null
          messages: MentorMessage[]
        }>
        const matching = missionId
          ? conversations.find((item) => item.mission_id === missionId)
          : conversations[0]
        if (matching?.messages?.length) {
          setMessages(
            matching.messages.filter(
              (message) => message.role === 'user' || message.role === 'assistant',
            ),
          )
        }
      })
      .catch(() => {
        if (active) {
          setError('Não foi possível carregar a conversa agora.')
          setStatus('unavailable')
        }
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [missionId])

  useEffect(() => {
    const node = listRef.current
    if (node) node.scrollTop = node.scrollHeight
  }, [messages, sending, loading])

  async function send(content?: string) {
    const text = (content ?? input).trim()
    if (!text || sending) return
    setInput('')
    setError('')
    setSending(true)
    setMessages((current) => [
      ...current,
      { role: 'user', content: text, timestamp: nowIso() },
    ])
    try {
      const response = await conversationsApi.chatWithMentor(text, missionId)
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: response.data.content,
          timestamp: response.data.timestamp ?? nowIso(),
          status: response.data.status,
        },
      ])
      setStatus(response.data.status ?? status)
      if (response.data.suggestions?.length) {
        setSuggestions(response.data.suggestions)
      }
    } catch {
      setError('Não foi possível enviar sua mensagem. Tente novamente.')
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content:
            'Não consegui responder agora. Sua mensagem pode não ter sido salva. Tente novamente em instantes.',
          timestamp: nowIso(),
          status: 'unavailable',
        },
      ])
    } finally {
      setSending(false)
      inputRef.current?.focus()
    }
  }

  function applySuggestion(suggestion: string) {
    setInput(suggestion)
    inputRef.current?.focus()
  }

  const visibleMessages = messages.length
    ? messages
    : opening
      ? [
          {
            role: 'assistant' as const,
            content: opening,
            timestamp: nowIso(),
          },
        ]
      : []

  return (
    <div className={[styles.chat, compact ? styles.compact : ''].join(' ')}>
      <header className={styles.chatHeader}>
        <AgentAvatar agent="mentor" size={compact ? 36 : 44} />
        <div className={styles.chatIdentity}>
          <strong>Mentor</strong>
          <span>
            {status === 'available'
              ? 'Conectado ao tutor'
              : status === 'unavailable'
                ? 'Temporariamente indisponível'
                : 'IA em preparação'}
          </span>
        </div>
        <span
          className={[
            styles.statusDot,
            status === 'available'
              ? styles.statusAvailable
              : status === 'unavailable'
                ? styles.statusUnavailable
                : styles.statusPreparing,
          ].join(' ')}
          title={
            status === 'available'
              ? 'Mentor conectado'
              : status === 'unavailable'
                ? 'Mentor indisponível'
                : 'Integração com IA em preparação'
          }
        />
        {onClose && (
          <button type="button" className={styles.close} onClick={onClose} aria-label="Fechar conversa">
            ×
          </button>
        )}
      </header>

      {status !== 'available' && (
        <p className={styles.notice} role="status">
          {status === 'unavailable'
            ? 'O Mentor está temporariamente indisponível. O conteúdo de apoio das missões continua acessível.'
            : 'A integração com a IA ainda está em preparação. Suas mensagens ficam salvas e o conteúdo de apoio continua nas missões.'}
        </p>
      )}

      <div
        className={styles.messages}
        ref={listRef}
        role="log"
        aria-live="polite"
        aria-label="Conversa com o Mentor"
      >
        {loading && <p className={styles.loading}>Carregando a conversa...</p>}
        {!loading &&
          visibleMessages.map((message, index) => (
            <div
              key={`${message.timestamp}-${index}`}
              className={[
                styles.message,
                message.role === 'user' ? styles.messageUser : styles.messageAssistant,
              ].join(' ')}
            >
              {message.role === 'assistant' && <AgentAvatar agent="mentor" size={28} />}
              <div className={styles.bubble}>
                <p>{message.content}</p>
                <span>{formatTime(message.timestamp)}</span>
              </div>
            </div>
          ))}
        {sending && (
          <div className={`${styles.message} ${styles.messageAssistant}`}>
            <AgentAvatar agent="mentor" size={28} />
            <div className={styles.bubble}>
              <p className={styles.thinking}>Preparando uma resposta...</p>
            </div>
          </div>
        )}
      </div>

      {error && (
        <p className={styles.error} role="alert">
          {error}
        </p>
      )}

      {suggestions.length > 0 && (
        <div className={styles.suggestions} aria-label="Perguntas sugeridas">
          {suggestions.slice(0, compact ? 2 : 4).map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              className={styles.suggestion}
              onClick={() => applySuggestion(suggestion)}
              disabled={sending}
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      <form
        className={styles.composer}
        onSubmit={(event) => {
          event.preventDefault()
          void send()
        }}
      >
        <label className={styles.srOnly} htmlFor={`mentor-message-${missionId ?? 'geral'}`}>
          Sua mensagem para o Mentor
        </label>
        <textarea
          id={`mentor-message-${missionId ?? 'geral'}`}
          ref={inputRef}
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              void send()
            }
          }}
          maxLength={2000}
          rows={compact ? 2 : 3}
          placeholder="Escreva sua dúvida com as suas palavras..."
          disabled={sending}
        />
        <button type="submit" className={styles.send} disabled={!input.trim() || sending}>
          {sending ? 'Enviando...' : 'Enviar'}
          {!sending && <ArrowRightIcon size={15} />}
        </button>
      </form>

      <p className={styles.footnote}>
        <CheckIcon size={12} />
        O Mentor orienta o raciocínio. Pontos e desbloqueios continuam com o backend.
      </p>
    </div>
  )
}
