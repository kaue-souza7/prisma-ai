export interface PasswordRule {
  key: 'length' | 'uppercase' | 'number'
  label: string
  met: boolean
}

export function validateEmail(value: string): string | undefined {
  const email = value.trim()
  if (!email) return 'Informe seu e-mail.'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Informe um e-mail válido.'
  return undefined
}

export function validateLoginPassword(value: string): string | undefined {
  if (!value) return 'Informe sua senha.'
  return undefined
}

export function getPasswordRules(password: string): PasswordRule[] {
  return [
    {
      key: 'length',
      label: '8 caracteres ou mais',
      met: password.length >= 8,
    },
    {
      key: 'uppercase',
      label: 'Uma letra maiúscula',
      met: /[A-Z]/.test(password),
    },
    {
      key: 'number',
      label: 'Um número',
      met: /[0-9]/.test(password),
    },
  ]
}

export function validateNewPassword(password: string): string | undefined {
  if (!password) return 'Crie uma senha.'
  if (password.length < 8) return 'A senha deve ter pelo menos 8 caracteres.'
  if (!/[A-Z]/.test(password)) return 'A senha deve conter ao menos uma letra maiúscula.'
  if (!/[0-9]/.test(password)) return 'A senha deve conter ao menos um número.'
  return undefined
}

export function getPasswordScore(password: string): number {
  return getPasswordRules(password).filter((rule) => rule.met).length
}

export function getPasswordStrengthLabel(password: string): string {
  const score = getPasswordScore(password)
  if (!password) return 'Aguardando sua senha'
  if (score === 3) return 'Senha forte'
  if (score === 2) return 'Quase lá'
  return 'Senha fraca'
}
