import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { CloseIcon, MenuIcon } from '@/design-system/Icons'
import { Logo } from '@/design-system/brand/Logo'

const links = [
  { href: '#inicio', label: 'Início' },
  { href: '#sobre', label: 'Sobre' },
  { href: '#impacto', label: 'Impacto' },
  { href: '#como-funciona', label: 'Como funciona' },
  { href: '#experiencia', label: 'Experiência' },
]

export function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const headerRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 18)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    if (!open) return
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false)
    }
    const onPointerDown = (event: PointerEvent) => {
      if (!headerRef.current?.contains(event.target as Node)) setOpen(false)
    }
    window.addEventListener('keydown', onKeyDown)
    window.addEventListener('pointerdown', onPointerDown)
    return () => {
      window.removeEventListener('keydown', onKeyDown)
      window.removeEventListener('pointerdown', onPointerDown)
    }
  }, [open])

  return (
    <header ref={headerRef} className={`pl-nav ${scrolled ? 'is-scrolled' : ''}`}>
      <div className="pl-container pl-nav-inner">
        <Logo />

        <nav className="pl-nav-links" aria-label="Navegação da landing page">
          {links.map((link) => (
            <a key={link.href} href={link.href} className="pl-nav-link">
              {link.label}
            </a>
          ))}
        </nav>

        <div className="pl-nav-actions">
          <Link to="/login" className="pl-btn pl-btn--ghost pl-nav-login">
            Entrar
          </Link>
          <Link to="/register" className="pl-btn pl-btn--primary pl-btn--compact">
            Cadastrar-se
          </Link>
          <button
            type="button"
            className="pl-menu-button"
            aria-label={open ? 'Fechar menu de navegação' : 'Abrir menu de navegação'}
            aria-expanded={open}
            aria-controls="pl-nav-menu"
            onClick={() => setOpen((value) => !value)}
          >
            {open ? <CloseIcon size={22} /> : <MenuIcon size={22} />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            id="pl-nav-menu"
            className="pl-nav-menu"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.22 }}
          >
            <div className="pl-container">
              <nav aria-label="Menu de navegação">
                {links.map((link, index) => (
                  <motion.a
                    key={link.href}
                    href={link.href}
                    className="pl-nav-menu-link"
                    onClick={() => setOpen(false)}
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <span>0{index + 1}</span>
                    {link.label}
                  </motion.a>
                ))}
              </nav>
              <div className="pl-nav-menu-auth">
                <Link to="/login" className="pl-btn pl-btn--secondary" onClick={() => setOpen(false)}>
                  Entrar
                </Link>
                <Link to="/register" className="pl-btn pl-btn--primary" onClick={() => setOpen(false)}>
                  Cadastrar-se
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
