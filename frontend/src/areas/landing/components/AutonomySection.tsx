import { CompassIcon, ShieldIcon, TargetIcon } from '@/design-system/Icons'
import { Reveal } from './primitives'

export function AutonomySection() {
  return (
    <section className="pl-section pl-autonomy">
      <div className="pl-autonomy-bg" aria-hidden="true">
        <div className="pl-autonomy-horizon" />
        <div className="pl-autonomy-sun" />
        <div className="pl-autonomy-rays" />
      </div>

      <div className="pl-container pl-autonomy-inner">
        <div className="pl-autonomy-heading">
          <Reveal>
            <p className="pl-eyebrow">
              <span className="pl-eyebrow-dot" aria-hidden="true" />
              O que você leva da jornada
            </p>
          </Reveal>
          <Reveal delay={0.08}>
            <h2>
              Conhecimento financeiro real.
              <span>Autonomia para o dia a dia.</span>
            </h2>
          </Reveal>
        </div>

        <div className="pl-autonomy-side">
          <Reveal delay={0.14}>
            <p>
              Entender salário, crédito, juros, poupança e golpes digitais não é teoria —
              é o que você vai praticar em cenários reais ao longo das trilhas.
            </p>
          </Reveal>
          <Reveal delay={0.2}>
            <div className="pl-autonomy-pillars">
              <span><CompassIcon size={15} /> Clareza</span>
              <span><ShieldIcon size={15} /> Segurança</span>
              <span><TargetIcon size={15} /> Autonomia</span>
            </div>
          </Reveal>
        </div>

        <Reveal className="pl-autonomy-path" delay={0.16}>
          <div className="pl-autonomy-path-line" aria-hidden="true" />
          <div className="pl-autonomy-milestone">
            <span className="pl-autonomy-dot is-done" />
            <small>Começar</small>
            <strong>Onboarding e Trilha 1</strong>
          </div>
          <div className="pl-autonomy-milestone">
            <span className="pl-autonomy-dot is-current" />
            <small>Praticar</small>
            <strong>Missões e simulações</strong>
          </div>
          <div className="pl-autonomy-milestone">
            <span className="pl-autonomy-dot" />
            <small>Conquistar</small>
            <strong>Autonomia financeira</strong>
          </div>
        </Reveal>
      </div>
    </section>
  )
}
