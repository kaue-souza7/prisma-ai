/**
 * API pública do pacote de mascotes 3D.
 * A demo usa o mesmo MascotViewer deste módulo.
 */
export { MascotViewer } from './viewer/MascotViewer.js';
export { CharacterController } from './core/CharacterController.js';
export { AnimationStateMachine } from './core/AnimationStateMachine.js';
export { MascotEventRouter } from './core/EventRouter.js';
export {
  ANIMATIONS,
  ANIMATION_BY_ID,
  ANIMATIONS_BY_CHARACTER,
  CHARACTERS,
  CHARACTER_LIST,
  CLIP_TO_ANIMATION,
  P1_ANIMATIONS,
  P2_ANIMATIONS,
  P3_ANIMATIONS,
  getAnimation,
  getAnimationsForCharacter,
  getClipName,
} from './core/catalog.js';
export { UX_EVENTS, UX_EVENT_BY_ID, sequenceLabel } from './core/events.js';

import { MascotViewer } from './viewer/MascotViewer.js';

/**
 * Cria um palco independente. O site pode usar apenas os GLBs/controlador,
 * mas esta fábrica cobre o caso Three.js + container DOM.
 */
export async function createMascotExperience(options) {
  const viewer = new MascotViewer(options);
  if (options?.character) {
    await viewer.showCharacter(options.character, { reset: true });
  }
  return viewer;
}
