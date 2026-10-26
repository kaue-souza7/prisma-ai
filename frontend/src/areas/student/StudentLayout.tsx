import { useEffect, useRef, useState } from 'react'
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { progressApi } from '@/api'
import {
  ChatIcon,
  CloseIcon,
  CompassPathIcon,
  HomeIcon,
  MenuIcon,
  SparkIcon,
  TrophyIcon,
  UserIcon,
} from '@/design-system/Icons'
import { useSessionStore } from '@/store/session'
import { CoinsDisplay } from './components/CoinsDisplay'
import { AgentAvatar, BrandMark } from './components/StudentVisuals'
import styles from './StudentLayout.module.css'

const navItems = [
  { to: '/student', label: 'Início', icon: HomeIcon, end: true },
  { to: '/student/journey', label: 'Minha jornada', shortLabel: 'Jornada', icon: CompassPathIcon },
  { to: '/student/mentor', label: 'Mentor e agentes', shortLabel: 'Mentor', icon: ChatIcon },
  { to: '/student/studio', label: 'Estúdio de Prismas', shortLabel: 'Estúdio', icon: SparkIcon },
  { to: '/student/progress', label: 'Conquistas e progresso', shortLabel: 'Progresso', icon: TrophyIcon },
  { to: '/student/profile', label: 'Meu perfil', shortLabel: 'Perfil', icon: UserIcon },
]

export function StudentLayout() {
  const user = useSessionStore((state) => state.user)
  const clearSession = useSessionStore((state) => state.clearSession)
  const coins = useSessionStore((state) => state.coins)
  const setCoins = useSessionStore((state) => state.setCoins)
  const navigate = useNavigate()
  const location = useLocation()
  const closeButtonRef = useRef<HTMLButtonElement>(null)
  const [menuOpen, setMenuOpen] = useState(false)
  const initial = user?.email?.slice(0, 1).toUpperCase() ?? 'P'

  useEffect(() => {
    setMenuOpen(false)
  }, [location.pathname])

  useEffect(() => {
    let active = true
    progressApi
      .getSummary()
      .then((response) => {
        if (active) setCoins(response.data.coins)
      })
      .catch(() => {
        // O saldo é secundário; uma falha não deve bloquear a navegação.
      })
    return () => {
      active = false
    }
  }, [setCoins])

  useEffect(() => {
    if (!menuOpen) return

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    closeButtonRef.current?.focus()

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setMenuOpen(false)
    }
    const onResize = () => {
      if (window.innerWidth <= 820) setMenuOpen(false)
    }

    window.addEventListener('keydown', onKeyDown)
    window.addEventListener('resize', onResize)

    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener('keydown', onKeyDown)
      window.removeEventListener('resize', onResize)
    }
  }, [menuOpen])

  function handleLogout() {
    clearSession()
    navigate('/login')
  }

  return (
    <div className={`student-app ${styles.shell}`}>
      <a href="#student-content" className={styles.skipLink}>
        Pular para o conteúdo
      </a>

      <aside
        id="student-sidebar"
        className={[styles.sidebar, menuOpen ? styles.sidebarOpen : ''].join(' ')}
        aria-label="Menu do estudante"
      >
        <div className={styles.sidebarTop}>
          <div className={styles.sidebarBrandRow}>
            <NavLink to="/student" className={styles.brandLink} aria-label="Prisma.AI — início">
              <BrandMark />
            </NavLink>
            <button
              ref={closeButtonRef}
              type="button"
              className={styles.closeMenu}
              aria-label="Fechar menu de navegação"
              onClick={() => setMenuOpen(false)}
            >
              <CloseIcon size={20} />
            </button>
          </div>
          <p className={styles.studentLabel}>Espaço do estudante</p>
        </div>

        <nav className={styles.nav} aria-label="Navegação principal">
          <span className={styles.navEyebrow}>Sua experiência</span>
          <ul className={styles.navList}>
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    end={item.end}
                    onClick={() => setMenuOpen(false)}
                    className={({ isActive }) =>
                      [styles.navLink, isActive ? styles.active : ''].join(' ')
                    }
                  >
                    <span className={styles.navIcon} aria-hidden="true">
                      <Icon size={18} />
                    </span>
                    <span>{item.label}</span>
                    <span className={styles.navGlow} aria-hidden="true" />
                  </NavLink>
                </li>
              )
            })}
          </ul>
        </nav>

        <div className={styles.mentorCard}>
          <div className={styles.mentorTop}>
            <AgentAvatar agent="mentor" size={42} />
            <div>
              <strong>Mentor</strong>
              <span>Seu tutor financeiro</span>
            </div>
          </div>
          <p>
            Tire dúvidas e revise conceitos. O chat já está disponível; a
            integração com IA será ativada em breve.
          </p>
          <NavLink
            to="/student/mentor"
            className={styles.mentorLink}
            onClick={() => setMenuOpen(false)}
          >
            Abrir o Mentor
            <span aria-hidden="true">→</span>
          </NavLink>
        </div>

        <div className={styles.userCard}>
          <span className={styles.avatar} aria-hidden="true">{initial}</span>
          <div className={styles.userInfo}>
            <strong>{user?.email.split('@')[0] ?? 'Estudante'}</strong>
            <span>{user?.email}</span>
          </div>
          <button type="button" className={styles.logout} onClick={handleLogout} aria-label="Sair da conta">
            Sair
          </button>
        </div>
      </aside>

      {menuOpen && (
        <button
          type="button"
          className={styles.menuBackdrop}
          aria-hidden="true"
          tabIndex={-1}
          onClick={() => setMenuOpen(false)}
        />
      )}

      <main id="student-content" className={styles.main}>
        <header className={styles.topbar}>
          <div className={styles.topbarLeft}>
            <button
              type="button"
              className={styles.menuButton}
              aria-label="Abrir menu de navegação"
              aria-expanded={menuOpen}
              aria-controls="student-sidebar"
              onClick={() => setMenuOpen(true)}
            >
              <MenuIcon size={20} />
            </button>
            <NavLink to="/student" className={styles.topbarBrand} aria-label="Prisma.AI — início">
              <BrandMark light />
            </NavLink>
            <span className={styles.topbarLabel}>Espaço do estudante</span>
          </div>
          <div className={styles.topbarRight}>
            <NavLink
              to="/student/studio"
              className={styles.coinsLink}
              aria-label="Abrir o Estúdio de Prismas"
            >
              <CoinsDisplay coins={coins} compact />
            </NavLink>
            <NavLink to="/student/profile" className={styles.topbarAvatar} aria-label="Meu perfil">
              {initial}
            </NavLink>
          </div>
        </header>
        <Outlet />
      </main>

      <nav className={styles.bottomNav} aria-label="Navegação mobile">
        {navItems.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                [styles.bottomNavItem, isActive ? styles.bottomNavActive : ''].join(' ')
              }
            >
              <span className={styles.bottomIcon} aria-hidden="true">
                <Icon size={19} />
              </span>
              <span>{item.shortLabel ?? item.label}</span>
            </NavLink>
          )
        })}
      </nav>
    </div>
  )
}
