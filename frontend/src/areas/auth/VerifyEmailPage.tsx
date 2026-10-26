import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { Button } from '@/design-system'
import {
  AlertTriangleIcon,
  CheckIcon,
  SpinnerIcon,
} from '@/design-system/Icons'
import { authApi } from '@/api'
import { AuthShell, GradientWord } from './components/AuthShell'
import { SupportVisual } from './components/AuthVisuals'
import { getAuthErrorMessage } from './apiError'
import styles from './Auth.module.css'

type Status = 'loading' | 'success' | 'error'

const content = {
  loading: {
    documentTitle: 'Verificando e-mail — Prisma.AI',
    eyebrow: 'Verificação de e-mail',
    heading: <>Confirmando <GradientWord>seu acesso.</GradientWord></>,
    description: 'Estamos validando o link de verificação com segurança. Isso leva só um instante.',
  },
  success: {
    documentTitle: 'E-mail verificado — Prisma.AI',
    eyebrow: 'E-mail confirmado',
    heading: <>Tudo certo, <GradientWord>conta ativada.</GradientWord></>,
    description: 'Seu e-mail foi confirmado. O próximo passo é entrar e começar sua jornada.',
  },
  error: {
    documentTitle: 'Verificação não concluída — Prisma.AI',
    eyebrow: 'Verificação de e-mail',
    heading: <>Não conseguimos <GradientWord>confirmar.</GradientWord></>,
    description: 'O link pode ter expirado ou já ter sido utilizado. Você pode tentar novamente pelo login.',
  },
} as const

export function VerifyEmailPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [status, setStatus] = useState<Status>('loading')
  const [message, setMessage] = useState('Validando seu e-mail...')
  const didRequest = useRef(false)
  const token = searchParams.get('token')
  const current = content[status]

  useEffect(() => {
    if (didRequest.current) return
    didRequest.current = true

    if (!token) {
      setStatus('error')
      setMessage('Link de verificação inválido: token não informado.')
      return
    }

    authApi
      .verifyEmail(token)
      .then((response) => {
        setStatus('success')
        setMessage(response.data.message)
      })
      .catch((err: unknown) => {
        setStatus('error')
        setMessage(getAuthErrorMessage(err, 'Não foi possível verificar o e-mail.'))
      })
  }, [token])

  return (
    <AuthShell
      mode="support"
      documentTitle={current.documentTitle}
      eyebrow={current.eyebrow}
      heading={current.heading}
      description={current.description}
      visual={<SupportVisual />}
    >
      <div className={styles.statusPanel}>
        <span
          className={[
            styles.statusIcon,
            status === 'success'
              ? styles.statusIconSuccess
              : status === 'error'
                ? styles.statusIconError
                : styles.statusIconLoading,
          ].join(' ')}
          aria-hidden="true"
        >
          {status === 'success' && <CheckIcon size={30} />}
          {status === 'error' && <AlertTriangleIcon size={30} />}
          {status === 'loading' && <SpinnerIcon size={30} />}
        </span>

        <p
          className={styles.statusCopy}
          role={status === 'error' ? 'alert' : 'status'}
          aria-live="polite"
        >
          {message}
        </p>

        {status !== 'loading' && (
          <div className={styles.statusActions}>
            <Button
              type="button"
              fullWidth
              className={styles.primaryAction}
              onClick={() => navigate('/login')}
            >
              Voltar ao login
            </Button>
            <Link to="/" className={styles.secondaryAction}>
              Ir para o início
            </Link>
          </div>
        )}
      </div>
    </AuthShell>
  )
}
