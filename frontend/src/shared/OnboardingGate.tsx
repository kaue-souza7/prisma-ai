import { useEffect, useRef, useState } from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { usersApi } from '@/api'
import { Button } from '@/design-system'
import { useSessionStore } from '@/store/session'
import styles from '@/areas/student/Student.module.css'

/**
 * Garante que o estudante conclua o onboarding antes de entrar na jornada.
 * O backend é a fonte da verdade; o store guarda o perfil apenas como cache.
 */
export function OnboardingGate() {
  const profile = useSessionStore((state) => state.profile)
  const setProfile = useSessionStore((state) => state.setProfile)
  const location = useLocation()
  const didLoad = useRef(false)
  const [loading, setLoading] = useState(profile === null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (profile !== null || didLoad.current) return
    didLoad.current = true

    usersApi
      .getMe()
      .then((response) => {
        setProfile(response.data.profile)
      })
      .catch(() => {
        setError('Não foi possível carregar seu perfil. Tente novamente.')
      })
      .finally(() => setLoading(false))
  }, [profile, setProfile])

  if (loading) {
    return <div className={`student-app ${styles.loading}`}>Carregando seu perfil...</div>
  }

  if (error) {
    return (
      <div className={`student-app ${styles.page}`}>
        <div className={styles.feedbackError} role="alert">
          <p>{error}</p>
          <Button onClick={() => window.location.reload()}>Tentar novamente</Button>
        </div>
      </div>
    )
  }

  if (!profile || !profile.onboarding_completed) {
    return (
      <Navigate
        to="/onboarding"
        replace
        state={{ from: location.pathname }}
      />
    )
  }

  return <Outlet />
}
