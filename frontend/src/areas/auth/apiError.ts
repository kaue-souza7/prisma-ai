interface ValidationDetail {
  message?: string
}

interface ApiErrorBody {
  error?: {
    message?: string
    detail?: ValidationDetail[] | string
  }
  detail?: unknown
}

interface ApiErrorLike {
  response?: {
    data?: ApiErrorBody
  }
}

function normalizeDetail(detail: ValidationDetail[] | string | unknown): string | undefined {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const first = detail.find(
      (item): item is ValidationDetail =>
        typeof item === 'object' && item !== null && typeof (item as ValidationDetail).message === 'string',
    )
    return first?.message
  }
  return undefined
}

/**
 * Extrai a mensagem mais específica disponível no envelope de erro da API
 * (`{ error: { message, detail } }`), mantendo fallback para erros de rede.
 */
export function getAuthErrorMessage(error: unknown, fallback: string): string {
  const body = (error as ApiErrorLike)?.response?.data
  const detailMessage = normalizeDetail(body?.error?.detail)
  const message = detailMessage || body?.error?.message

  if (!message) return fallback

  return message
    .replace(/^Value error,\s*/i, '')
    .replace(/^String should match pattern.*$/i, 'Informe um e-mail válido.')
}
