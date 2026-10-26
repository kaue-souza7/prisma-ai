export type MissionStatus = 'locked' | 'available' | 'in_progress' | 'completed'
export type CompetencyStatus = 'not_started' | 'developing' | 'demonstrated'

export interface ActivityOption {
  value: string
  label: string
}

export interface ActivityContent {
  schema_version?: number
  prompt: string
  options?: ActivityOption[]
  scenario?: string
  feedback_correct?: string
  feedback_incorrect?: string
  feedback_static?: string
  hint?: string
  max_length?: number
  competency_codes?: string[]
}

export interface Activity {
  id: number
  order: number
  activity_type: 'multiple_choice' | 'open_text' | 'simulation' | string
  content: ActivityContent
  points_value: number
}

export interface Competency {
  id: number
  code?: string | null
  name: string
  description?: string | null
  is_essential: boolean
}

export interface Mission {
  id: number
  phase_id: number
  number: number
  name: string
  description?: string | null
  order: number
  is_required: boolean
  passing_score: number
}

export interface MissionProgress {
  mission_id: number
  status: MissionStatus
  score: number | null
  score_percent: number | null
  attempts: number
  started_at: string | null
  completed_at: string | null
}

export interface MissionDetail extends Mission {
  competencies: Competency[]
  activities: Activity[]
  user_status: MissionStatus
  is_unlocked: boolean
  user_progress: MissionProgress | null
  completed_activity_ids: number[]
}

export interface MissionWithProgress {
  mission: Mission
  progress: MissionProgress | null
  status: MissionStatus
  is_unlocked: boolean
}

export interface Phase {
  id: number
  number: number
  name: string
  description?: string | null
  order: number
}

export interface PhaseJourney {
  phase: Phase
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  is_unlocked: boolean
  missions: MissionWithProgress[]
}

export interface LessonStep {
  index: number
  type: 'intro' | 'reading' | 'question' | 'scenario' | 'summary' | string
  title: string
  body: string | null
  agent: string | null
  content_type: string | null
  highlights: string[]
  activity: Activity | null
  user_response: {
    is_correct: boolean | null
    feedback: string
    attempt_number: number
    response_data: Record<string, unknown>
    correct_answer?: string | null
  } | null
  completed: boolean
}

export interface Lesson {
  mission: Mission
  phase: Phase
  competencies: Competency[]
  steps: LessonStep[]
  current_step: number
  completed_steps: number[]
  estimated_minutes: number
  status: MissionStatus
  progress: MissionProgress | null
  score_percent?: number | null
  passed?: boolean | null
  attempt_finished?: boolean
  must_retry?: boolean | null
  can_retry_optionally?: boolean | null
  next_mission: { id: number; number: number; name: string } | null
  mission_insight?: AgentInsight | null
  next_step?: CatalystRecommendation | null
}

export interface TrailPhase {
  number: number
  name: string
  description?: string | null
}

export interface Trail {
  source: 'rules' | 'standard' | 'ai' | string
  version: number
  goal_category?: string | null
  phase_order: number[]
  rationale: string
  focus_areas: string[]
  pace: 'supported' | 'steady' | 'accelerated' | string
  knowledge_level?: string | null
  life_context?: string | null
  urgency?: string | null
  generated_at?: string | null
  phases: TrailPhase[]
}

export interface CatalystRecommendation {
  kind: 'start' | 'continue' | 'review' | 'complete' | string
  message: string
  mission_id: number | null
  mission_name: string | null
  phase_number: number | null
  phase_name: string | null
  trail_position: number | null
  trail_size: number | null
}

export interface AgentInsight {
  agent: 'analyst' | 'mentor' | 'catalyst' | string
  severity: 'attention' | 'positive' | 'neutral' | string
  action: string
  competencies: string[]
  message: string
}

export interface JourneyOverview {
  trail: Trail | null
  phases: PhaseJourney[]
  recommendation: CatalystRecommendation
}

export interface MentorContext {
  mission_id: number | null
  mission_name: string | null
  phase_number: number | null
  phase_name: string | null
  opening_message: string
  suggestions: string[]
  status: 'available' | 'preparing' | 'unavailable' | string
  personal_goal: string | null
  reinforcement_topics: string[]
}

export interface MentorMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  status?: 'available' | 'preparing' | 'unavailable' | string
} 


export interface LessonProgress {
  current_step: number
  completed_steps: number[]
  mission_completed: boolean
}

export interface ContentItem {
  id: number
  mission_id: number | null
  content_type: 'explanation' | 'example' | 'tip' | string
  title: string | null
  body: string
  order: number
  is_published: boolean
  created_at: string
}

export interface Achievement {
  key: string
  name: string
  earned_at: string
}

export interface UserCompetencyProgress {
  code: string | null
  name: string
  status: CompetencyStatus
  correct_count: number
  incorrect_count: number
  reinforcement_suggested: boolean
}

export interface ProgressSummary {
  total_points: number
  coins: number
  level: number
  level_name: string
  current_level_points: number
  next_level_points: number | null
  achievements: Achievement[]
  competencies: UserCompetencyProgress[]
  missions_completed: number
  missions_in_progress: number
  analyst_insight?: AgentInsight | null
}

export type StudioFormat = 'revisao' | 'flashcards' | 'exercicios'

export interface StudioSection {
  title: string
  body: string
}

export interface StudioFlashcard {
  front: string
  back: string
}

export interface StudioQuestion {
  prompt: string
  options?: ActivityOption[]
  correct_answer?: string
  feedback_correct?: string
  feedback_incorrect?: string
  competency_codes?: string[]
  user_response?: Record<string, unknown> | null
  is_correct?: boolean | null
  feedback?: string
}

export interface StudioContent {
  type: StudioFormat
  title?: string
  message?: string
  sections?: StudioSection[]
  summary?: string[]
  cards?: StudioFlashcard[]
  questions?: StudioQuestion[]
  coins_rewarded?: boolean
}

export interface GeneratedContent {
  id: number
  format: StudioFormat
  phase_id: number | null
  phase_name: string | null
  mission_id: number | null
  mission_name: string | null
  style_hint: string | null
  content: StudioContent
  status: 'generating' | 'ready' | 'failed' | string
  coins_spent: number
  created_at: string
}

export interface StudioLibrary {
  items: GeneratedContent[]
  total: number
}

export interface GenerateStudioRequest {
  format: StudioFormat
  phase_id: number
  mission_id?: number | null
  style_hint?: string | null
}

export interface StudioExerciseResult {
  is_correct: boolean | null
  correct_answer: string | null
  feedback: string
  all_done: boolean
  coins_earned: number
}

export interface User {
  id: number
  email: string
  role: string
  is_verified: boolean
}

export interface UserProfile {
  personal_goal: string | null
  knowledge_level: string | null
  onboarding_completed: boolean
  consent_given: boolean
  preferences: Record<string, unknown> | null
  trail?: Trail | null
}
