import { CheckIcon } from '@/design-system/Icons'
import {
  getPasswordRules,
  getPasswordScore,
  getPasswordStrengthLabel,
} from '../validation'
import styles from './PasswordStrength.module.css'

export function PasswordStrength({ password, id }: { password: string; id?: string }) {
  const score = getPasswordScore(password)
  const label = getPasswordStrengthLabel(password)
  const rules = getPasswordRules(password)

  return (
    <div className={styles.meter} id={id}>
      <div className={styles.top} aria-live="polite">
        <span>Força da senha</span>
        <strong data-score={score}>{label}</strong>
      </div>

      <div className={styles.track} aria-hidden="true">
        <span className={styles.fill} data-score={score} />
      </div>

      <ul className={styles.rules}>
        {rules.map((rule) => (
          <li key={rule.key} className={rule.met ? styles.met : ''}>
            <span aria-hidden="true">{rule.met ? <CheckIcon size={10} /> : null}</span>
            {rule.label}
          </li>
        ))}
      </ul>
    </div>
  )
}
