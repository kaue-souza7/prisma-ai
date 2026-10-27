import {
  ChartIcon,
  CheckIcon,
  CompassPathIcon,
  LayersIcon,
  SparkIcon,
  TargetIcon,
} from '@/design-system/Icons'
import { Reveal, SectionHeading, SpotlightCard } from './primitives'

export function SolutionSection() {
  return (
    <section className="pl-section pl-solution" id="sobre">
      <div className="pl-section-glow pl-section-glow--left" aria-hidden="true" />
      <div className="pl-container">
        <SectionHeading
          eyebrow="O que é o Prisma.AI"
          title={<>Da teoria à prática: <span className="pl-gradient-text">você aprende fazendo.</span></>}
          description="Doze trilhas de educação financeira com missões reais, simulações e feedback contextual. Cada trilha desenvolve competências que se acumulam ao longo da jornada."
        />

        <div className="pl-bento">
          <Reveal className="pl-bento-cell pl-bento-cell--wide">
            <SpotlightCard className="pl-bento-card pl-bento-card--journey">
              <div className="pl-card-topline">
                <span className="pl-icon-box pl-icon-box--purple"><CompassPathIcon /></span>
                <span className="pl-card-index">01 / JORNADA</span>
              </div>
              <div className="pl-journey-copy">
                <h3>Doze trilhas. Uma progressão com propósito.</h3>
                <p>
                  Do primeiro salário à proteção digital, cada trilha desenvolve
                  competências financeiras concretas — com missões, simulações e critérios claros de conclusão.
                </p>
              </div>
              <div className="pl-mini-journey" aria-hidden="true">
                <div className="pl-mini-phase is-done">
                  <span><CheckIcon size={11} /></span>
                  <small>01</small>
                  <strong>Primeiro salário</strong>
                </div>
                <div className="pl-mini-connector is-done" />
                <div className="pl-mini-phase is-current">
                  <span><CompassPathIcon size={12} /></span>
                  <small>02</small>
                  <strong>Dinheiro digital</strong>
                </div>
                <div className="pl-mini-connector" />
                <div className="pl-mini-phase">
                  <span>03</span>
                  <small>03</small>
                  <strong>Por que poupar</strong>
                </div>
                <div className="pl-mini-connector" />
                <div className="pl-mini-phase is-muted">
                  <span>04</span>
                  <small>04</small>
                  <strong>Juros</strong>
                </div>
              </div>
            </SpotlightCard>
          </Reveal>

          <Reveal className="pl-bento-cell pl-bento-cell--tall" delay={0.08}>
            <SpotlightCard className="pl-bento-card pl-bento-card--personal">
              <div className="pl-card-topline">
                <span className="pl-icon-box pl-icon-box--blue"><TargetIcon /></span>
                <span className="pl-card-index">02 / CONTEXTO</span>
              </div>
              <h3>Adaptado ao seu ponto de partida.</h3>
              <p>
                O onboarding identifica seus objetivos e nível de conhecimento.
                As recomendações se ajustam à sua evolução, não a uma resposta isolada.
              </p>
              <div className="pl-orbit-visual" aria-hidden="true">
                <span className="pl-orbit-ring pl-orbit-ring--one" />
                <span className="pl-orbit-ring pl-orbit-ring--two" />
                <span className="pl-orbit-core"><SparkIcon size={20} /></span>
                <span className="pl-orbit-node pl-orbit-node--one" />
                <span className="pl-orbit-node pl-orbit-node--two" />
                <span className="pl-orbit-node pl-orbit-node--three" />
              </div>
            </SpotlightCard>
          </Reveal>

          <Reveal className="pl-bento-cell" delay={0.04}>
            <SpotlightCard className="pl-bento-card pl-bento-card--practice">
              <span className="pl-icon-box pl-icon-box--coral"><LayersIcon /></span>
              <h3>Decisões sem risco real.</h3>
              <p>Cenários fictícios, dilemas financeiros e simulações para praticar antes de enfrentar situações reais.</p>
              <span className="pl-card-tag">Aprender fazendo</span>
            </SpotlightCard>
          </Reveal>

          <Reveal className="pl-bento-cell" delay={0.1}>
            <SpotlightCard className="pl-bento-card pl-bento-card--ai">
              <span className="pl-icon-box pl-icon-box--mint"><SparkIcon /></span>
              <h3>IA que orienta, não que decide.</h3>
              <p>
                O Mentor explica conceitos e acompanha seu raciocínio. O Analista
                identifica dificuldades. O Catalisador sugere o próximo passo.
              </p>
              <div className="pl-agent-chips" aria-hidden="true">
                <span>Catalisador</span>
                <span>Mentor</span>
                <span>Analista</span>
              </div>
            </SpotlightCard>
          </Reveal>

          <Reveal className="pl-bento-cell" delay={0.14}>
            <SpotlightCard className="pl-bento-card pl-bento-card--progress">
              <div className="pl-progress-orbit" aria-hidden="true">
                <svg viewBox="0 0 80 80">
                  <circle cx="40" cy="40" r="31" />
                  <circle cx="40" cy="40" r="31" className="pl-progress-orbit-fill" />
                </svg>
                <ChartIcon size={19} />
              </div>
              <h3>Progresso que você enxerga.</h3>
              <p>Pontos, conquistas e competências demonstradas mostram o que você já aprendeu — e o que vem a seguir.</p>
            </SpotlightCard>
          </Reveal>
        </div>
      </div>
    </section>
  )
}
