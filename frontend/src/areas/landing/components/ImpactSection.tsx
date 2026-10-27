import type { ReactNode } from 'react'
import { ArrowRightIcon, ChartIcon, SparkIcon, WalletIcon } from '@/design-system/Icons'
import { Reveal, SectionHeading } from './primitives'

interface ImpactStat {
  label: string
  value: string
  suffix: string
  description: string
  source: string
  tone: 'coral' | 'blue' | 'mint'
  icon: ReactNode
}

const stats: ImpactStat[] = [
  {
    label: 'Idade média',
    value: '20',
    suffix: 'anos',
    description:
      'no primeiro relacionamento com o sistema financeiro em 2024. Em 2020, eram cerca de 35 anos.',
    source: 'BCB · 2025',
    tone: 'coral',
    icon: <SparkIcon size={16} />,
  },
  {
    label: 'Acesso ao crédito',
    value: '27,6',
    suffix: 'milhões',
    description:
      'de jovens de 15 a 29 anos com acesso a crédito em 2024 — mais que o dobro de 2016.',
    source: 'BCB · 2025',
    tone: 'blue',
    icon: <WalletIcon size={16} />,
  },
  {
    label: 'Inadimplência',
    value: '3,3%',
    suffix: 'vs. 2,1%',
    description:
      'inadimplência média de jovens de 15 a 29 anos e adultos nos últimos oito anos — mais de 50% maior para os jovens.',
    source: 'BCB · 2025',
    tone: 'mint',
    icon: <ChartIcon size={16} />,
  },
]

export function ImpactSection() {
  return (
    <section className="pl-section pl-impact" id="impacto">
      <div className="pl-container">
        <SectionHeading
          align="center"
          eyebrow="Por que isso importa"
          title={<>A primeira conta chega <span className="pl-gradient-text">antes da primeira aula.</span></>}
          description="Jovens entram no crédito cada vez mais cedo. E a inadimplência entre eles é maior que a dos adultos. Estes são os números por trás da jornada."
        />

        <div className="pl-impact-stats">
          {stats.map((stat, index) => (
            <Reveal key={stat.label} delay={index * 0.08}>
              <article className={`pl-impact-card pl-impact-card--${stat.tone}`}>
                <div className="pl-impact-card-top">
                  <span className="pl-impact-label">{stat.label}</span>
                  <span className="pl-impact-icon" aria-hidden="true">{stat.icon}</span>
                </div>
                <p className="pl-impact-value">
                  <strong>{stat.value}</strong>{' '}<small>{stat.suffix}</small>
                </p>
                <p className="pl-impact-description">{stat.description}</p>
                <span className="pl-impact-source">{stat.source}</span>
              </article>
            </Reveal>
          ))}
        </div>

        <Reveal className="pl-impact-detail" delay={0.12}>
          <p>
            Entre jovens de baixa renda (até 2 salários mínimos), <strong>17,4% estavam inadimplentes em 2024</strong>.
            E <strong>13 milhões</strong> usaram rotativo ou parcelado — 79% dos que usaram cartão.
          </p>
        </Reveal>

        <Reveal className="pl-impact-paradox" delay={0.16}>
          <div className="pl-impact-scores">
            <div className="pl-impact-score">
              <strong>64,5</strong>
              <span>jovens 16–24</span>
            </div>
            <span className="pl-impact-score-divider" aria-hidden="true" />
            <div className="pl-impact-score pl-impact-score--muted">
              <strong>59,6</strong>
              <span>média nacional</span>
            </div>
          </div>

          <div className="pl-impact-paradox-copy">
            <span className="pl-impact-kicker">O paradoxo</span>
            <h3>Saber não é o mesmo que praticar.</h3>
            <p>
              Na pesquisa de letramento do BCB, jovens de 16 a 24 anos pontuam acima da média.
              Mas, no crédito, a inadimplência é maior. O Prisma.AI existe para transformar
              conhecimento em prática guiada.
            </p>
            <a className="pl-impact-link" href="#experiencia">
              Ver a experiência
              <ArrowRightIcon size={15} />
            </a>
          </div>
        </Reveal>

        <Reveal className="pl-impact-sources" delay={0.18}>
          <span>Fontes:</span>
          <a
            href="https://www.bcb.gov.br/content/cidadaniafinanceira/documentos_cidadania/RCF/relatorio_de_cidadania_financeira_2025.pdf"
            target="_blank"
            rel="noreferrer"
          >
            BCB, Relatório de Cidadania Financeira 2025
          </a>
          <span aria-hidden="true">·</span>
          <a
            href="https://www.metropoles.com/brasil/jovens-tem-inadimplencia-50-superior-a-de-adultos-aponta-bc"
            target="_blank"
            rel="noreferrer"
          >
            Metrópoles, 13/04/2026
          </a>
          <span aria-hidden="true">·</span>
          <a
            href="https://www.bcb.gov.br/content/cidadaniafinanceira/documentos_cidadania/letramento/relatorio-de-letramento-financeiro.pdf"
            target="_blank"
            rel="noreferrer"
          >
            BCB/OCDE, 2023
          </a>
        </Reveal>
      </div>
    </section>
  )
}
