import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { ForgotPasswordPage } from './ForgotPasswordPage'
import { LoginPage } from './LoginPage'
import { RegisterPage } from './RegisterPage'
import { ResetPasswordPage } from './ResetPasswordPage'
import { VerifyEmailPage } from './VerifyEmailPage'

const apiMocks = vi.hoisted(() => ({
  login: vi.fn(),
  getMe: vi.fn(),
  register: vi.fn(),
  requestPasswordReset: vi.fn(),
  confirmPasswordReset: vi.fn(),
  verifyEmail: vi.fn(),
}))

const sessionMocks = vi.hoisted(() => ({
  setSession: vi.fn(),
}))

vi.mock('@/api', () => ({
  authApi: {
    login: apiMocks.login,
    register: apiMocks.register,
    requestPasswordReset: apiMocks.requestPasswordReset,
    confirmPasswordReset: apiMocks.confirmPasswordReset,
    verifyEmail: apiMocks.verifyEmail,
  },
  usersApi: {
    getMe: apiMocks.getMe,
  },
}))

vi.mock('@/store/session', () => ({
  useSessionStore: (selector: (state: { setSession: typeof sessionMocks.setSession }) => unknown) =>
    selector({ setSession: sessionMocks.setSession }),
}))

function renderRoute(element: JSX.Element, initialEntry = '/login') {
  return render(
    <MemoryRouter
      initialEntries={[initialEntry]}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        <Route path="/verify-email" element={<VerifyEmailPage />} />
        <Route path="/student" element={<div>Área do estudante</div>} />
        <Route path="/" element={<div>Início</div>} />
        <Route path="*" element={element} />
      </Routes>
    </MemoryRouter>,
  )
}

function fillField(label: string, value: string) {
  fireEvent.change(screen.getByLabelText(label), { target: { value } })
}

describe('Prisma.AI auth screens', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('validates the login form before calling the API', async () => {
    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <LoginPage />
      </MemoryRouter>,
    )

    fireEvent.click(screen.getByRole('button', { name: /^Entrar$/ }))

    expect(await screen.findByText('Informe seu e-mail.')).toBeInTheDocument()
    expect(screen.getByText('Informe sua senha.')).toBeInTheDocument()
    expect(apiMocks.login).not.toHaveBeenCalled()
  })

  it('logs in and navigates to the student area', async () => {
    apiMocks.login.mockResolvedValue({
      data: { access_token: 'access-123', refresh_token: 'refresh-123' },
    })
    apiMocks.getMe.mockResolvedValue({
      data: { user: { id: 1, email: 'ana@prisma.ai', role: 'student', is_verified: true } },
    })

    renderRoute(<LoginPage />, '/login')

    fillField('E-mail', 'ana@prisma.ai')
    fillField('Senha', 'Senha123')
    fireEvent.click(screen.getByRole('button', { name: /^Entrar$/ }))

    expect(await screen.findByText('Área do estudante')).toBeInTheDocument()
    expect(apiMocks.login).toHaveBeenCalledWith('ana@prisma.ai', 'Senha123')
    expect(sessionMocks.setSession).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'ana@prisma.ai' }),
      'access-123',
      'refresh-123',
      null,
    )
  })

  it('shows the API error when login fails', async () => {
    apiMocks.login.mockRejectedValue({
      response: { data: { error: { message: 'E-mail ou senha incorretos.' } } },
    })

    renderRoute(<LoginPage />, '/login')

    fillField('E-mail', 'ana@prisma.ai')
    fillField('Senha', 'SenhaErrada1')
    fireEvent.click(screen.getByRole('button', { name: /^Entrar$/ }))

    expect(await screen.findByText('E-mail ou senha incorretos.')).toBeInTheDocument()
    expect(sessionMocks.setSession).not.toHaveBeenCalled()
  })

  it('validates the password rules before registering', async () => {
    renderRoute(<RegisterPage />, '/register')

    fillField('E-mail', 'ana@prisma.ai')
    fillField('Senha', 'fraca')
    fireEvent.click(screen.getByRole('button', { name: /Criar minha conta/ }))

    expect(await screen.findByText('A senha deve ter pelo menos 8 caracteres.')).toBeInTheDocument()
    expect(apiMocks.register).not.toHaveBeenCalled()
  })

  it('registers and shows the email confirmation state', async () => {
    apiMocks.register.mockResolvedValue({ data: { message: 'Cadastro realizado.' } })

    renderRoute(<RegisterPage />, '/register')

    fillField('E-mail', 'ana@prisma.ai')
    fillField('Senha', 'Senha123')
    fireEvent.click(screen.getByRole('button', { name: /Criar minha conta/ }))

    expect(await screen.findByRole('heading', { name: /Confirme seu e-mail/i })).toBeInTheDocument()
    expect(screen.getByText('ana@prisma.ai')).toBeInTheDocument()
    expect(apiMocks.register).toHaveBeenCalledWith('ana@prisma.ai', 'Senha123')
  })

  it('shows recovery instructions after requesting a password reset', async () => {
    apiMocks.requestPasswordReset.mockResolvedValue({
      data: { message: 'Se o e-mail estiver cadastrado, você receberá as instruções em breve.' },
    })

    renderRoute(<ForgotPasswordPage />, '/forgot-password')

    fillField('E-mail da conta', 'ana@prisma.ai')
    fireEvent.click(screen.getByRole('button', { name: /Enviar instruções/ }))

    expect(await screen.findByRole('heading', { name: /Confira sua caixa de entrada/i })).toBeInTheDocument()
    expect(screen.getByText(/Se o e-mail estiver cadastrado/)).toBeInTheDocument()
    expect(apiMocks.requestPasswordReset).toHaveBeenCalledWith('ana@prisma.ai')
  })

  it('confirms a password reset with the token from the URL', async () => {
    apiMocks.confirmPasswordReset.mockResolvedValue({ data: { message: 'Senha redefinida com sucesso.' } })

    renderRoute(<ResetPasswordPage />, '/reset-password?token=reset-token')

    fillField('Nova senha', 'NovaSenha123')
    fireEvent.click(screen.getByRole('button', { name: /Salvar nova senha/ }))

    expect(await screen.findByRole('heading', { name: /Seu acesso foi renovado/i })).toBeInTheDocument()
    expect(apiMocks.confirmPasswordReset).toHaveBeenCalledWith('reset-token', 'NovaSenha123')
  })

  it('reports an invalid email verification link', async () => {
    apiMocks.verifyEmail.mockRejectedValue({
      response: { data: { error: { message: 'Token de verificação inválido.' } } },
    })

    renderRoute(<VerifyEmailPage />, '/verify-email?token=token-invalido')

    await waitFor(() => {
      expect(screen.getByText('Token de verificação inválido.')).toBeInTheDocument()
    })
    expect(apiMocks.verifyEmail).toHaveBeenCalledWith('token-invalido')
  })
})
