import React from 'react'
import styles from './Input.module.css'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
  hint?: string
}

export function Input({ label, error, hint, id, className = '', ...props }: InputProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-')
  return (
    <div className={styles.field}>
      <label className={styles.label} htmlFor={inputId}>{label}</label>
      <input
        id={inputId}
        className={[styles.input, error ? styles.hasError : '', className].join(' ')}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />
      {hint && !error && <p id={`${inputId}-hint`} className={styles.hint}>{hint}</p>}
      {error && <p id={`${inputId}-error`} className={styles.error} role="alert">{error}</p>}
    </div>
  )
}
