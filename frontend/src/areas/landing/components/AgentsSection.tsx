import { Mascot3D } from '@/features/mascots/Mascot3D'
import type { AgentKey } from '@/areas/student/components/StudentVisuals'
import { Reveal, SectionHeading, SpotlightCard } from './primitives'

interface LandingAgent {
  key: AgentKey
  index: string
  name: string
  role: string
  description: string
  tags: string[]
  animation: string
  accent: string
}

const agents: LandingAgent[] = [
  {
    key: 'catalyst',
    index: 'A01',
    name: 'Catalisador',
    role: 'Personalização e próximo passo',
    description:
      'Personaliza a trilha, recomenda o próximo passo e celebra conquistas com base no seu objetivo, contexto de vida e progresso.',
    tags: ['Próximo passo', 'Missões', 'Reforço'],
    animation: 'C-03',
    accent: 'coral e laranja',
  },
  {
    key: 'mentor',
    index: 'A02',
    name: 'Mentor',
    role: 'Tutoria em tempo real',
    description:
      'Explica conceitos financeiros, responde dúvidas durante as missões, propõe quizzes e acompanha seu raciocínio nas atividades.',
    tags: ['Explicações', 'Quizzes', 'Feedback'],
    animation: 'M-08',
    accent: 'azul e ciano',
  },
  {
    key: 'analyst',
    index: 'A03',
    name: 'Analista de Progresso',
    role: 'Avaliação e reforço adaptativo',
    description:
      'Atua em segundo plano. Analisa respostas, identifica dificuldades recorrentes por competência e gera recomendações de reforço para o Mentor.',
    tags: ['Competências', 'Dificuldades', 'Reforço'],
    animation: 'A-02',
    accent: 'verde e menta',
  },
]

export function AgentsSection() {
  return (
    <section className="pl-section pl-agents">
      <div className="pl-agents-bg" aria-hidden="true">
        <div className="pl-agents-grid" />
      </div>
      <div className="pl-container">
        <SectionHeading
          eyebrow="Ecossistema de agentes"
          title={<>Três agentes. <span className="pl-gradient-text">Uma jornada mais inteligente.</span></>}
          description="Catalisador, Mentor e Analista de Progresso atuam em papéis complementares — coordenados pelo IBM watsonx Orchestrate para apoiar seu aprendizado."
        />

        <div className="pl-agent-grid">
          {agents.map((agent, index) => {
            return (
              <Reveal key={agent.key} delay={index * 0.1}>
                <SpotlightCard className={`pl-agent-card pl-agent-card--${agent.key}`}>
                  <div className="pl-agent-topline">
                    <span className="pl-agent-index">{agent.index}</span>
                    <span className="pl-agent-status">Visão do produto</span>
                  </div>

                  <div className="pl-agent-visual" aria-hidden="true">
                    <div className="pl-agent-halo" />
                    <div className="pl-agent-ring pl-agent-ring--outer" />
                    <div className="pl-agent-ring pl-agent-ring--inner" />
                    <Mascot3D
                      agent={agent.key}
                      animation={agent.animation}
                      size={150}
                      shadows={false}
                      className="pl-agent-mascot"
                    />
                    <span className="pl-agent-spark pl-agent-spark--one" />
                    <span className="pl-agent-spark pl-agent-spark--two" />
                    <span className="pl-agent-spark pl-agent-spark--three" />
                  </div>

                  <h3>{agent.name}</h3>
                  <p className="pl-agent-role">{agent.role}</p>
                  <p className="pl-agent-description">{agent.description}</p>

                  <div className="pl-agent-tags">
                    {agent.tags.map((tag) => <span key={tag}>{tag}</span>)}
                  </div>
                  <div className="pl-agent-accent">
                    <span />
                    {agent.accent}
                  </div>
                </SpotlightCard>
              </Reveal>
            )
          })}
        </div>

        <Reveal delay={0.16}>
          <p className="pl-agents-note">
            Os três agentes já operam com fallback determinístico e integração real ao
            IBM watsonx Orchestrate. Pontos, conquistas e desbloqueios continuam sendo
            calculados pelo backend — nunca pela IA.
          </p>
        </Reveal>
      </div>
    </section>
  )
}
