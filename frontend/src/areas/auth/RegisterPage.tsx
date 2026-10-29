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
import { RegisterVisual } from './components/AuthVisuals'
import { AuthField } from './components/AuthField'
import { PasswordStrength } from './components/PasswordStrength'
import { getAuthErrorMessage } from './apiError'
import { validateEmail, validateNewPassword } from './validation'
import styles from './Auth.module.css'

interface FieldErrors {
  email?: string
  password?: string
}

export function RegisterPage() {
  const navigate = useNavigate()
  const setSession = useSessionStore((state) => state.setSession)
  const emailRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)
  const passwordStrengthId = 'register-password-strength'

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
      password: validateNewPassword(password),
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
      await authApi.register(email.trim(), password)
      // Cadastro com acesso direto: autentica em seguida e entra na jornada.
      const { data } = await authApi.login(email.trim(), password)
      const meRes = await usersApi.getMe(data.access_token)
      setSession(
        meRes.data.user,
        data.access_token,
        data.refresh_token,
        meRes.data.profile ?? null,
      )
      navigate(
        meRes.data.profile?.onboarding_completed === false ? '/onboarding' : '/student',
      )
    } catch (error) {
      setServerError(getAuthErrorMessage(error, 'Não foi possível criar sua conta. Tente novamente.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthShell
      mode="register"
      documentTitle="Criar conta — Prisma.AI"
      eyebrow="Seu ponto de partida"
      heading={<>Sua jornada <GradientWord>começa aqui.</GradientWord></>}
      description="Crie sua conta e comece a aprender educação financeira na prática — 12 trilhas, 45 missões, simulações e agentes de IA que acompanham seu progresso."
      visual={<RegisterVisual />}
      footer={(
        <p className={styles.crossLink}>
          Já tem uma conta? <Link to="/login">Entrar na plataforma</Link>
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
          autoComplete="new-password"
          placeholder="Crie uma senha segura"
          extraDescribedBy={passwordStrengthId}
          required
        />

        <PasswordStrength password={password} id={passwordStrengthId} />

        {serverError && (
          <div className={styles.alert} role="alert">
            <AlertCircleIcon size={16} />
            <span>{serverError}</span>
          </div>
        )}

        <Button type="submit" fullWidth loading={loading} className={styles.submit}>
          <span className={styles.submitContent}>
            {loading ? 'Criando sua conta...' : 'Criar minha conta'}
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
          Só e-mail e senha. Nenhum dado bancário solicitado. Simulações sempre em cenários fictícios.
        </span>
      </div>
    </AuthShell>
  )
}
