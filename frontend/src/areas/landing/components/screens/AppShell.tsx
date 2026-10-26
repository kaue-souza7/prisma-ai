import type { ReactNode } from 'react'
import {
  ChatIcon,
  CompassPathIcon,
  HomeIcon,
  TrophyIcon,
  UserIcon,
} from '@/design-system/Icons'
import { AgentAvatar, BrandMark } from '@/areas/student/components/StudentVisuals'
import { PREVIEW_STUDENT } from './studentPreviewData'

type ActivePage = 'home' | 'journey' | 'progress'

const NAV_ITEMS: Array<{
  key: ActivePage | 'mentor' | 'profile'
  label: string
  icon: typeof HomeIcon
}> = [
  { key: 'home', label: 'Início', icon: HomeIcon },
  { key: 'journey', label: 'Minha jornada', icon: CompassPathIcon },
  { key: 'mentor', label: 'Mentor e agentes', icon: ChatIcon },
  { key: 'progress', label: 'Conquistas e progresso', icon: TrophyIcon },
  { key: 'profile', label: 'Meu perfil', icon: UserIcon },
]

export function AppShell({
  active,
  children,
}: {
  active: ActivePage
  children: ReactNode
}) {
  return (
    <div className="pl-app">
      <aside className="pl-app-sidebar">
        <div className="pl-app-brand">
          <BrandMark />
          <span className="pl-app-student-label">Espaço do estudante</span>
        </div>

        <div className="pl-app-nav">
          <span className="pl-app-nav-eyebrow">Sua experiência</span>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon
            return (
              <span
                key={item.key}
                className={`pl-app-nav-link${item.key === active ? ' is-active' : ''}`}
              >
                <span className="pl-app-nav-icon">
                  <Icon size={17} />
                </span>
                {item.label}
                <span className="pl-app-nav-glow" />
              </span>
            )
          })}
        </div>

        <div className="pl-app-mentor-card">
          <div className="pl-app-mentor-head">
            <AgentAvatar agent="mentor" size={38} />
            <div>
              <strong>Mentor</strong>
              <span>Seu tutor financeiro</span>
            </div>
          </div>
          <p>
            Tire dúvidas e revise conceitos. A conversa com IA será ativada em
            breve.
          </p>
          <span className="pl-app-mentor-link">
            Conhecer os agentes <span aria-hidden="true">→</span>
          </span>
        </div>

        <div className="pl-app-user">
          <span className="pl-app-avatar" aria-hidden="true">M</span>
          <span className="pl-app-user-info">
            <strong>{PREVIEW_STUDENT.handle}</strong>
            <span>{PREVIEW_STUDENT.email}</span>
          </span>
          <span className="pl-app-logout">Sair</span>
        </div>
      </aside>

      <main className="pl-app-main">{children}</main>
    </div>
  )
}
