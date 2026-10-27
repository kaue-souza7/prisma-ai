/**
 * Dados de exemplo usados apenas nas prévias da landing page.
 *
 * O conteúdo espelha o que o estudante vê na área autenticada
 * (trilhas, missões, competências e conquistas reais do produto),
 * sem depender da API.
 */

export type PreviewMissionStatus = 'completed' | 'in_progress' | 'available' | 'locked'
export type PreviewPhaseStatus = 'completed' | 'in_progress' | 'locked'

export interface PreviewMission {
  number: number
  name: string
  status: PreviewMissionStatus
  score?: number
}

export interface PreviewPhase {
  number: number
  name: string
  description: string
  status: PreviewPhaseStatus
  missions: PreviewMission[]
}

export const PREVIEW_PHASES: PreviewPhase[] = [
  {
    number: 1,
    name: 'Meu primeiro salário',
    description:
      'Compreenda o holerite, o salário líquido, o INSS, o IRRF e os direitos trabalhistas.',
    status: 'completed',
    missions: [
      { number: 1, name: 'De onde vem o dinheiro?', status: 'completed', score: 100 },
      { number: 2, name: 'Holerite linha a linha', status: 'completed', score: 100 },
      { number: 3, name: '13º salário e férias', status: 'completed', score: 100 },
    ],
  },
  {
    number: 2,
    name: 'Orçamento na prática',
    description:
      'Organize o orçamento mensal, identifique gastos invisíveis e mantenha o controle das despesas.',
    status: 'completed',
    missions: [
      { number: 1, name: 'O que importa primeiro?', status: 'completed', score: 100 },
      { number: 2, name: 'Meu primeiro plano', status: 'completed', score: 100 },
      { number: 3, name: 'Gastos invisíveis', status: 'completed', score: 100 },
      { number: 4, name: 'Controle de despesas', status: 'completed', score: 100 },
    ],
  },
  {
    number: 3,
    name: 'Pagamentos do dia a dia',
    description:
      'Compare Pix, débito, crédito e carteiras digitais e escolha o meio certo para cada compra.',
    status: 'in_progress',
    missions: [
      { number: 1, name: 'Como vou pagar?', status: 'completed', score: 100 },
      { number: 2, name: 'Carteiras digitais e pagamentos no celular', status: 'completed', score: 100 },
      { number: 3, name: 'Antes de confirmar', status: 'available' },
      { number: 4, name: 'Comparando meios de pagamento', status: 'locked' },
    ],
  },
  {
    number: 4,
    name: 'Cartão e fatura',
    description:
      'Entenda o ciclo do cartão, a fatura, o pagamento mínimo e as consequências do rotativo.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Entendendo o cartão', status: 'locked' },
      { number: 2, name: 'Fatura e ciclo de compras', status: 'locked' },
      { number: 3, name: 'Pagamento mínimo e suas consequências', status: 'locked' },
    ],
  },
  {
    number: 5,
    name: 'Metas e reserva',
    description:
      'Formule metas financeiras e calcule o tamanho ideal da reserva de emergência.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Por que poupar?', status: 'locked' },
      { number: 2, name: 'Calculando a reserva de emergência', status: 'locked' },
      { number: 3, name: 'Atingindo a meta', status: 'locked' },
      { number: 4, name: 'Usando e revisando a reserva', status: 'locked' },
    ],
  },
  {
    number: 6,
    name: 'Guardar sem perder o controle',
    description:
      'Separe o dinheiro no recebimento e adapte o método para diferentes perfis de renda.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Separar primeiro', status: 'locked' },
      { number: 2, name: 'Separar o dinheiro no recebimento', status: 'locked' },
      { number: 3, name: 'Adaptando o método para diferentes rendas', status: 'locked' },
    ],
  },
  {
    number: 7,
    name: 'Juros e parcelas',
    description:
      'Calcule o custo real do crédito, interprete o CET e avalie ofertas de parcelamento.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Juros simples e compostos', status: 'locked' },
      { number: 2, name: 'Parcelamento e CET', status: 'locked' },
      { number: 3, name: '"Sem juros" existe?', status: 'locked' },
      { number: 4, name: 'Comparando ofertas', status: 'locked' },
    ],
  },
  {
    number: 8,
    name: 'Dívida que cresce',
    description:
      'Interprete o crescimento de dívidas, o rotativo e trace estratégias de saída.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Como a dívida cresce', status: 'locked' },
      { number: 2, name: 'Cálculo do rotativo', status: 'locked' },
      { number: 3, name: 'Estratégias de saída', status: 'locked' },
    ],
  },
  {
    number: 9,
    name: 'Inflação e poder de compra',
    description:
      'Compreenda o IPCA, calcule reajustes e diferencie rendimento nominal de real.',
    status: 'locked',
    missions: [
      { number: 1, name: 'O que é inflação?', status: 'locked' },
      { number: 2, name: 'Rendimento real', status: 'locked' },
      { number: 3, name: 'Inflação e decisões', status: 'locked' },
    ],
  },
  {
    number: 10,
    name: 'Onde o dinheiro rende',
    description:
      'Conheça renda fixa, FGC e tributação para comparar produtos e investir melhor.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Fundamentos do investimento', status: 'locked' },
      { number: 2, name: 'Produtos de renda fixa', status: 'locked' },
      { number: 3, name: 'FGC e tributação', status: 'locked' },
      { number: 4, name: 'Comparando produtos', status: 'locked' },
    ],
  },
  {
    number: 11,
    name: 'Golpes e proteção de dados',
    description:
      'Reconheça fraudes digitais, proteja seus dados e saiba como agir após um golpe.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Tipos de golpe', status: 'locked' },
      { number: 2, name: 'Golpes com Pix', status: 'locked' },
      { number: 3, name: 'Proteção de dados', status: 'locked' },
      { number: 4, name: 'O que fazer depois', status: 'locked' },
      { number: 5, name: 'Reconhecimento rápido', status: 'locked' },
    ],
  },
  {
    number: 12,
    name: 'Desafio integrador',
    description:
      'Aplique as competências de todas as trilhas em cenários reais de decisão financeira.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Cenário: primeiro salário', status: 'locked' },
      { number: 2, name: 'Cenário: decisão de pagamento', status: 'locked' },
      { number: 3, name: 'Cenário: crise financeira', status: 'locked' },
      { number: 4, name: 'Cenário: alerta de fraude', status: 'locked' },
    ],
  },
]

export const PREVIEW_STUDENT = {
  name: 'Marina',
  email: 'marina.souza@email.com',
  handle: 'marina.souza',
}

export const PREVIEW_PROGRESS = {
  points: 450,
  level: 2,
  levelName: 'Consciente',
  currentLevelPoints: 300,
  nextLevelPoints: 700,
  missionsCompleted: 9,
  achievementsCount: 4,
  demonstratedCompetencies: 12,
  progressPercent: 37.5,
} as const

export const PREVIEW_COMPETENCIES = [
  {
    code: '3.1.1',
    name: 'Distinguir débito, crédito, Pix e carteira digital',
    status: 'demonstrated' as const,
    correct: 2,
    incorrect: 0,
    reinforcement: false,
  },
  {
    code: '3.1.2',
    name: 'Escolher o meio de pagamento adequado à situação',
    status: 'developing' as const,
    correct: 1,
    incorrect: 2,
    reinforcement: true,
  },
  {
    code: '3.1.3',
    name: 'Comparar prazo de compensação dos diferentes meios',
    status: 'demonstrated' as const,
    correct: 2,
    incorrect: 0,
    reinforcement: false,
  },
  {
    code: '3.3.1',
    name: 'Aplicar checagem antes de confirmar um pagamento',
    status: 'not_started' as const,
    correct: 0,
    incorrect: 0,
    reinforcement: false,
  },
]

export const PREVIEW_ACHIEVEMENTS = [
  { key: 'planejador_iniciante', name: 'Planejador iniciante', date: '12 de outubro de 2026' },
  { key: 'sem_duvidas', name: 'Sem dúvidas', date: '09 de outubro de 2026' },
  { key: 'primeiro_passo', name: 'Primeiro passo', date: '05 de outubro de 2026' },
]

export function phaseProgress(phase: PreviewPhase) {
  const total = phase.missions.length
  const completed = phase.missions.filter((mission) => mission.status === 'completed').length
  return {
    total,
    completed,
    percent: total ? Math.round((completed / total) * 100) : 0,
  }
}
