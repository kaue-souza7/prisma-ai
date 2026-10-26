import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute } from '@/shared/ProtectedRoute'
import { OnboardingGate } from '@/shared/OnboardingGate'
import { StudentLayout } from '@/areas/student/StudentLayout'

const LandingPage = lazy(() =>
  import('@/areas/landing/LandingPage').then((module) => ({ default: module.LandingPage })),
)
const LoginPage = lazy(() =>
  import('@/areas/auth/LoginPage').then((module) => ({ default: module.LoginPage })),
)
const RegisterPage = lazy(() =>
  import('@/areas/auth/RegisterPage').then((module) => ({ default: module.RegisterPage })),
)
const VerifyEmailPage = lazy(() =>
  import('@/areas/auth/VerifyEmailPage').then((module) => ({ default: module.VerifyEmailPage })),
)
const ForgotPasswordPage = lazy(() =>
  import('@/areas/auth/ForgotPasswordPage').then((module) => ({ default: module.ForgotPasswordPage })),
)
const ResetPasswordPage = lazy(() =>
  import('@/areas/auth/ResetPasswordPage').then((module) => ({ default: module.ResetPasswordPage })),
)
const StudentHome = lazy(() =>
  import('@/areas/student/StudentHome').then((module) => ({ default: module.StudentHome })),
)
const OnboardingPage = lazy(() =>
  import('@/areas/student/OnboardingPage').then((module) => ({ default: module.OnboardingPage })),
)
const JourneyPage = lazy(() =>
  import('@/areas/student/JourneyPage').then((module) => ({ default: module.JourneyPage })),
)
const LessonPlayerPage = lazy(() =>
  import('@/areas/student/LessonPlayerPage').then((module) => ({ default: module.LessonPlayerPage })),
)
const ProgressPage = lazy(() =>
  import('@/areas/student/ProgressPage').then((module) => ({ default: module.ProgressPage })),
)
const ProfilePage = lazy(() =>
  import('@/areas/student/ProfilePage').then((module) => ({ default: module.ProfilePage })),
)
const MentorPage = lazy(() =>
  import('@/areas/student/MentorPage').then((module) => ({ default: module.MentorPage })),
)
const StudioPage = lazy(() =>
  import('@/areas/student/StudioPage').then((module) => ({ default: module.StudioPage })),
)

function RouteFallback() {
  return (
    <div className="route-fallback" role="status" aria-live="polite">
      <span className="route-fallback-mark" aria-hidden="true" />
      <span>Carregando experiência...</span>
    </div>
  )
}

export function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Suspense fallback={<RouteFallback />}>
        <Routes>
        {/* Landing page pública */}
        <Route path="/" element={<LandingPage />} />

        {/* Auth */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verify-email" element={<VerifyEmailPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />

        {/* Área do estudante — protegida */}
        <Route element={<ProtectedRoute role="student" />}>
          <Route path="/onboarding" element={<OnboardingPage />} />

          <Route element={<OnboardingGate />}>
            <Route path="/student/learn/:missionId" element={<LessonPlayerPage />} />
            <Route element={<StudentLayout />}>
              <Route path="/student" element={<StudentHome />} />
              <Route path="/student/journey" element={<JourneyPage />} />
              <Route path="/student/mentor" element={<MentorPage />} />
              <Route path="/student/studio" element={<StudioPage />} />
              <Route path="/student/progress" element={<ProgressPage />} />
              <Route path="/student/profile" element={<ProfilePage />} />
            </Route>
          </Route>
        </Route>

        {/* 404 */}
        <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
