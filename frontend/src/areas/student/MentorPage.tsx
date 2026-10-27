import { Link, useSearchParams } from 'react-router-dom'
import { ArrowRightIcon, ChatIcon, CheckIcon, SparkIcon } from '@/design-system/Icons'
import { useDocumentTitle } from '@/shared/useDocumentTitle'
import { AGENT_META, AgentAvatar, PrismMascot } from './components/StudentVisuals'
import { MentorChat } from './components/MentorChat'
import styles from './Mentor.module.css'

const AGENT_DETAILS = {
  catalyst: {
    role: 'Personaliza a trilha e o próximo passo',
    description:
      'Organiza a ordem das trilhas a partir do seu objetivo e indica a missão mais adequada ao seu momento. As regras são explícitas e o backend valida cada sugestão.',
    state: 'Ativo na jornada',
  },
  mentor: {
    role: 'Explica e acompanha',
    description:
      'Vai explicar conceitos, trazer exemplos e responder dúvidas durante as atividades. A interface e o histórico já estão prontos; a IA entra quando o Orchestrate for liberado.',
    state: 'Interface pronta',
  },
  analyst: {
    role: 'Lê evidências de progresso',
    description:
      'Identifica competências em desenvolvimento, dificuldades recorrentes e oportunidades de revisão sem julgar você. Aparece no resumo das missões e no painel.',
    state: 'Ativo no painel',
  },
} as const

export function MentorPage() {
  useDocumentTitle('Mentor e agentes — Prisma.AI')
  const [searchParams] = useSearchParams()
  const rawMission = Number(searchParams.get('mission'))
  const missionId = Number.isFinite(rawMission) && rawMission > 0 ? rawMission : undefined

  return (
    <div className={`st-app-page ${styles.page}`}>
      <header className={styles.hero}>
        <div className={styles.heroCopy}>
          <span className="st-eyebrow">Mentor e agentes</span>
          <h1>
            Uma equipe para <span>aprender com você.</span>
          </h1>
          <p>
            Converse com o Mentor, acompanhe as recomendações do Analista e veja
            o Catalisador organizar sua trilha. Os agentes apoiam a decisão, mas
            nunca concedem pontos ou desbloqueios por conta própria.
          </p>
          <div className={styles.heroMeta}>
            <span className="st-chip st-chip--purple"><SparkIcon size={12} /> 3 agentes</span>
            <span className="st-chip">Backend como autoridade</span>
            {missionId && <span className="st-chip st-chip--mint">Contexto da missão ativo</span>}
          </div>
        </div>
        <div className={styles.heroArt} aria-hidden="true">
          <span className={styles.heroOrb} />
          <PrismMascot size={220} tone="mentor" />
        </div>
      </header>

      <section className={styles.workspace} aria-label="Conversa com o Mentor">
        <div className={styles.chatColumn}>
          <div className={styles.chatIntro}>
            <div>
              <span className="st-eyebrow">
                {missionId ? 'Dúvida dentro da missão' : 'Conversa livre'}
              </span>
              <h2>
                {missionId
                  ? 'O Mentor já conhece o contexto da sua missão.'
                  : 'Pergunte sobre qualquer conceito da sua jornada.'}
              </h2>
              <p>
                As mensagens ficam salvas no seu histórico. Quando a integração
                com o watsonx Orchestrate for ativada, o Mentor passa a responder
                com mediação pedagógica real — sem mudar a interface.
              </p>
            </div>
            {missionId && (
              <Link to={`/student/learn/${missionId}`} className={styles.backToMission}>
                Voltar à missão
                <ArrowRightIcon size={14} />
              </Link>
            )}
          </div>
          <MentorChat missionId={missionId} />
        </div>

        <aside className={styles.sideColumn}>
          <article className={styles.sideCard}>
            <span className="st-eyebrow">Como funciona</span>
            <h2>Orientação, não atalho.</h2>
            <ul className={styles.sideList}>
              <li>
                <span><CheckIcon size={12} /></span>
                O Mentor ajuda você a raciocinar, sem entregar a resposta pronta.
              </li>
              <li>
                <span><CheckIcon size={12} /></span>
                O Analista observa evidências e sugere revisão quando um conceito
                aparece com dificuldade mais de uma vez.
              </li>
              <li>
                <span><CheckIcon size={12} /></span>
                O Catalisador organiza a trilha e o próximo passo com regras
                explícitas, validadas pelo backend.
              </li>
            </ul>
          </article>

          <div className={styles.agentStack}>
            {(['catalyst', 'mentor', 'analyst'] as const).map((agent) => {
              const meta = AGENT_META[agent]
              const detail = AGENT_DETAILS[agent]
              return (
                <article
                  key={agent}
                  className={[styles.agentCard, styles[`agent_${agent}`]].join(' ')}
                >
                  <div className={styles.agentTop}>
                    <AgentAvatar agent={agent} size={40} />
                    <span className={styles.agentState}>
                      {agent === 'mentor' && <span className={styles.pulse} />}
                      {detail.state}
                    </span>
                  </div>
                  <h2>{meta.name}</h2>
                  <span className={styles.agentRole}>{detail.role}</span>
                  <p>{detail.description}</p>
                </article>
              )
            })}
          </div>

          <article className={styles.fallbackCard}>
            <div className={styles.fallbackIcon} aria-hidden="true">
              <ChatIcon size={22} />
            </div>
            <div className={styles.fallbackCopy}>
              <span className="st-eyebrow">Fallback oficial</span>
              <h2>O conteúdo de apoio já está nas missões.</h2>
              <p>
                Cada missão tem explicações, exemplos e dicas estáticas revisadas
                pela equipe de produto. Esse é o fallback até a integração com o
                watsonx Orchestrate ser validada.
              </p>
            </div>
            <Link to="/student/journey" className={styles.primaryAction}>
              Abrir minha jornada
              <ArrowRightIcon size={15} />
            </Link>
          </article>
        </aside>
      </section>

      <section className={styles.principles}>
        <article>
          <strong>Sem decisões no seu lugar</strong>
          <p>Os agentes explicam, questionam e sugerem. A decisão financeira continua sendo sua.</p>
        </article>
        <article>
          <strong>Sem pontos por conversa</strong>
          <p>Pontuação, conclusão e desbloqueio seguem regras determinísticas do backend.</p>
        </article>
        <article>
          <strong>Com limites claros</strong>
          <p>O produto não pede dados bancários e não executa transações reais.</p>
        </article>
      </section>
    </div>
  )
}
