export function pluralize(count: number, singular: string, plural: string) {
  return `${count} ${count === 1 ? singular : plural}`
}

export function displayName(email?: string | null) {
  if (!email) return 'Estudante'
  const local = email.split('@')[0].split('.')[0]
  return local.charAt(0).toUpperCase() + local.slice(1)
}
