import api from './client'
import type {
  GeneratedContent,
  GenerateStudioRequest,
  StudioExerciseResult,
  StudioLibrary,
} from '@/types/student'

export const studioApi = {
  generate: (data: GenerateStudioRequest) =>
    api.post<GeneratedContent>('/api/v1/studio/generate', data),
  getGeneration: (id: number) =>
    api.get<GeneratedContent>(`/api/v1/studio/generate/${id}`),
  getLibrary: (limit = 20, offset = 0) =>
    api.get<StudioLibrary>('/api/v1/studio/library', {
      params: { limit, offset },
    }),
  submitExercise: (
    generationId: number,
    questionIndex: number,
    responseData: object,
  ) =>
    api.post<StudioExerciseResult>(
      `/api/v1/studio/exercises/${generationId}/submit`,
      { question_index: questionIndex, response_data: responseData },
    ),
}
