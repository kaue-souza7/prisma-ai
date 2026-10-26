import { useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { Button } from '@/design-system'
import {
  AlertCircleIcon,
  AlertTriangleIcon,
  ArrowRightIcon,
  CheckIcon,
  KeyIcon,
  LockIcon,
} from '@/design-system/Icons'
import { authApi } from '@/api'
import { AuthField } from './components/AuthField'
import { AuthShell, GradientWord } from './components/AuthShell'
import { SupportVisual } from './components/AuthVisuals'
import { PasswordStrength } from './components/PasswordStrength'
import { getAuthErrorMessage } from './apiError'
import { validateNewPassword } from './validation'
import styles from './Auth.module.css'

export function ResetPasswordPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token') || ''
  const [password, setPassword] = useState('')
  const [fieldError, setFieldError] = useState<string>()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const passwordRef = useRef<HTMLInputElement>(null)

  function handlePasswordChange(value: string) {
    setPassword(value)
    if (fieldError) setFieldError(undefined)
    if (error) setError('')
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const passwordError = validateNewPassword(password)
    if (passwordError) {
      setFieldError(passwordError)
      passwordRef.current?.focus()
      return
    }

    setError('')
    setLoading(true)

    try {
      await authApi.confirmPasswordReset(token, password)
      setSuccess(true)
    } catch (err: unknown) {
      setError(getAuthErrorMessage(err, 'Não foi possível redefinir a senha.'))
    } finally {
      setLoading(false)
    }
  }

  if (!token) {
    return (
      <AuthShell
        mode="support"
        documentTitle="Link inválido — Prisma.AI"
        eyebrow="Redefinição de senha"
        heading={<>Esse link <GradientWord>não é válido.</GradientWord></>}
        description="O link de redefinição não contém um token válido ou pode ter expirado."
        visual={<SupportVisual />}
      >
        <div className={styles.statusPanel}>
          <span className={`${styles.statusIcon} ${styles.statusIconError}`} aria-hidden="true">
            <AlertTriangleIcon size={30} />
          </span>

          <p className={styles.statusCopy}>
            Solicite um novo link para continuar com segurança. Por proteção, links de
            redefinição têm validade limitada.
          </p>

          <div className={styles.statusActions}>
            <Button
              type="button"
              fullWidth
              className={styles.primaryAction}
              onClick={() => navigate('/forgot-password')}
            >
              Solicitar novo link
            </Button>
            <Link to="/login" className={styles.secondaryAction}>
              Voltar ao login
            </Link>
          </div>
        </div>
      </AuthShell>
    )
  }

  if (success) {
    return (
      <AuthShell
        mode="support"
        documentTitle="Senha redefinida — Prisma.AI"
        eyebrow="Tudo certo"
        heading={<>Seu acesso foi <GradientWord>renovado.</GradientWord></>}
        description="Sua senha foi alterada com sucesso. Você já pode entrar com a nova senha."
        visual={<SupportVisual />}
      >
        <div className={styles.statusPanel}>
          <span className={`${styles.statusIcon} ${styles.statusIconSuccess}`} aria-hidden="true">
            <CheckIcon size={30} />
          </span>

          <p className={styles.statusCopy}>
            A nova senha está ativa. Use-a para entrar e retomar sua jornada de onde parou.
          </p>

          <div className={styles.statusActions}>
            <Button
              type="button"
              fullWidth
              className={styles.primaryAction}
              onClick={() => navigate('/login')}
            >
              Entrar na plataforma
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
      mode="support"
      documentTitle="Nova senha — Prisma.AI"
      eyebrow="Defina uma nova senha"
      heading={<>Um novo acesso, <GradientWord>do seu jeito.</GradientWord></>}
      description="Crie uma senha forte para proteger sua conta e continuar sua jornada de onde parou."
      visual={<SupportVisual />}
      footer={
        <p className={styles.crossLink}>
          Lembrou a senha? <Link to="/login">Voltar ao login</Link>
        </p>
      }
    >
      <form className={styles.form} onSubmit={handleSubmit} noValidate>
        <AuthField
          ref={passwordRef}
          label="Nova senha"
          icon={<KeyIcon size={18} />}
          type="password"
          name="new_password"
          value={password}
          onChange={(event) => handlePasswordChange(event.target.value)}
          autoComplete="new-password"
          placeholder="Uma senha segura"
          error={fieldError}
          extraDescribedBy="reset-password-strength"
          required
        />

        <PasswordStrength password={password} id="reset-password-strength" />

        {error && (
          <div className={styles.alert} role="alert">
            <AlertCircleIcon size={16} />
            <span>{error}</span>
          </div>
        )}

        <Button type="submit" fullWidth loading={loading} className={styles.submit}>
          <span className={styles.submitContent}>
            {loading ? 'Salvando nova senha...' : 'Salvar nova senha'}
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
        <span>
          Mínimo de 8 caracteres, com uma letra maiúscula e um número. Sua senha não é
          armazenada em texto puro.
        </span>
      </div>
    </AuthShell>
  )
}
