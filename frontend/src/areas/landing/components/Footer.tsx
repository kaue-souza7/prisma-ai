import { Link } from 'react-router-dom'
import { Logo } from '@/design-system/brand/Logo'

const navLinks = [
  { href: '#inicio', label: 'Início' },
  { href: '#como-funciona', label: 'Como funciona' },
  { href: '#experiencia', label: 'Experiência' },
  { href: '#sobre', label: 'Sobre' },
]

export function Footer() {
  return (
    <footer className="pl-footer">
      <div className="pl-container">
        <div className="pl-footer-main">
          <div className="pl-footer-brand">
            <Logo />
            <p>
              Seis fases de educação financeira gamificada — do primeiro salário à proteção digital. Aprenda fazendo, avance por competências.
            </p>
          </div>

          <div className="pl-footer-column">
            <span className="pl-footer-label">Navegar</span>
            {navLinks.map((link) => (
              <a key={link.href} href={link.href}>{link.label}</a>
            ))}
          </div>

          <div className="pl-footer-column">
            <span className="pl-footer-label">Acesso</span>
            <Link to="/login">Entrar</Link>
            <Link to="/register">Cadastrar-se</Link>
            <Link to="/forgot-password">Recuperar senha</Link>
          </div>

          <div className="pl-footer-column pl-footer-legal">
            <span className="pl-footer-label">Institucional</span>
            <span title="Documento em preparação">Política de Privacidade <small>em breve</small></span>
            <span title="Documento em preparação">Termos de Uso <small>em breve</small></span>
          </div>
        </div>

        <div className="pl-footer-bottom">
          <span>© {new Date().getFullYear()} Prisma.AI. Todos os direitos reservados.</span>
          <span className="pl-footer-signature">
            Sua jornada. Suas escolhas. Seu futuro.
          </span>
        </div>
      </div>
    </footer>
  )
}
