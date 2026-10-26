import styles from './CoinsDisplay.module.css'

export function CoinsDisplay({
  coins,
  showLabel = false,
  compact = false,
}: {
  coins: number
  showLabel?: boolean
  compact?: boolean
}) {
  return (
    <span
      className={[styles.coins, compact ? styles.compact : ''].join(' ')}
      aria-label={`${coins} Prismas`}
      title={`${coins} Prismas`}
    >
      <span className={styles.gem} aria-hidden="true">◆</span>
      <strong>{coins.toLocaleString('pt-BR')}</strong>
      {showLabel && <span className={styles.label}>Prismas</span>}
    </span>
  )
}
