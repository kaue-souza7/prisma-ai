import { fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { StudentHome } from './StudentHome'
import { useSessionStore } from '@/store/session'

const apiMocks = vi.hoisted(() => ({
  getSummary: vi.fn(),
  getOverview: vi.fn(),
}))

vi.mock('@/api', () => ({
  progressApi: { getSummary: apiMocks.getSummary },
  journeyApi: { getOverview: apiMocks.getOverview },
}))

const journey = [
  {
    phase: {
      id: 1,
      number: 1,
      name: 'Primeiro salário',
      description: 'Organize sua primeira renda.',
      order: 1,
    },
    status: 'in_progress',
    is_unlocked: true,
    missions: [
      {
        mission: {
          id: 10,
          phase_id: 1,
          number: 1,
          name: 'De onde vem o dinheiro?',
          description: null,
          order: 1,
          is_required: true,
          passing_score: 70,
        },
        progress: null,
        status: 'available',
        is_unlocked: true,
      },
    ],
  },
  {
    phase: {
      id: 2,
      number: 2,
      name: 'Seu dinheiro no digital',
      description: null,
      order: 2,
    },
    status: 'locked',
    is_unlocked: false,
    missions: [],
  },
]

function renderHome() {
  return render(
    <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <StudentHome />
    </MemoryRouter>,
  )
}

describe('StudentHome', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useSessionStore.setState({
      user: { id: 1, email: 'ana@prisma.ai', role: 'student', is_verified: true },
      profile: null,
      accessToken: 'token',
      refreshToken: 'refresh',
      isAuthenticated: true,
    })
    apiMocks.getSummary.mockResolvedValue({
      data: {
        total_points: 150,
        level: 2,
        level_name: 'Consciente',
        current_level_points: 0,
        next_level_points: 700,
        achievements: [],
        competencies: [],
        missions_completed: 1,
        missions_in_progress: 1,
      },
    })
    apiMocks.getOverview.mockResolvedValue({
      data: {
        trail: {
          source: 'rules',
          version: 1,
          goal_category: 'dividas',
          phase_order: [4, 1, 2, 3, 5, 6],
          rationale: 'Começar por juros ajuda a entender o custo do crédito.',
          focus_areas: ['Juros compostos'],
          pace: 'steady',
          phases: [
            { number: 4, name: 'Juros', description: null },
            { number: 1, name: 'Primeiro salário', description: null },
          ],
        },
        phases: journey,
        recommendation: {
          kind: 'start',
          message: 'Sua trilha começa por Juros. Começar por juros ajuda.',
          mission_id: 10,
          mission_name: 'De onde vem o dinheiro?',
          phase_number: 1,
          phase_name: 'Primeiro salário',
          trail_position: 2,
          trail_size: 6,
        },
      },
    })
  })

  it('shows progress and opens the next available mission', async () => {
    renderHome()

    expect(await screen.findByText(/Olá, ana/i)).toBeInTheDocument()
    expect(screen.getByText('150')).toBeInTheDocument()
    expect(screen.getByText('Nível 2 de 5')).toBeInTheDocument()
    expect(screen.getByText('1 missão concluída')).toBeInTheDocument()
    expect(screen.getByText(/Sua trilha começa por Juros/)).toBeInTheDocument()

    const missionLink = screen.getByRole('link', {
      name: /De onde vem o dinheiro\?/,
    })
    expect(missionLink).toHaveAttribute('href', '/student/learn/10')
    expect(screen.getAllByText('Em preparação').length).toBeGreaterThan(0)
  })

  it('offers a retry when loading fails', async () => {
    apiMocks.getSummary.mockRejectedValueOnce(new Error('network'))
    apiMocks.getOverview.mockResolvedValueOnce({ data: { trail: null, phases: journey, recommendation: null } })

    renderHome()

    expect(
      await screen.findByText(/Não foi possível carregar seu progresso/),
    ).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Tentar novamente' }))

    expect(await screen.findByText(/Olá, ana/i)).toBeInTheDocument()
  })
})
