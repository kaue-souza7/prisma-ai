import { beforeEach, describe, expect, it } from 'vitest'

import { useSessionStore } from './session'

const user = {
  id: 1,
  email: 'estudante@example.com',
  role: 'student',
  is_verified: true,
}

describe('session store', () => {
  beforeEach(() => {
    localStorage.clear()
    useSessionStore.setState({
      user: null,
      profile: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    })
  })

  it('stores the authenticated session and access tokens', () => {
    useSessionStore.getState().setSession(user, 'access-token', 'refresh-token')

    const state = useSessionStore.getState()
    expect(state.user).toEqual(user)
    expect(state.accessToken).toBe('access-token')
    expect(state.refreshToken).toBe('refresh-token')
    expect(state.isAuthenticated).toBe(true)
    expect(localStorage.getItem('access_token')).toBe('access-token')
    expect(localStorage.getItem('refresh_token')).toBe('refresh-token')
  })

  it('clears user and tokens on logout', () => {
    useSessionStore.getState().setSession(user, 'access-token', 'refresh-token')

    useSessionStore.getState().clearSession()

    const state = useSessionStore.getState()
    expect(state.user).toBeNull()
    expect(state.accessToken).toBeNull()
    expect(state.refreshToken).toBeNull()
    expect(state.isAuthenticated).toBe(false)
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
  })
})
