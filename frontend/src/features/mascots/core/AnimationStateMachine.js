import { ANIMATION_BY_ID } from './catalog.js';

/**
 * Máquina de estados pura (sem Three.js).
 * Recebe solicitações de animação, aplica as prioridades documentadas,
 * enfileira quando necessário e devolve a próxima animação após a atual.
 *
 * Prioridade: menor número = mais alta.
 */
export class AnimationStateMachine {
  constructor({ characterId, animations, idleId, onLog = null }) {
    this.characterId = characterId;
    this.animations = new Map(animations.map((animation) => [animation.id, animation]));
    this.idle = this.animations.get(idleId);
    if (!this.idle) throw new Error(`Idle ${idleId} não encontrado para ${characterId}`);
    this.onLog = onLog;
    this.current = null;
    this.queue = [];
    this.context = {
      textActive: false,
      panelOpen: false,
      recommendationActive: false,
      positiveProgressActive: false,
      trailCompleteActive: false,
    };
    this.reducedMotion = false;
    this.resetReason = null;
  }

  log(level, message, data = {}) {
    this.onLog?.({ level, message, characterId: this.characterId, ...data });
  }

  getSnapshot() {
    return {
      current: this.current,
      queue: this.queue.map((entry) => ({ animation: entry.animation, priority: entry.priority, source: entry.source })),
      context: { ...this.context },
      reducedMotion: this.reducedMotion,
    };
  }

  setTextActive(active) {
    this.context.textActive = Boolean(active);
    this.log('context', active ? 'Texto ativo: reações entram na fila.' : 'Texto encerrado.');
  }

  setContext(partial) {
    Object.assign(this.context, partial);
    this.log('context', 'Contexto atualizado.', { context: { ...this.context } });
  }

  setReducedMotion(enabled) {
    this.reducedMotion = Boolean(enabled);
  }

  isBlockedByContext(animation) {
    if (animation.id === 'A-05' && this.context.recommendationActive) {
      return 'A-05 é mutuamente exclusivo com A-03 na mesma abertura do painel.';
    }
    if (animation.id === 'A-03' && this.context.positiveProgressActive) {
      return 'A-03 não ocorre quando há progresso positivo na mesma abertura do painel.';
    }
    if (animation.id === 'C-11' && (this.context.trailCompleteActive || this.current?.id === 'C-12')) {
      return 'C-11 nunca ocorre junto de C-12; C-12 tem prioridade absoluta.';
    }
    return null;
  }

  /**
   * @param {string|object} animationOrId
   * @param {object} options
   * @param {number=} options.priority sobrescreve a prioridade do catálogo
   * @param {boolean=} options.force interrompe estados curtos (nunca os locked)
   * @param {boolean=} options.queue se false, simplesmente ignora em vez de enfileirar
   * @param {string=} options.source
   */
  request(animationOrId, options = {}) {
    const animation = typeof animationOrId === 'string' ? this.animations.get(animationOrId) : animationOrId;
    if (!animation) {
      return { action: 'ignore', reason: `Animação desconhecida: ${animationOrId}` };
    }
    const priority = options.priority ?? animation.priority;
    const source = options.source ?? 'api';
    const animate = { ...animation, effectivePriority: priority };

    const blocked = this.isBlockedByContext(animate);
    if (blocked) return { action: 'ignore', reason: blocked };

    if (!this.current) {
      return { action: 'play', animation: animate, priority, source, reason: 'sem estado ativo' };
    }

    if (this.current.id === animate.id) {
      if (!options.force) {
        return { action: 'ignore', reason: `${animate.id} já está em execução.` };
      }
      return { action: 'play', animation: animate, priority, source, reason: 'reinício forçado' };
    }

    if (this.current.locked && !options.interruptLocked) {
      return this.enqueue(animate, priority, source, options, 'estado protegido (locked) aguarda o fim');
    }

    // Proteção explícita do M-08 enquanto o texto do Mentor está ativo.
    // Nos demais estados de apresentação, a tabela de prioridades manda.
    if (this.context.textActive && this.current.id === 'M-08' && !animate.presentation) {
      return this.enqueue(animate, priority, source, options, 'texto ativo: reação aguarda o fim do texto');
    }

    const currentPriority = this.current.effectivePriority ?? this.current.priority;
    const isShortReaction = this.current.kind === 'reaction' || this.current.kind === 'celebration';

    if (isShortReaction) {
      if (!options.force && !(priority < currentPriority && priority === 1)) {
        return this.enqueue(animate, priority, source, options, 'reação curta em curso: aguarda conclusão');
      }
    }

    if (animate.presentation && this.context.textActive && priority <= currentPriority) {
      return { action: 'play', animation: animate, priority, source, reason: 'apresentação de texto assume' };
    }

    if (options.force || priority < currentPriority) {
      return { action: 'play', animation: animate, priority, source, reason: 'prioridade maior' };
    }

    if (priority === currentPriority && this.current.kind === 'idle') {
      return { action: 'play', animation: animate, priority, source, reason: 'substitui idle' };
    }

    return this.enqueue(animate, priority, source, options, 'prioridade menor ou igual');
  }

  enqueue(animation, priority, source, options, reason) {
    if (options.queue === false) {
      return { action: 'ignore', reason };
    }
    if (this.queue.some((entry) => entry.animation.id === animation.id)) {
      return { action: 'ignore', reason: `${animation.id} já está na fila.` };
    }
    if (this.queue.length >= 12) {
      this.queue.shift();
      this.log('warn', 'Fila cheia: descartando a solicitação mais antiga.');
    }
    const entry = {
      animation,
      priority,
      source,
      requestedAt: Date.now(),
    };
    this.queue.push(entry);
    this.queue.sort((a, b) => a.priority - b.priority || a.requestedAt - b.requestedAt);
    return { action: 'queue', animation, priority, source, reason };
  }

  acceptPlay(animation, priority, source) {
    this.current = { ...animation, effectivePriority: priority ?? animation.priority, source };
  }

  /** A atual terminou ou o texto fechou; devolve a próxima ou idle. */
  finishCurrent() {
    const previous = this.current;
    this.current = null;
    while (this.queue.length > 0) {
      const entry = this.queue.shift();
      if (this.isBlockedByContext(entry.animation)) {
        this.log('warn', 'Item da fila descartado por conflito de contexto.', { id: entry.animation.id });
        continue;
      }
      return {
        animation: { ...entry.animation, effectivePriority: entry.priority, source: entry.source },
        priority: entry.priority,
        source: entry.source,
        fromQueue: true,
        previous,
      };
    }
    return {
      animation: this.idle,
      priority: this.idle.priority,
      source: 'auto-idle',
      fromQueue: false,
      previous,
    };
  }

  clearQueue() {
    this.queue = [];
  }

  reset() {
    this.current = null;
    this.queue = [];
    this.context.textActive = false;
    this.resetReason = 'manual';
  }

  get hasQueue() {
    return this.queue.length > 0;
  }
}

export function createMachineFor(characterId, animations, idleId, onLog) {
  const resolved = animations ?? Object.values(ANIMATION_BY_ID);
  return new AnimationStateMachine({ characterId, animations: resolved, idleId, onLog });
}
