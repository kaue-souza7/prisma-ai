import { HomeScreen } from './screens/HomeScreen'
import { ScreenViewport } from './screens/ScreenViewport'

export function ProductPreview() {
  return (
    <div className="pl-preview">
      <div className="pl-preview-topbar">
        <div className="pl-preview-dots" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <span className="pl-preview-app">app.prisma.ai/inicio</span>
        <span className="pl-preview-live">
          <span className="pl-preview-live-dot" />
          Tela do produto
        </span>
      </div>

      <ScreenViewport label="Tela de exemplo da página inicial da área do estudante">
        <HomeScreen />
      </ScreenViewport>
    </div>
  )
}
