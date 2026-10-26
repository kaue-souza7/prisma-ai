import { forwardRef, useId, useState } from 'react'
import type { InputHTMLAttributes, ReactNode } from 'react'
import { AlertCircleIcon, EyeIcon, EyeOffIcon } from '@/design-system/Icons'
import styles from './AuthField.module.css'

interface AuthFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label: string
  icon: ReactNode
  error?: string
  hint?: string
  labelAction?: ReactNode
  extraDescribedBy?: string
}

export const AuthField = forwardRef<HTMLInputElement, AuthFieldProps>(function AuthField(
  {
    label,
    icon,
    error,
    hint,
    labelAction,
    extraDescribedBy,
    id,
    type = 'text',
    className = '',
    ...props
  },
  ref,
) {
  const generatedId = useId().replace(/:/g, '')
  const inputId = id || `auth-field-${generatedId}`
  const [visible, setVisible] = useState(false)
  const isPassword = type === 'password'
  const resolvedType = isPassword && visible ? 'text' : type
  const describedBy = [
    error ? `${inputId}-error` : '',
    hint ? `${inputId}-hint` : '',
    extraDescribedBy || '',
  ]
    .filter(Boolean)
    .join(' ') || undefined

  return (
    <div className={`${styles.field} ${className}`}>
      <div className={styles.labelRow}>
        <label className={styles.label} htmlFor={inputId}>
          {label}
        </label>
        {labelAction && <span className={styles.labelAction}>{labelAction}</span>}
      </div>

      <div className={`${styles.control} ${error ? styles.invalid : ''}`}>
        <span className={styles.icon} aria-hidden="true">
          {icon}
        </span>

        <input
          ref={ref}
          id={inputId}
          type={resolvedType}
          className={styles.input}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy}
          {...props}
        />

        {isPassword && (
          <button
            type="button"
            className={styles.reveal}
            onClick={() => setVisible((value) => !value)}
            aria-label={visible ? 'Ocultar senha' : 'Mostrar senha'}
            aria-pressed={visible}
          >
            {visible ? <EyeOffIcon size={17} /> : <EyeIcon size={17} />}
          </button>
        )}
      </div>

      {hint && !error && (
        <p id={`${inputId}-hint`} className={styles.hint}>
          {hint}
        </p>
      )}

      {error && (
        <p id={`${inputId}-error`} className={styles.error} role="alert">
          <AlertCircleIcon size={14} />
          <span>{error}</span>
        </p>
      )}
    </div>
  )
})
