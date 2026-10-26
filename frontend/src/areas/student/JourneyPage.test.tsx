import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { JourneyPage } from './JourneyPage'

const apiMocks = vi.hoisted(() => ({
  getOverview: vi.fn(),
}))

vi.mock('@/api', () => ({
  journeyApi: { getOverview: apiMocks.getOverview },
}))

const phases = [
  {
    phase: {
      id: 1,
      number: 1,
      name: 'Primeiro salário',
      description: 'Entenda a sua primeira renda.',
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
      {
        mission: {
          id: 11,
          phase_id: 1,
          number: 2,
          name: 'O que importa primeiro?',
          description: null,
          order: 2,
          is_required: true,
          passing_score: 70,
        },
        progress: null,
        status: 'locked',
        is_unlocked: false,
      },
    ],
  },
]

describe('JourneyPage', () => {
  beforeEach(() => {
    apiMocks.getOverview.mockResolvedValue({
      data: {
        phases,
        trail: {
          source: 'rules',
          version: 1,
          phase_order: [1],
          rationale: 'Sua trilha começa pela base do primeiro salário.',
          focus_areas: ['Fundamentos'],
          pace: 'steady',
          phases: [{ number: 1, name: 'Primeiro salário', description: null }],
        },
        recommendation: {
          kind: 'start',
          message: 'O próximo passo é “De onde vem o dinheiro?”.',
          mission_id: 10,
          mission_name: 'De onde vem o dinheiro?',
          phase_number: 1,
          phase_name: 'Primeiro salário',
          trail_position: 1,
          trail_size: 6,
        },
      },
    })
  })

  it('lists available and locked missions with progress state', async () => {
    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <JourneyPage />
      </MemoryRouter>,
    )

    expect(await screen.findByRole('heading', { name: 'Primeiro salário' })).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: /De onde vem o dinheiro\?/ }),
    ).toHaveAttribute('href', '/student/learn/10')
    expect(screen.getByText('2. O que importa primeiro?')).toBeInTheDocument()
    expect(screen.getByText('Bloqueada')).toBeInTheDocument()
    expect(
      screen.getByText('Sua trilha começa pela base do primeiro salário.'),
    ).toBeInTheDocument()
  })
})
