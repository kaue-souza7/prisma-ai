import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { CharacterController } from '../core/CharacterController.js';
import { CHARACTERS, getAnimation } from '../core/catalog.js';

const IDLE = { catalisador: 'C-01', mentor: 'M-01', analista: 'A-01' };

/**
 * Palco Three.js independente, com carregamento lazy por mascote.
 * Pode ser embutido em qualquer container; a demo usa este mesmo componente.
 */
export class MascotViewer {
  constructor({
    container,
    modelBaseUrl = '/src/assets/models',
    reducedMotion = null,
    fade = 0.25,
    pixelRatio = null,
    autoResize = true,
    // Na integração com o app, o piso escuro do demo é opcional.
    showFloor = false,
    shadows = true,
  }) {
    if (!container) throw new Error('MascotViewer requer um container DOM.');
    this.container = container;
    this.modelBaseUrl = modelBaseUrl.replace(/\/$/, '');
    this.fade = fade;
    this.showFloor = showFloor;
    this.shadowsRequested = shadows;
    this.listeners = new Map();
    this.characters = new Map();
    this.loading = new Map();
    this.activeId = null;
    this.stageVisible = true;
    this.documentVisible = !document.hidden;
    this.scrollPaused = false;
    this.busy = false;
    this.disposed = false;
    this.scrollTimer = null;
    this.lastTime = performance.now();
    this.resize = this.resize.bind(this);

    const mq = window.matchMedia?.('(prefers-reduced-motion: reduce)');
    this.systemReducedMotion = mq?.matches ?? false;
    this.reducedMotion = reducedMotion === null ? this.systemReducedMotion : Boolean(reducedMotion);
    this._mqListener = (event) => {
      this.systemReducedMotion = event.matches;
      this.emit('systempreference', { reducedMotion: event.matches });
    };
    mq?.addEventListener?.('change', this._mqListener);

    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance',
    });
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.NeutralToneMapping;
    this.renderer.toneMappingExposure = 0.95;
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.shadowsEnabled = this.shadowsRequested && window.innerWidth > 760;
    const dpr = pixelRatio ?? Math.min(window.devicePixelRatio || 1, 2);
    this.renderer.setPixelRatio(dpr);
    this.renderer.domElement.className = 'mascot-canvas';
    this.renderer.domElement.setAttribute('aria-label', 'Mascote 3D interativo. Arraste para orbitar.');
    this.renderer.domElement.setAttribute('role', 'img');
    container.appendChild(this.renderer.domElement);

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(30, 1, 0.1, 80);
    this.camera.position.set(0.95, 1.82, 6.15);
    this.cameraTarget = new THREE.Vector3(0, 1.16, 0);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.copy(this.cameraTarget);
    this.controls.enablePan = false;
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.06;
    this.controls.minDistance = 4.2;
    this.controls.maxDistance = 10;
    this.controls.minPolarAngle = Math.PI * 0.22;
    this.controls.maxPolarAngle = Math.PI * 0.56;
    this.controls.minAzimuthAngle = -Math.PI * 0.45;
    this.controls.maxAzimuthAngle = Math.PI * 0.45;
    this.controls.update();

    this.setupScene();
    this.setupEnvironment();
    this.setupLights();
    this.setupFloor();

    this.clock = new THREE.Clock();
    this.resizeObserver = autoResize
      ? new ResizeObserver(() => this.resize())
      : null;
    this.resizeObserver?.observe(container);
    this.resize();

    this.visibilityObserver = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (!entry) return;
        this.stageVisible = entry.isIntersecting;
        this.applyActivity();
        this.emit('stagevisibility', { visible: this.stageVisible });
      },
      { threshold: 0.08 },
    );
    this.visibilityObserver.observe(container);
    document.addEventListener('visibilitychange', this.handleDocumentVisibility);
    window.addEventListener('scroll', this.handleScroll, { passive: true });
    window.addEventListener('resize', this.resize);

    this.animate = this.animate.bind(this);
    this.raf = requestAnimationFrame(this.animate);
  }

  setupScene() {
    this.scene.fog = new THREE.FogExp2('#070b13', 0.022);
  }

  setupEnvironment() {
    const pmrem = new THREE.PMREMGenerator(this.renderer);
    const room = new RoomEnvironment();
    this.environment = pmrem.fromScene(room, 0.04).texture;
    this.scene.environment = this.environment;
    this.scene.environmentIntensity = 0.34;
    room.dispose?.();
    pmrem.dispose();
  }

  setupLights() {
    this.hemi = new THREE.HemisphereLight('#dce9ff', '#070a10', 0.55);
    this.scene.add(this.hemi);

    this.key = new THREE.DirectionalLight('#fff4e3', 1.35);
    this.key.position.set(3.6, 5.6, 4.2);
    this.key.castShadow = this.shadowsEnabled;
    const shadowSize = Math.min(window.devicePixelRatio || 1, 2) > 1.5 ? 2048 : 1024;
    this.key.shadow.mapSize.set(shadowSize, shadowSize);
    this.key.shadow.camera.left = -4.5;
    this.key.shadow.camera.right = 4.5;
    this.key.shadow.camera.top = 5.5;
    this.key.shadow.camera.bottom = -2;
    this.key.shadow.camera.near = 0.1;
    this.key.shadow.camera.far = 16;
    this.renderer.shadowMap.enabled = this.shadowsEnabled;
    this.key.shadow.bias = -0.00035;
    this.key.shadow.normalBias = 0.02;
    this.scene.add(this.key);

    this.fill = new THREE.DirectionalLight('#9fc7ff', 0.38);
    this.fill.position.set(-4, 3.2, 3.4);
    this.scene.add(this.fill);

    this.rim = new THREE.PointLight('#FCA048', 7, 9, 2);
    this.rim.position.set(-2.2, 2.6, -2.4);
    this.scene.add(this.rim);
  }

  setupFloor() {
    if (this.showFloor) {
      this.floor = new THREE.Mesh(
        new THREE.CircleGeometry(18, 128),
        new THREE.MeshStandardMaterial({
          color: '#0a1019',
          roughness: 0.57,
          metalness: 0.12,
        }),
      );
      this.floor.rotation.x = -Math.PI / 2;
      this.floor.position.y = -0.005;
      this.floor.receiveShadow = true;
      this.scene.add(this.floor);

      this.ringMaterial = new THREE.MeshBasicMaterial({
        color: '#FCA048',
        transparent: true,
        opacity: 0.38,
        depthWrite: false,
        side: THREE.DoubleSide,
      });
      this.ring = new THREE.Mesh(new THREE.RingGeometry(1.27, 1.292, 160), this.ringMaterial);
      this.ring.rotation.x = -Math.PI / 2;
      this.ring.position.y = 0.002;
      this.scene.add(this.ring);

      this.ringMaterialSoft = new THREE.MeshBasicMaterial({
        color: '#FCA048',
        transparent: true,
        opacity: 0.09,
        depthWrite: false,
        side: THREE.DoubleSide,
      });
      this.ringSoft = new THREE.Mesh(new THREE.RingGeometry(1.6, 1.72, 160), this.ringMaterialSoft);
      this.ringSoft.rotation.x = -Math.PI / 2;
      this.ringSoft.position.y = 0.001;
      this.scene.add(this.ringSoft);
    }

    // Halo de contato com textura radial gerada localmente (sem assets externos).
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const context = canvas.getContext('2d');
    const gradient = context.createRadialGradient(128, 128, 8, 128, 128, 126);
    gradient.addColorStop(0, 'rgba(0,0,0,0.42)');
    gradient.addColorStop(0.42, 'rgba(0,0,0,0.25)');
    gradient.addColorStop(1, 'rgba(0,0,0,0)');
    context.fillStyle = gradient;
    context.fillRect(0, 0, 256, 256);
    const shadowTexture = new THREE.CanvasTexture(canvas);
    shadowTexture.colorSpace = THREE.SRGBColorSpace;
    this.shadowHalo = new THREE.Mesh(
      new THREE.PlaneGeometry(2.8, 2.8),
      new THREE.MeshBasicMaterial({
        map: shadowTexture,
        transparent: true,
        depthWrite: false,
        opacity: 0.8,
      }),
    );
    this.shadowHalo.rotation.x = -Math.PI / 2;
    this.shadowHalo.position.y = 0.004;
    this.scene.add(this.shadowHalo);
  }

  on(event, listener) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event).add(listener);
    return () => this.listeners.get(event)?.delete(listener);
  }

  emit(event, payload = {}) {
    for (const listener of this.listeners.get(event) ?? []) {
      try {
        listener(payload);
      } catch (error) {
        console.error(`Erro no listener ${event}`, error);
      }
    }
  }

  async loadCharacter(characterId) {
    if (!CHARACTERS[characterId]) throw new Error(`Personagem inválido: ${characterId}`);
    if (this.characters.has(characterId)) return this.characters.get(characterId).controller;
    if (this.loading.has(characterId)) return this.loading.get(characterId);

    const loadPromise = (async () => {
      this.emit('loadstart', { characterId });
      const loader = new GLTFLoader();
      const url = `${this.modelBaseUrl}/${CHARACTERS[characterId].modelFile}`;
      const gltf = await loader.loadAsync(url, (event) => {
        const total = event.total || 0;
        const loaded = event.loaded || 0;
        this.emit('loadprogress', {
          characterId,
          loaded,
          total,
          ratio: total > 0 ? loaded / total : null,
        });
      });
      const root = gltf.scene;
      root.visible = false;
      const noShadow = /^(Eye_|Iris_|Pupil_|Shine_|HappyEye_|Brow_.*Mesh$|Mouth$|Mouth_Teeth$|Mouth_Tongue$|Glasses_Mesh$|Tablet_UI|Tablet_Screen|Tablet_Camera|Book_.*Detail$|Shoe_.*_Detail$)/;
      root.traverse((node) => {
        if (node.isMesh || node.isSkinnedMesh) {
          node.castShadow = !noShadow.test(node.name);
          node.receiveShadow = true;
          const materials = Array.isArray(node.material) ? node.material : [node.material];
          for (const material of materials) {
            if (!material) continue;
            material.envMapIntensity = 0.8;
            material.needsUpdate = true;
          }
        }
      });
      const controller = new CharacterController({
        characterId,
        gltf,
        fade: this.fade,
        reducedMotion: this.reducedMotion,
      });
      const forwardEvents = [
        'statechange',
        'animationstart',
        'transition',
        'queued',
        'ignored',
        'text',
        'motionmode',
        'visibility',
        'stopped',
        'log',
        'error',
      ];
      for (const event of forwardEvents) {
        controller.on(event, (data) => this.emit(event, data));
      }
      this.scene.add(root);
      const item = { characterId, gltf, root, controller };
      this.characters.set(characterId, item);
      this.emit('loadend', { characterId, controller, animations: gltf.animations.length });
      return controller;
    })();

    this.loading.set(characterId, loadPromise);
    try {
      return await loadPromise;
    } finally {
      this.loading.delete(characterId);
    }
  }

  async showCharacter(characterId, { reset = true } = {}) {
    const controller = await this.loadCharacter(characterId);
    if (this.disposed) return controller;
    if (this.activeId && this.activeId !== characterId) {
      const previous = this.characters.get(this.activeId);
      if (previous) {
        previous.controller.setVisible(false);
        previous.root.visible = false;
      }
    }
    this.activeId = characterId;
    const item = this.characters.get(characterId);
    item.root.visible = true;
    controller.setVisible(this.stageVisible && this.documentVisible);
    controller.setPaused(this.scrollPaused, 'scroll');

    const character = CHARACTERS[characterId];
    this.ringMaterial?.color.set(character.color);
    this.ringMaterialSoft?.color.set(character.color);
    this.rim.color.set(character.color);
    this.shadowHalo.material.opacity = 0.8;
    this.emit('characterchange', { characterId, character, controller });

    if (reset) {
      controller.setTextActive(false);
      controller.setContext({
        panelOpen: false,
        recommendationActive: false,
        positiveProgressActive: false,
        trailCompleteActive: false,
      });
      controller.play(IDLE[characterId], {
        force: true,
        clearQueue: true,
        source: 'showCharacter',
      });
    } else if (!controller.currentSpec) {
      controller.play(IDLE[characterId], { force: true, clearQueue: true, source: 'showCharacter' });
    }
    this.applyActivity();
    return controller;
  }

  get activeController() {
    return this.activeId ? this.characters.get(this.activeId)?.controller ?? null : null;
  }

  getController(characterId) {
    return this.characters.get(characterId)?.controller ?? null;
  }

  async playAnimation(animationId) {
    const spec = getAnimation(animationId);
    if (!spec) return { ok: false, reason: `Animação desconhecida: ${animationId}` };
    if (this.activeId !== spec.character) {
      await this.showCharacter(spec.character, { reset: false });
    }
    const controller = this.activeController;
    controller.setTextActive(false);
    return controller.playAnimation(animationId);
  }

  async triggerAnimation(animationId, priority) {
    const spec = getAnimation(animationId);
    if (!spec) return { ok: false, reason: `Animação desconhecida: ${animationId}` };
    if (this.activeId !== spec.character) {
      await this.showCharacter(spec.character, { reset: false });
    }
    return this.activeController.triggerAnimation(animationId, priority);
  }

  setReducedMotion(enabled) {
    this.reducedMotion = Boolean(enabled);
    for (const { controller } of this.characters.values()) {
      controller.setReducedMotion(this.reducedMotion, { silent: true });
    }
    this.emit('motionmode', { reducedMotion: this.reducedMotion });
    return this.reducedMotion;
  }

  stopAnimation() {
    this.activeController?.stopAnimation();
  }

  resetCamera() {
    const aspect = this.getAspect();
    const distance = aspect < 0.95 ? 7.15 : 6.15;
    this.camera.position.set(0.95, 1.82, distance);
    this.controls.target.copy(this.cameraTarget);
    this.controls.update();
    this.emit('camerareset', {});
  }

  getAspect() {
    const rect = this.container.getBoundingClientRect();
    return rect.width / Math.max(1, rect.height);
  }

  resize() {
    if (this.disposed) return;
    const width = this.container.clientWidth;
    const shouldShadows = this.shadowsRequested && window.innerWidth > 760;
    if (shouldShadows !== this.shadowsEnabled) {
      this.shadowsEnabled = shouldShadows;
      this.renderer.shadowMap.enabled = shouldShadows;
      if (this.key) this.key.castShadow = shouldShadows;
      this.emit('qualitychange', { shadows: shouldShadows });
    }
    const height = this.container.clientHeight;
    if (width === 0 || height === 0) return;
    this.renderer.setSize(width, height, false);
    const aspect = width / height;
    this.camera.aspect = aspect;
    this.camera.updateProjectionMatrix();
    if (this.lastAspect && Math.abs(this.lastAspect - aspect) > 0.2) {
      this.resetCamera();
    }
    this.lastAspect = aspect;
    this.emit('resize', { width, height });
  }

  handleDocumentVisibility = () => {
    this.documentVisible = !document.hidden;
    this.applyActivity();
    this.emit('stagevisibility', { visible: this.stageVisible && this.documentVisible });
  };

  handleScroll = () => {
    this.scrollPaused = true;
    this.applyActivity();
    clearTimeout(this.scrollTimer);
    this.scrollTimer = setTimeout(() => {
      this.scrollPaused = false;
      this.applyActivity();
    }, 160);
  };

  applyActivity() {
    const controller = this.activeController;
    if (!controller) return;
    controller.setVisible(this.stageVisible && this.documentVisible);
    controller.setPaused(this.scrollPaused, 'scroll');
  }

  isVisuallyActive() {
    return Boolean(this.activeId && this.stageVisible && this.documentVisible && !this.scrollPaused);
  }

  animate(now = performance.now()) {
    if (this.disposed) return;
    this.raf = requestAnimationFrame(this.animate);
    const dt = this.clock.getDelta();
    this.controls.update();
    const controller = this.activeController;
    if (controller) controller.update(dt);
    this.renderer.render(this.scene, this.camera);
  }

  destroy() {
    this.disposed = true;
    cancelAnimationFrame(this.raf);
    this.resizeObserver?.disconnect();
    this.visibilityObserver?.disconnect();
    document.removeEventListener('visibilitychange', this.handleDocumentVisibility);
    window.removeEventListener('scroll', this.handleScroll);
    window.removeEventListener('resize', this.resize);
    this.controls.dispose();
    for (const { controller } of this.characters.values()) controller.dispose();
    this.renderer.dispose();
    this.environment?.dispose?.();
    this.renderer.domElement.remove();
    this.listeners.clear();
  }
}
