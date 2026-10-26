/**
 * Dados de exemplo usados apenas nas prévias da landing page.
 *
 * O conteúdo espelha o que o estudante vê na área autenticada
 * (fases, missões, competências e conquistas reais do produto),
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
    name: 'Primeiro salário',
    description:
      'Compreender renda, prioridades e organização inicial do dinheiro.',
    status: 'completed',
    missions: [
      { number: 1, name: 'De onde vem o dinheiro?', status: 'completed', score: 100 },
      { number: 2, name: 'O que importa primeiro?', status: 'completed', score: 100 },
      { number: 3, name: 'Meu primeiro plano', status: 'completed', score: 100 },
    ],
  },
  {
    number: 2,
    name: 'Seu dinheiro no digital',
    description:
      'Compreender meios de pagamento digitais, débito, crédito e cuidados com transações.',
    status: 'in_progress',
    missions: [
      { number: 1, name: 'Como vou pagar?', status: 'completed', score: 100 },
      { number: 2, name: 'Entendendo o cartão', status: 'available' },
      { number: 3, name: 'Antes de confirmar', status: 'locked' },
    ],
  },
  {
    number: 3,
    name: 'Por que poupar',
    description:
      'Desenvolver compreensão de objetivos financeiros, planejamento e preparação para imprevistos.',
    status: 'locked',
    missions: [
      { number: 1, name: 'Um objetivo que faz sentido', status: 'locked' },
      { number: 2, name: 'Guardar sem perder o controle', status: 'locked' },
      { number: 3, name: 'E se acontecer algo inesperado?', status: 'locked' },
    ],
  },
  {
    number: 4,
    name: 'Juros: a favor e contra você',
    description:
      'Compreender como juros, tempo, atrasos e condições de crédito afetam o valor total de uma decisão financeira.',
    status: 'locked',
    missions: [
      { number: 1, name: 'O tempo e os juros', status: 'locked' },
      { number: 2, name: 'Parcelas não contam a história inteira', status: 'locked' },
      { number: 3, name: 'O que acontece quando a dívida cresce?', status: 'locked' },
    ],
  },
  {
    number: 5,
    name: 'Onde o dinheiro rende',
    description:
      'Introduzir a relação entre inflação, poder de compra, poupança e características básicas de alternativas de investimento.',
    status: 'locked',
    missions: [
      { number: 1, name: 'O que meu dinheiro consegue comprar?', status: 'locked' },
      { number: 2, name: 'Guardar ou investir?', status: 'locked' },
      { number: 3, name: 'Rendimento, prazo e liquidez', status: 'locked' },
    ],
  },
  {
    number: 6,
    name: 'Proteção digital',
    description:
      'Desenvolver a capacidade de reconhecer riscos digitais e tomar decisões seguras diante de possíveis fraudes financeiras.',
    status: 'locked',
    missions: [
      { number: 1, name: 'A mensagem suspeita', status: 'locked' },
      { number: 2, name: 'Antes de enviar um Pix', status: 'locked' },
      { number: 3, name: 'Protegendo meus dados', status: 'locked' },
      { number: 4, name: 'Desafio integrador', status: 'locked' },
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
  missionsCompleted: 4,
  achievementsCount: 3,
  demonstratedCompetencies: 2,
  progressPercent: 37.5,
} as const

export const PREVIEW_COMPETENCIES = [
  {
    code: '2.1.1',
    name: 'Explicar como funcionam Pix, débito e crédito',
    status: 'demonstrated' as const,
    correct: 2,
    incorrect: 0,
    reinforcement: false,
  },
  {
    code: '2.1.2',
    name: 'Escolher o meio de pagamento adequado à situação',
    status: 'developing' as const,
    correct: 1,
    incorrect: 2,
    reinforcement: true,
  },
  {
    code: '2.1.3',
    name: 'Reconhecer que o Pix concluído não pode ser cancelado',
    status: 'demonstrated' as const,
    correct: 2,
    incorrect: 0,
    reinforcement: false,
  },
  {
    code: '2.2.1',
    name: 'Explicar limite, fatura, fechamento e vencimento',
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
