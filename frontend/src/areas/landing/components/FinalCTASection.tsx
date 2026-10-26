import { Link } from 'react-router-dom'
import { ArrowRightIcon, SparkIcon } from '@/design-system/Icons'
import { Magnetic, Reveal } from './primitives'
import { PrismArt } from '@/design-system/brand/PrismArt'

export function FinalCTASection() {
  return (
    <section className="pl-section pl-final-cta">
      <div className="pl-container">
        <Reveal>
          <div className="pl-final-card">
            <PrismArt className="pl-final-prism" variant="cta" />
            <div className="pl-final-glow" aria-hidden="true" />
            <div className="pl-final-content">
              <p className="pl-eyebrow">
                <span className="pl-eyebrow-dot" aria-hidden="true" />
                Comece agora
              </p>
              <h2>Seis fases. Dezoito missões. Uma nova relação com o dinheiro.</h2>
              <p>
                Do primeiro salário à proteção digital — pratique decisões financeiras
                reais em cenários seguros e avance por competências demonstradas.
              </p>
              <div className="pl-final-actions">
                <Magnetic strength={8}>
                  <Link to="/register" className="pl-btn pl-btn--primary pl-btn--hero">
                    Começar minha jornada
                    <span className="pl-btn-icon"><ArrowRightIcon size={18} /></span>
                  </Link>
                </Magnetic>
                <Link to="/login" className="pl-btn pl-btn--glass pl-btn--hero">
                  Já tenho uma conta
                </Link>
              </div>
              <div className="pl-final-note">
                <SparkIcon size={14} />
                Sem dados bancários. Sem transações reais. Só aprendizado.
              </div>
            </div>
            <div className="pl-final-orbit pl-final-orbit--one" aria-hidden="true" />
            <div className="pl-final-orbit pl-final-orbit--two" aria-hidden="true" />
          </div>
        </Reveal>
      </div>
    </section>
  )
}
