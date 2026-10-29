import { ANIMATION_BY_ID } from './catalog.js';
import { UX_EVENT_BY_ID } from './events.js';

/**
 * Camada de simulação de eventos de UX. Não é necessária no site: ela existe
 * para validar as máquinas de estado sem depender do backend.
 */
export class MascotEventRouter {
  constructor({ resolveController, onLog = null, onTimer = null }) {
    this.resolveController = resolveController;
    this.onLog = onLog;
    this.onTimer = onTimer;
    this.timers = new Set();
    this.token = 0;
    this.lastEvent = null;
  }

  log(level, message, data = {}) {
    this.onLog?.({ level, message, ...data });
  }

  clearTimers() {
    for (const timer of this.timers) clearTimeout(timer);
    this.timers.clear();
  }

  schedule(callback, delay) {
    const timer = setTimeout(() => {
      this.timers.delete(timer);
      callback();
    }, Math.max(0, delay));
    this.timers.add(timer);
    this.onTimer?.(this.timers.size);
    return timer;
  }

  async dispatch(eventId, options = {}) {
    const definition = UX_EVENT_BY_ID[eventId];
    if (!definition) throw new Error(`Evento desconhecido: ${eventId}`);
    const { reset = true, focus = true, autoReturn = true } = options;
    this.clearTimers();
    const token = ++this.token;
    this.lastEvent = eventId;

    const controller = await this.resolveController(definition.character, { focus });
    if (!controller) {
      throw new Error(`Controlador indisponível para ${definition.character}`);
    }

    if (reset) {
      controller.stopAnimation();
      this.log('info', `Estado de ${definition.character} reiniciado para a simulação.`, { event: eventId });
    }

    controller.setContext({
      panelOpen: false,
      recommendationActive: false,
      positiveProgressActive: false,
      trailCompleteActive: false,
      ...(definition.context || {}),
    });

    if (definition.text) {
      controller.setTextActive(true);
    }

    const sequence = definition.sequence;
    const results = [];
    for (let i = 0; i < sequence.length; i++) {
      const animationId = sequence[i];
      const animation = ANIMATION_BY_ID[animationId];
      if (!animation) throw new Error(`Animação inexistente no evento ${eventId}: ${animationId}`);
      const result = controller.play(animationId, {
        force: i === 0,
        clearQueue: i === 0,
        source: `event:${eventId}`,
      });
      results.push({ animationId, result });
      this.log('info', `${animationId} ${animation.name} → ${result.action ?? 'ignored'}${result.reason ? ` (${result.reason})` : ''}`, {
        event: eventId,
        animationId,
      });
    }

    this.log('event', `${definition.label}: ${sequence.join(' → ')}`, { event: eventId });

    // Encerramento automático da apresentação de texto apenas para a demo.
    if (definition.text && autoReturn) {
      const presentationIndex = sequence.findIndex((id) => ANIMATION_BY_ID[id]?.presentation);
      const index = presentationIndex === -1 ? sequence.length - 1 : presentationIndex;
      const before = sequence
        .slice(0, index)
        .reduce((sum, id) => sum + (ANIMATION_BY_ID[id]?.duration ?? 0), 0);
      const duration = definition.textMs ?? 5000;
      this.schedule(() => {
        if (token !== this.token) return;
        const state = controller.getState();
        const presentationIds = sequence.filter((id) => ANIMATION_BY_ID[id]?.presentation);
        if (presentationIds.includes(state.currentId) && state.textActive) {
          this.log('info', 'Texto encerrado: retorno automático ao idle.', { event: eventId });
          controller.endText();
        }
      }, (before + 0.3) * 1000 + duration);
    }

    // Loops de espera (digitação/processamento/escuta) são encerrados na demo
    // para permitir que o visitante continue testando.
    if (definition.holdMs && autoReturn) {
      const lastId = sequence[sequence.length - 1];
      this.schedule(() => {
        if (token !== this.token) return;
        const state = controller.getState();
        if (state.currentId === lastId) {
          this.log('info', 'Fim da simulação do loop: retorno ao idle.', { event: eventId });
          controller.stopAnimation();
        }
      }, definition.holdMs);
    }

    if (definition.secondary) {
      this.log(
        'info',
        `Reação secundária prevista: ${definition.secondary.sequence.join(', ')} em ${definition.secondary.character}. ` +
          'No site, ocorre em outra tela/painel; selecione o personagem para inspecioná-la aqui.',
        { event: eventId },
      );
      if (!autoReturn) {
        this.schedule(async () => {
          if (token !== this.token) return;
          const secondary = await this.resolveController(definition.secondary.character, { focus: false, load: false });
          if (secondary) {
            for (const id of definition.secondary.sequence) {
              secondary.play(id, { force: true, source: `event:${eventId}:secondary` });
            }
          }
        }, definition.secondary.delayMs ?? 1500);
      }
    }

    return { event: definition, controller, results };
  }

  cancelPending() {
    this.clearTimers();
    this.token++;
  }
}
