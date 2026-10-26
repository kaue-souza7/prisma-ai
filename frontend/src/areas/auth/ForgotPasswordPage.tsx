import { useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/design-system'
import {
  AlertCircleIcon,
  ArrowRightIcon,
  CheckIcon,
  LockIcon,
  MailIcon,
} from '@/design-system/Icons'
import { authApi } from '@/api'
import { AuthField } from './components/AuthField'
import { AuthShell, GradientWord } from './components/AuthShell'
import { SupportVisual } from './components/AuthVisuals'
import { getAuthErrorMessage } from './apiError'
import { validateEmail } from './validation'
import styles from './Auth.module.css'

export function ForgotPasswordPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [fieldError, setFieldError] = useState<string>()
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [sent, setSent] = useState(false)
  const emailRef = useRef<HTMLInputElement>(null)

  function handleEmailChange(value: string) {
    setEmail(value)
    if (fieldError) setFieldError(undefined)
    if (error) setError('')
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const emailError = validateEmail(email)
    if (emailError) {
      setFieldError(emailError)
      emailRef.current?.focus()
      return
    }

    setError('')
    setLoading(true)

    try {
      const response = await authApi.requestPasswordReset(email.trim())
      setMessage(response.data.message)
      setSent(true)
    } catch (err: unknown) {
      setError(getAuthErrorMessage(err, 'Não foi possível solicitar a recuperação.'))
    } finally {
      setLoading(false)
    }
  }

  function handleTryAnotherEmail() {
    setSent(false)
    setMessage('')
    setEmail('')
    window.setTimeout(() => emailRef.current?.focus(), 0)
  }

  if (sent) {
    return (
      <AuthShell
        mode="support"
        documentTitle="Instruções enviadas — Prisma.AI"
        eyebrow="Verifique seu e-mail"
        heading={<>Confira sua <GradientWord>caixa de entrada.</GradientWord></>}
        description="Confira sua caixa de entrada e siga as instruções para criar uma nova senha."
        visual={<SupportVisual />}
      >
        <div className={styles.statusPanel}>
          <span className={`${styles.statusIcon} ${styles.statusIconSuccess}`} aria-hidden="true">
            <CheckIcon size={30} />
          </span>

          <p className={styles.statusCopy}>
            E-mail informado: <span className={styles.statusEmail}>{email.trim()}</span>.
            Lembre de conferir também a pasta de spam ou lixo eletrônico.
          </p>

          {message && (
            <div className={styles.successNote} role="status">
              <CheckIcon size={15} />
              <span>{message}</span>
            </div>
          )}

          <div className={styles.statusActions}>
            <Button
              type="button"
              fullWidth
              className={styles.primaryAction}
              onClick={() => navigate('/login')}
            >
              Voltar ao login
            </Button>
            <button
              type="button"
              className={styles.secondaryAction}
              onClick={handleTryAnotherEmail}
            >
              Enviar para outro e-mail
            </button>
          </div>
        </div>
      </AuthShell>
    )
  }

  return (
    <AuthShell
      mode="support"
      documentTitle="Recuperar senha — Prisma.AI"
      eyebrow="Recuperação de acesso"
      heading={<>Vamos trazer você <GradientWord>de volta.</GradientWord></>}
      description="Informe o e-mail da sua conta. Enviaremos um link seguro para você criar uma nova senha."
      visual={<SupportVisual />}
      footer={
        <p className={styles.crossLink}>
          Lembrou a senha? <Link to="/login">Voltar ao login</Link>
        </p>
      }
    >
      <form className={styles.form} onSubmit={handleSubmit} noValidate>
        <AuthField
          ref={emailRef}
          label="E-mail da conta"
          icon={<MailIcon size={18} />}
          type="email"
          name="email"
          value={email}
          onChange={(event) => handleEmailChange(event.target.value)}
          autoComplete="email"
          placeholder="voce@email.com"
          inputMode="email"
          spellCheck={false}
          error={fieldError}
          hint="Use o mesmo e-mail informado no seu cadastro."
          required
        />

        {error && (
          <div className={styles.alert} role="alert">
            <AlertCircleIcon size={16} />
            <span>{error}</span>
          </div>
        )}

        <Button type="submit" fullWidth loading={loading} className={styles.submit}>
          <span className={styles.submitContent}>
            {loading ? 'Enviando instruções...' : 'Enviar instruções'}
            {!loading && (
              <span className={styles.submitArrow} aria-hidden="true">
                <ArrowRightIcon size={16} />
              </span>
            )}
          </span>
        </Button>
      </form>

      <div className={styles.cardNote}>
        <LockIcon size={14} />
        <span>Por segurança, não informamos se um e-mail está cadastrado.</span>
      </div>
    </AuthShell>
  )
}
