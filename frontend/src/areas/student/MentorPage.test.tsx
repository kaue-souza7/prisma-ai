import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { MentorPage } from './MentorPage'

const apiMocks = vi.hoisted(() => ({
  getMentorContext: vi.fn(),
  getMentorHistory: vi.fn(),
  chatWithMentor: vi.fn(),
}))

vi.mock('@/api', () => ({
  conversationsApi: {
    getMentorContext: apiMocks.getMentorContext,
    getMentorHistory: apiMocks.getMentorHistory,
    chatWithMentor: apiMocks.chatWithMentor,
  },
}))

function renderMentor(path = '/student/mentor') {
  return render(
    <MemoryRouter
      initialEntries={[path]}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <MentorPage />
    </MemoryRouter>,
  )
}

describe('MentorPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    apiMocks.getMentorContext.mockResolvedValue({
      data: {
        mission_id: null,
        mission_name: null,
        phase_number: null,
        phase_name: null,
        opening_message: 'Pode me perguntar sobre qualquer conceito da sua jornada.',
        suggestions: ['Como funciona juros compostos?'],
        status: 'preparing',
        personal_goal: null,
        reinforcement_topics: [],
      },
    })
    apiMocks.getMentorHistory.mockResolvedValue({ data: [] })
    apiMocks.chatWithMentor.mockResolvedValue({
      data: {
        role: 'assistant',
        content: 'O Mentor ainda está em preparação.',
        timestamp: new Date().toISOString(),
        status: 'preparing',
        suggestions: [],
        source: 'fallback',
      },
    })
  })

  it('presents the three agents and an honest fallback without pretending to call AI', async () => {
    renderMentor()

    expect(screen.getByRole('heading', { name: 'Catalisador' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Mentor' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Analista de Progresso' })).toBeInTheDocument()
    expect(screen.getAllByText('Interface pronta').length).toBeGreaterThan(0)
    expect(
      screen.getByRole('heading', { name: 'O conteúdo de apoio já está nas missões.' }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(/Pode me perguntar sobre qualquer conceito/),
    ).toBeInTheDocument()
  })

  it('sends a message through the persisted chat contract', async () => {
    renderMentor()

    const input = await screen.findByLabelText('Sua mensagem para o Mentor')
    fireEvent.change(input, { target: { value: 'Como funciona a reserva de emergência?' } })
    fireEvent.click(screen.getByRole('button', { name: /Enviar/ }))

    await waitFor(() => {
      expect(apiMocks.chatWithMentor).toHaveBeenCalledWith(
        'Como funciona a reserva de emergência?',
        undefined,
      )
    })
    expect(await screen.findByText('O Mentor ainda está em preparação.')).toBeInTheDocument()
  })

  it('carries the mission context from the lesson into the chat', async () => {
    apiMocks.getMentorContext.mockResolvedValueOnce({
      data: {
        mission_id: 10,
        mission_name: 'De onde vem o dinheiro?',
        phase_number: 1,
        phase_name: 'Primeiro salário',
        opening_message: 'Estou com você no módulo 1.1 — De onde vem o dinheiro?',
        suggestions: ['Explique salário bruto com um exemplo.'],
        status: 'preparing',
        personal_goal: 'Organizar meu primeiro salário',
        reinforcement_topics: [],
      },
    })

    renderMentor('/student/mentor?mission=10')

    expect(await screen.findByText(/Estou com você no módulo 1.1/)).toBeInTheDocument()
    expect(apiMocks.getMentorContext).toHaveBeenCalledWith(10)
    expect(screen.getByText('Contexto da missão ativo')).toBeInTheDocument()
  })
})
