import {
  ArrowRightIcon,
  CloseIcon,
  VolumeIcon,
} from '@/design-system/Icons'
import { AgentAvatar } from '@/areas/student/components/StudentVisuals'

const OPTIONS = [
  {
    letter: 'A',
    label: 'Um valor extra de renda que o banco oferece todo mês.',
  },
  {
    letter: 'B',
    label: 'O valor máximo que o emissor permite você usar no cartão.',
    correct: true,
  },
  {
    letter: 'C',
    label: 'O valor mínimo que você precisa pagar na fatura.',
  },
  {
    letter: 'D',
    label: 'O dinheiro que você já tem guardado no banco.',
  },
]

export function LessonScreen() {
  return (
    <div className="pl-app pl-app--lesson">
      <header className="pl-app-lesson-topbar">
        <span className="pl-app-lesson-icon">
          <CloseIcon size={16} />
        </span>

        <div className="pl-app-lesson-center">
          <span className="pl-app-lesson-brand">Prisma.AI</span>
          <div className="pl-app-lesson-progress">
            <div className="pl-app-track">
              <span style={{ width: '33%' }} />
            </div>
            <span>Etapa 3 de 9</span>
          </div>
        </div>

        <span className="pl-app-lesson-icon">
          <VolumeIcon size={16} />
        </span>
      </header>

      <main className="pl-app-lesson-stage">
        <article className="pl-app-step-card">
          <div className="pl-app-question-meta">
            <span className="pl-app-question-type">Verificação</span>
            <span className="pl-app-step-number">3/9</span>
          </div>

          <h1>O que é o limite do cartão de crédito?</h1>

          <div className="pl-app-options">
            {OPTIONS.map((option) => (
              <div
                className={`pl-app-option${option.correct ? ' is-correct' : ''}`}
                key={option.letter}
              >
                <span className="pl-app-option-letter">{option.letter}</span>
                <span>{option.label}</span>
              </div>
            ))}
          </div>

          <div className="pl-app-feedback is-correct">
            <AgentAvatar agent="mentor" size={40} />
            <div>
              <span className="pl-app-feedback-kicker">Resposta correta</span>
              <strong>Você aplicou o conceito.</strong>
              <p>
                Exato! O limite é o teto do que você pode usar. Ele não é renda
                nem dinheiro seu: tudo o que você usar vai ter que ser pago na
                fatura.
              </p>
            </div>
          </div>

          <div className="pl-app-question-footer">
            <span className="pl-app-primary-action">
              Continuar
              <ArrowRightIcon size={14} />
            </span>
          </div>
        </article>
      </main>

      <footer className="pl-app-lesson-footer">
        <span>2.2 · 5 min estimados</span>
        <span className="pl-app-lesson-agent">
          <AgentAvatar agent="mentor" size={24} />
          Mentor
        </span>
      </footer>
    </div>
  )
}
