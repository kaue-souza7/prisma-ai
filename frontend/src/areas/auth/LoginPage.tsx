import { useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/design-system'
import {
  AlertCircleIcon,
  ArrowRightIcon,
  LockIcon,
  MailIcon,
  ShieldIcon,
} from '@/design-system/Icons'
import { authApi, usersApi } from '@/api'
import { useSessionStore } from '@/store/session'
import { AuthShell, GradientWord } from './components/AuthShell'
import { LoginVisual } from './components/AuthVisuals'
import { AuthField } from './components/AuthField'
import { getAuthErrorMessage } from './apiError'
import { validateEmail, validateLoginPassword } from './validation'
import styles from './Auth.module.css'

interface FieldErrors {
  email?: string
  password?: string
}

export function LoginPage() {
  const navigate = useNavigate()
  const setSession = useSessionStore((state) => state.setSession)
  const emailRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  function clearError(field: keyof FieldErrors) {
    setFieldErrors((current) => (
      current[field] ? { ...current, [field]: undefined } : current
    ))
    setServerError('')
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    const nextErrors: FieldErrors = {
      email: validateEmail(email),
      password: validateLoginPassword(password),
    }
    setFieldErrors(nextErrors)
    setServerError('')

    if (nextErrors.email || nextErrors.password) {
      if (nextErrors.email) emailRef.current?.focus()
      else passwordRef.current?.focus()
      return
    }

    setLoading(true)
    try {
      const { data } = await authApi.login(email.trim(), password)
      const meRes = await usersApi.getMe(data.access_token)
      setSession(
        meRes.data.user,
        data.access_token,
        data.refresh_token,
        meRes.data.profile ?? null,
      )
      navigate(meRes.data.profile?.onboarding_completed === false ? '/onboarding' : '/student')
    } catch (error) {
      setServerError(getAuthErrorMessage(error, 'Não foi possível entrar. Tente novamente.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthShell
      mode="login"
      documentTitle="Entrar — Prisma.AI"
      eyebrow="Acesso seguro"
      heading={<>Bem-vindo <GradientWord>de volta.</GradientWord></>}
      description="Entre para retomar suas missões, conferir pontos e conquistas, e continuar sua jornada de educação financeira."
      visual={<LoginVisual />}
      footer={(
        <p className={styles.crossLink}>
          Ainda não tem conta? <Link to="/register">Criar conta gratuita</Link>
        </p>
      )}
    >
      <form className={styles.form} onSubmit={handleSubmit} noValidate>
        <AuthField
          ref={emailRef}
          label="E-mail"
          icon={<MailIcon size={18} />}
          type="email"
          name="email"
          value={email}
          onChange={(event) => {
            setEmail(event.target.value)
            clearError('email')
          }}
          error={fieldErrors.email}
          autoComplete="email"
          inputMode="email"
          spellCheck={false}
          placeholder="voce@exemplo.com"
          required
        />

        <AuthField
          ref={passwordRef}
          label="Senha"
          icon={<LockIcon size={18} />}
          type="password"
          name="password"
          value={password}
          onChange={(event) => {
            setPassword(event.target.value)
            clearError('password')
          }}
          error={fieldErrors.password}
          labelAction={<Link to="/forgot-password">Esqueci minha senha</Link>}
          autoComplete="current-password"
          placeholder="Sua senha"
          required
        />

        {serverError && (
          <div className={styles.alert} role="alert">
            <AlertCircleIcon size={16} />
            <span>{serverError}</span>
          </div>
        )}

        <Button type="submit" fullWidth loading={loading} className={styles.submit}>
          <span className={styles.submitContent}>
            {loading ? 'Entrando...' : 'Entrar'}
            {!loading && (
              <span className={styles.submitArrow} aria-hidden="true">
                <ArrowRightIcon size={16} />
              </span>
            )}
          </span>
        </Button>
      </form>

      <div className={styles.cardNote}>
        <ShieldIcon size={14} />
        <span>
          Acesso protegido. Nenhum dado bancário solicitado — apenas e-mail e senha.
        </span>
      </div>
    </AuthShell>
  )
}
