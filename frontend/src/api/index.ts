import api from './client'
export { studioApi } from './studio'
import type {
  AgentInsight,
  CatalystRecommendation,
  ContentItem,
  JourneyOverview,
  Lesson,
  LessonProgress,
  MentorContext,
  MentorMessage,
  MissionDetail,
  MissionProgress,
  PhaseJourney,
  ProgressSummary,
  Trail,
  User,
  UserProfile,
} from '@/types/student'

export const authApi = {
  register: (email: string, password: string) =>
    api.post('/api/v1/auth/register', { email, password }),

  login: (email: string, password: string) =>
    api.post<{ access_token: string; refresh_token: string }>('/api/v1/auth/login', { email, password }),

  verifyEmail: (token: string) =>
    api.get(`/api/v1/auth/verify-email?token=${token}`),

  requestPasswordReset: (email: string) =>
    api.post('/api/v1/auth/password-reset/request', { email }),

  confirmPasswordReset: (token: string, new_password: string) =>
    api.post('/api/v1/auth/password-reset/confirm', { token, new_password }),
}

export const usersApi = {
  getMe: (accessToken?: string) =>
    api.get<{ user: User; profile: UserProfile | null }>('/api/v1/users/me', {
      headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
    }),
  updateProfile: (data: object) => api.patch('/api/v1/users/me/profile', data),
  completeOnboarding: (data: object) =>
    api.post<{ message: string; trail: Trail | null }>('/api/v1/users/me/onboarding', data),
  getAdaptiveQuestions: (data: object) =>
    api.post<{ questions: string[]; source: string }>(
      '/api/v1/users/me/onboarding/adaptive-questions',
      data,
    ),
  getTrail: () => api.get<Trail | null>('/api/v1/users/me/trail'),
  setTrailPreference: (mode: 'personalized' | 'standard') =>
    api.post<Trail>('/api/v1/users/me/trail/preference', { mode }),
}

export const journeyApi = {
  getPhases: () => api.get('/api/v1/journey/phases'),
  getMyProgress: () => api.get<PhaseJourney[]>('/api/v1/journey/phases/my-progress'),
  getOverview: () => api.get<JourneyOverview>('/api/v1/journey/overview'),
  getMission: (id: number) => api.get<MissionDetail>(`/api/v1/journey/missions/${id}`),
  getLesson: (id: number) => api.get<Lesson>(`/api/v1/journey/missions/${id}/lesson`),
  saveLessonStep: (id: number, stepIndex: number) =>
    api.post<LessonProgress>(`/api/v1/journey/missions/${id}/lesson/progress`, {
      step_index: stepIndex,
    }),
  startMission: (id: number) => api.post(`/api/v1/journey/missions/${id}/start`),
  submitResponse: (missionId: number, activityId: number, responseData: object) =>
    api.post<{
      is_correct: boolean | null
      correct_answer: string | null
      score: number
      feedback: string
      feedback_agent: 'mentor' | 'analyst' | string
      attempt_number: number
      reinforcement: AgentInsight | null
      mission_completed: boolean
      attempt_finished: boolean
      points_earned: number
      coins_earned: number
      new_achievements: string[]
      score_percent: number | null
      passed: boolean | null
      must_retry: boolean | null
      can_retry_optionally: boolean | null
      mission_insight: AgentInsight | null
      next_step: CatalystRecommendation | null
    }>(`/api/v1/journey/missions/${missionId}/submit`, {
      activity_id: activityId,
      response_data: responseData,
    }),
  retryMission: (id: number, voluntary = false) =>
    api.post<MissionProgress>(`/api/v1/journey/missions/${id}/retry`, {
      voluntary,
    }),
}

export const progressApi = {
  getSummary: () => api.get<ProgressSummary>('/api/v1/progress/summary'),
}

export const contentApi = {
  getMissionContent: (missionId: number) =>
    api.get<ContentItem[]>(`/api/v1/content/missions/${missionId}`),
}

export const conversationsApi = {
  chatWithMentor: (content: string, mission_id?: number) =>
    api.post<MentorMessage & { suggestions: string[]; source: string }>(
      '/api/v1/conversations/mentor',
      { content, mission_id },
    ),
  getMentorContext: (mission_id?: number) =>
    api.get<MentorContext>('/api/v1/conversations/mentor/context', {
      params: mission_id ? { mission_id } : undefined,
    }),
  getMentorHistory: () => api.get('/api/v1/conversations/mentor/history'),
}
