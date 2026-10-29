import * as THREE from 'three';
import {
  ANIMATIONS_BY_CHARACTER,
  ANIMATION_BY_ID,
  CHARACTERS,
  getAnimation,
} from './catalog.js';
import { AnimationStateMachine } from './AnimationStateMachine.js';

const IDLE_BY_CHARACTER = {
  catalisador: 'C-01',
  mentor: 'M-01',
  analista: 'A-01',
};

const DEFAULT_FADE = 0.25;
const REDUCED_FADE = 0.2;

function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}

/**
 * Controlador de um mascote carregado. Recebe um GLTF já parseado
 * (gltf.scene + gltf.animations) e opera sobre o AnimationMixer.
 */
export class CharacterController {
  constructor({ characterId, gltf, fade = DEFAULT_FADE, reducedMotion = false, onEvent = null }) {
    if (!CHARACTERS[characterId]) throw new Error(`Personagem inválido: ${characterId}`);
    if (!gltf?.scene || !gltf.animations?.length) throw new Error(`GLTF inválido para ${characterId}`);
    this.characterId = characterId;
    this.gltf = gltf;
    this.root = gltf.scene;
    this.fade = fade;
    this.onEvent = onEvent;
    this.listeners = new Map();
    this.visible = true;
    this.pauseReasons = new Set();
    this.currentAction = null;
    this.currentSpec = null;
    this.currentSource = null;
    this.lastDecision = null;
    this.fadeOuts = [];
    this.staticRemaining = 0;
    this.pendingTextEnd = 0;
    this.reducedMotion = Boolean(reducedMotion);
    this.renderedClip = null;
    this.loadingReplacement = false;
    this.startedAt = 0;
    this._mediaQuery = null;

    const animations = ANIMATIONS_BY_CHARACTER[characterId];
    this.animations = animations;
    this.animationById = Object.fromEntries(animations.map((animation) => [animation.id, animation]));
    this.idleSpec = this.animationById[IDLE_BY_CHARACTER[characterId]];
    this.machine = new AnimationStateMachine({
      characterId,
      animations,
      idleId: IDLE_BY_CHARACTER[characterId],
      onLog: (entry) => this.emit('log', entry),
    });
    this.machine.setReducedMotion(this.reducedMotion);

    this.clips = new Map(gltf.animations.map((clip) => [clip.name, clip]));
    for (const animation of animations) {
      if (!this.clips.has(animation.clip)) {
        throw new Error(`Clipe ausente no GLB de ${characterId}: ${animation.clip} (${animation.id})`);
      }
    }
    this.mixer = new THREE.AnimationMixer(this.root);
    this.actions = new Map();
    for (const clip of gltf.animations) {
      this.actions.set(clip.name, this.mixer.clipAction(clip));
    }
    this.mixer.addEventListener('finished', (event) => this.handleFinished(event));
  }

  on(event, listener) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event).add(listener);
    return () => this.listeners.get(event)?.delete(listener);
  }

  emit(event, payload) {
    const data = { type: event, characterId: this.characterId, ...payload };
    this.onEvent?.(data);
    for (const listener of this.listeners.get(event) ?? []) {
      try {
        listener(data);
      } catch (error) {
        console.error(`[${this.characterId}] erro em listener ${event}`, error);
      }
    }
  }

  play(animationId, options = {}) {
    const spec = getAnimation(animationId);
    if (!spec || spec.character !== this.characterId) {
      const message = `Animação ${animationId} não pertence a ${this.characterId}.`;
      this.emit('ignored', { animationId, reason: message });
      return { ok: false, reason: message };
    }
    if (options.clearQueue) this.machine.clearQueue();
    const decision = this.machine.request(spec, {
      priority: options.priority,
      force: options.force ?? false,
      queue: options.queue ?? true,
      source: options.source ?? 'api',
      interruptLocked: options.interruptLocked ?? false,
    });
    this.lastDecision = decision.reason;
    if (decision.action === 'play') {
      this.machine.acceptPlay(decision.animation, decision.priority, decision.source);
      this.startAnimation(decision.animation, { fade: options.fade });
      return { ok: true, action: 'play', animation: spec.id };
    }
    if (decision.action === 'queue') {
      this.emit('queued', {
        animation: decision.animation,
        priority: decision.priority,
        reason: decision.reason,
        queue: this.machine.getSnapshot().queue,
      });
      this.emitState('queued');
      return { ok: true, action: 'queue', animation: spec.id, reason: decision.reason };
    }
    this.emit('ignored', { animationId, reason: decision.reason });
    return { ok: false, action: 'ignore', reason: decision.reason };
  }

  /** Compatível com a API solicitada: playAnimation(id) interrompe o estado atual. */
  playAnimation(animationId) {
    return this.play(animationId, { force: true, clearQueue: true, source: 'playAnimation' });
  }

  /** Compatível com a API solicitada: triggerAnimation(id, priority). */
  triggerAnimation(animationId, priority) {
    return this.play(animationId, { priority, force: false, source: 'triggerAnimation' });
  }

  startAnimation(spec, { fade = this.fade, fromQueue = false } = {}) {
    if (!spec) return;
    const transitionFade = this.reducedMotion ? Math.min(fade, REDUCED_FADE) : fade;
    if (this.currentAction) {
      const old = this.currentAction;
      if (old !== this.actions.get(spec.clip)) {
        old.fadeOut(transitionFade);
        this.fadeOuts.push({ action: old, remaining: transitionFade + 0.015 });
      }
    }

    const reduced = this.reducedMotion;
    const replacement = reduced && spec.reducedReplacement === 'loading';
    const renderedSpec = replacement ? this.idleSpec : spec;
    const clip = this.clips.get(renderedSpec.clip);
    const action = this.actions.get(renderedSpec.clip);
    if (!clip || !action) {
      this.emit('error', { message: `Clipe não encontrado: ${renderedSpec.clip}` });
      return;
    }

    // Remove eventual fade-out pendente para esta mesma action.
    this.fadeOuts = this.fadeOuts.filter((entry) => entry.action !== action);
    action.stop();
    action.reset();
    action.enabled = true;
    action.setEffectiveWeight(1);
    action.setEffectiveTimeScale(1);
    action.paused = false;
    action.clampWhenFinished = true;

    const shouldPause = reduced;
    if (shouldPause) {
      action.setLoop(THREE.LoopOnce, 1);
      action.time = Math.max(0, Math.min(clip.duration, spec.reducedPose * clip.duration));
    } else if (spec.loop) {
      action.setLoop(THREE.LoopRepeat, Infinity);
      action.time = 0;
    } else {
      action.setLoop(THREE.LoopOnce, 1);
      action.time = 0;
    }
    action.play();
    action.fadeIn(transitionFade);
    if (shouldPause) {
      action.paused = true;
      action.time = Math.max(0, Math.min(clip.duration, spec.reducedPose * clip.duration));
    }

    this.currentAction = action;
    this.currentSpec = { ...spec };
    this.renderedClip = renderedSpec.clip;
    this.loadingReplacement = Boolean(replacement);
    this.currentSource = spec.source;
    this.startedAt = performance.now();
    this.staticRemaining = 0;
    this.pendingTextEnd = 0;
    if (reduced && !spec.loop) {
      const isPresentation = Boolean(spec.presentation);
      if (!isPresentation && !replacement) {
        this.staticRemaining = Math.max(0.9, spec.duration * 0.92);
      }
    }

    this.emit('animationstart', {
      animation: spec,
      previous: this.lastStartedSpec ?? null,
      reduced,
      replacement,
      fade: transitionFade,
      fromQueue,
      clip: renderedSpec.clip,
    });
    this.lastStartedSpec = spec;
    this.emitState('playing');
  }

  handleFinished(event) {
    if (event.action !== this.currentAction) return;
    if (!this.currentSpec) return;
    if (this.reducedMotion) return;
    if (this.currentSpec.loop) return;
    this.finishAndAdvance('finished');
  }

  finishAndAdvance(reason = 'finished') {
    if (!this.currentSpec) return;
    const previous = this.currentSpec;
    const next = this.machine.finishCurrent();
    const fade = this.reducedMotion ? REDUCED_FADE : this.fade;
    this.machine.acceptPlay(next.animation, next.priority, next.source);
    this.startAnimation(next.animation, { fade, fromQueue: next.fromQueue });
    this.emit('transition', {
      from: previous.id,
      to: next.animation.id,
      reason,
      priority: next.priority,
      fromQueue: next.fromQueue,
    });
  }

  endText() {
    this.machine.setTextActive(false);
    this.emit('text', { active: false });
    this.requestPresentationEnd();
    this.emitState('text-ended');
  }

  requestPresentationEnd() {
    if (!this.currentSpec?.presentation) return;
    const delay = Number(this.currentSpec.textEndDelay ?? 0);
    if (delay > 0) {
      this.pendingTextEnd = delay;
    } else {
      this.finishAndAdvance('text-ended');
    }
  }

  setTextActive(active) {
    this.machine.setTextActive(active);
    this.emit('text', { active });
    if (!active) this.requestPresentationEnd();
    this.emitState('text');
  }

  setContext(partial) {
    this.machine.setContext(partial);
    this.emitState('context');
  }

  setReducedMotion(enabled, { silent = false } = {}) {
    const next = Boolean(enabled);
    if (next === this.reducedMotion) return;
    this.reducedMotion = next;
    this.machine.setReducedMotion(next);
    if (!silent) {
      this.emit('motionmode', { reducedMotion: next });
    }
    if (this.currentSpec) {
      this.startAnimation(this.currentSpec, { fade: next ? REDUCED_FADE : this.fade });
    }
    this.emitState('reduced-motion');
  }

  stopAnimation({ toIdle = true } = {}) {
    this.machine.clearQueue();
    this.machine.reset();
    this.fadeOuts = [];
    this.staticRemaining = 0;
    this.pendingTextEnd = 0;
    if (!toIdle) {
      if (this.currentAction) this.currentAction.fadeOut(this.fade);
      this.currentAction = null;
      this.currentSpec = null;
      this.emitState('stopped');
      return;
    }
    const idle = this.idleSpec;
    this.machine.acceptPlay(idle, idle.priority, 'stop');
    this.startAnimation(idle, { fade: this.fade });
    this.pendingTextEnd = 0;
    this.emit('stopped', {});
  }

  setVisible(visible) {
    const next = Boolean(visible);
    if (next === this.visible) return;
    this.visible = next;
    this.emit('visibility', { visible: next });
    this.emitState('visibility');
  }

  setPaused(paused, reason = 'manual') {
    if (paused) this.pauseReasons.add(reason);
    else this.pauseReasons.delete(reason);
    this.emitState('pause');
  }

  isRunning() {
    return this.visible && this.pauseReasons.size === 0;
  }

  update(dt) {
    if (!this.isRunning()) return;
    const delta = Math.min(dt || 0, 0.12);
    this.mixer.update(delta);

    if (this.fadeOuts.length > 0) {
      for (const entry of this.fadeOuts) entry.remaining -= delta;
      const done = this.fadeOuts.filter((entry) => entry.remaining <= 0);
      for (const entry of done) {
        if (entry.action !== this.currentAction) entry.action.stop();
      }
      this.fadeOuts = this.fadeOuts.filter((entry) => entry.remaining > 0);
    }

    if (this.pendingTextEnd > 0 && this.currentSpec) {
      this.pendingTextEnd -= delta;
      if (this.pendingTextEnd <= 0) {
        this.pendingTextEnd = 0;
        this.finishAndAdvance('text-ended');
      }
    }

    if (this.reducedMotion && this.staticRemaining > 0 && this.currentSpec) {
      this.staticRemaining -= delta;
      if (this.staticRemaining <= 0) {
        this.staticRemaining = 0;
        this.finishAndAdvance('reduced-pose-ended');
      }
    }
  }

  getProgress() {
    if (!this.currentAction) return 0;
    const duration = this.currentAction.getClip().duration || 1;
    return clamp01((this.currentAction.time || 0) / duration);
  }

  getState() {
    const queue = this.machine.getSnapshot().queue.map((entry) => ({
      id: entry.animation.id,
      name: entry.animation.name,
      priority: entry.priority,
      source: entry.source,
    }));
    return {
      characterId: this.characterId,
      currentId: this.currentSpec?.id ?? null,
      currentName: this.currentSpec?.name ?? null,
      currentKind: this.currentSpec?.kind ?? null,
      currentPriority: this.currentSpec?.effectivePriority ?? this.currentSpec?.priority ?? null,
      currentLoop: Boolean(this.currentSpec?.loop),
      renderedClip: this.renderedClip,
      duration: this.currentSpec?.duration ?? 0,
      progress: this.getProgress(),
      queue,
      reducedMotion: this.reducedMotion,
      loadingReplacement: this.loadingReplacement,
      pendingTextEnd: Number(this.pendingTextEnd.toFixed(2)),
      textActive: this.machine.context.textActive,
      visible: this.visible,
      running: this.isRunning(),
      pausedReasons: [...this.pauseReasons],
      lastDecision: this.lastDecision,
      context: { ...this.machine.context },
      source: this.currentSource,
    };
  }

  emitState(reason) {
    this.emit('statechange', { state: this.getState(), reason });
  }

  dispose() {
    this.mixer.stopAllAction();
    this.listeners.clear();
    this.currentAction = null;
    this.machine.clearQueue();
  }
}

export { IDLE_BY_CHARACTER, DEFAULT_FADE, REDUCED_FADE };
