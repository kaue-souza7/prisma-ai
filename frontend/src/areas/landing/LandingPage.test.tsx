import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'

import { LandingPage } from './LandingPage'

function renderLanding() {
  return render(
    <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <LandingPage />
    </MemoryRouter>,
  )
}

describe('Prisma.AI landing page', () => {
  it('presents the hero value proposition and auth actions', () => {
    renderLanding()

    expect(screen.getByRole('heading', { level: 1 }).textContent).toContain('Sua jornada.')
    expect(screen.getByRole('heading', { level: 1 }).textContent).toContain('Seu futuro.')

    const registerLinks = screen.getAllByRole('link', { name: /Cadastrar-se/i })
    const loginLinks = screen.getAllByRole('link', { name: /^Entrar$/i })

    expect(registerLinks.length).toBeGreaterThan(0)
    expect(loginLinks.length).toBeGreaterThan(0)
    expect(registerLinks.every((link) => link.getAttribute('href') === '/register')).toBe(true)
    expect(loginLinks.every((link) => link.getAttribute('href') === '/login')).toBe(true)
  })

  it('keeps the requested navigation anchors and agent identities', () => {
    renderLanding()

    expect(screen.getAllByRole('link', { name: 'Como funciona' })[0].getAttribute('href')).toBe('#como-funciona')
    expect(screen.getAllByRole('link', { name: 'Experiência' })[0].getAttribute('href')).toBe('#experiencia')
    expect(screen.getAllByRole('link', { name: 'Sobre' })[0].getAttribute('href')).toBe('#sobre')

    expect(screen.getByRole('heading', { name: 'Catalisador' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Mentor' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Analista de Progresso' })).toBeInTheDocument()
  })

  it('opens and closes the navigation menu from the hamburger button', async () => {
    renderLanding()

    const button = screen.getByRole('button', { name: 'Abrir menu de navegação' })
    expect(button).toHaveAttribute('aria-expanded', 'false')

    fireEvent.click(button)
    expect(button).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('navigation', { name: 'Menu de navegação' })).toBeInTheDocument()

    fireEvent.keyDown(window, { key: 'Escape' })
    await waitFor(() => {
      expect(screen.queryByRole('navigation', { name: 'Menu de navegação' })).not.toBeInTheDocument()
    })
  })

  it('shows a real product screen in the hero instead of an illustrative mockup', () => {
    renderLanding()

    expect(
      screen.getByRole('img', {
        name: 'Tela de exemplo da página inicial da área do estudante',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Seu próximo passo')).toBeInTheDocument()
  })

  it('switches between the product screens in the experience tabs', async () => {
    renderLanding()

    expect(await screen.findByText(/Seu caminho,/)).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Minicurso' }))
    expect(
      await screen.findByText('O que é o limite do cartão de crédito?'),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Progresso' }))
    expect(await screen.findByText('O que você já demonstra.')).toBeInTheDocument()
  })
})
