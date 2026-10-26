import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, UserProfile } from '@/types/student'

interface SessionState {
  user: User | null
  profile: UserProfile | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  coins: number
  setCoins: (coins: number) => void
  addCoins: (amount: number) => void
  setSession: (
    user: User,
    accessToken: string,
    refreshToken: string,
    profile?: UserProfile | null,
  ) => void
  clearSession: () => void
  setUser: (user: User) => void
  setProfile: (profile: UserProfile | null) => void
}

export const useSessionStore = create<SessionState>()(
  persist(
    (set) => ({
      user: null,
      profile: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      coins: 0,

      setCoins: (coins) => set({ coins: Math.max(0, coins) }),
      addCoins: (amount) =>
        set((state) => ({ coins: Math.max(0, state.coins + amount) })),

      setSession: (user, accessToken, refreshToken, profile = null) => {
        localStorage.setItem('access_token', accessToken)
        localStorage.setItem('refresh_token', refreshToken)
        set({ user, profile, accessToken, refreshToken, isAuthenticated: true })
      },

      clearSession: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({
          user: null,
          profile: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
          coins: 0,
        })
      },

      setUser: (user) => set({ user }),
      setProfile: (profile) => set({ profile }),
    }),
    {
      name: 'ell-session',
      partialize: (state) => ({
        user: state.user,
        profile: state.profile,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
        coins: state.coins,
      }),
    },
  ),
)
