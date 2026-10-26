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
  ShieldIcon,
  SparkIcon,
} from '@/design-system/Icons'
import { authApi } from '@/api'
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
  const emailRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
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
      setSuccess(true)
    } catch (error) {
      setServerError(getAuthErrorMessage(error, 'Não foi possível criar sua conta. Tente novamente.'))
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <AuthShell
        mode="register"
        documentTitle="Confirme seu e-mail — Prisma.AI"
        eyebrow="Quase lá!"
        heading={<>Confirme <GradientWord>seu e-mail.</GradientWord></>}
        description="Conta criada. Verifique sua caixa de entrada para ativar o acesso e começar a Fase 1."
        visual={<RegisterVisual />}
        footer={(
          <p className={styles.crossLink}>
            Já confirmou? <Link to="/login">Entrar na plataforma</Link>
          </p>
        )}
      >
        <div className={styles.statusPanel}>
          <span className={`${styles.statusIcon} ${styles.statusIconSuccess}`} aria-hidden="true">
            <CheckIcon size={30} />
          </span>

          <p className={styles.statusCopy}>
            Enviamos um link de verificação para <span className={styles.statusEmail}>{email.trim()}</span>.
            Abra sua caixa de entrada para ativar a conta.
          </p>

          <ul className={styles.successSteps}>
            <li>
              <span aria-hidden="true"><MailIcon size={13} /></span>
              <div>
                <strong>Abra o e-mail de verificação</strong>
                <small>O link confirma que a conta é sua.</small>
              </div>
            </li>
            <li>
              <span aria-hidden="true"><CheckIcon size={13} /></span>
              <div>
                <strong>Ative sua conta</strong>
                <small>Depois da confirmação, o acesso está liberado.</small>
              </div>
            </li>
            <li>
              <span aria-hidden="true"><SparkIcon size={13} /></span>
              <div>
                <strong>Comece a Fase 1</strong>
                <small>Onboarding guiado e primeira missão: Primeiro salário.</small>
              </div>
            </li>
          </ul>

          {import.meta.env.DEV && (
            <p className={styles.devHint}>
              Ambiente local: o token de verificação aparece no log do backend com
              <code>docker compose logs backend | grep MOCK</code>
            </p>
          )}

          <div className={styles.statusActions}>
            <Button
              type="button"
              fullWidth
              className={styles.primaryAction}
              onClick={() => navigate('/login')}
            >
              Ir para o login
            </Button>
            <Link to="/" className={styles.secondaryAction}>
              Voltar ao início
            </Link>
          </div>
        </div>
      </AuthShell>
    )
  }

  return (
    <AuthShell
      mode="register"
      documentTitle="Criar conta — Prisma.AI"
      eyebrow="Seu ponto de partida"
      heading={<>Sua jornada <GradientWord>começa aqui.</GradientWord></>}
      description="Crie sua conta e comece a aprender educação financeira na prática — 6 fases, 18 missões, simulações e agentes de IA que acompanham seu progresso."
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
