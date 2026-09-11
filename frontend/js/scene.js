/**
 * StudyBuddy - 3D Master Scene Orchestrator
 * High Performance WebGL Three.js Renderer
 */

import { appState, actions, events } from './state.js';
import { ConversationSphere } from './components/conversation-sphere.js';
import { ModeOrbs } from './components/mode-orbs.js';
import { DifficultyWheel } from './components/difficulty-wheel.js';
import { ScoreCube } from './components/score-cube.js';
import { KnowledgeGraph } from './components/knowledge-graph.js';
import { ProgressHelix } from './components/progress-helix.js';
import { DifficultyIndicator } from './components/difficulty-indicator.js';

export class SceneManager {
  constructor(canvasElement) {
    this.canvas = canvasElement;
    this.width = window.innerWidth;
    this.height = window.innerHeight;

    this.clock = new THREE.Clock();
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();

    this.initScene();
    this.initComponents();
    this.bindEvents();
    this.animate();
  }

  initScene() {
    // 1. Scene
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x0a0a14, 0.035);

    // 2. Camera
    this.camera = new THREE.PerspectiveCamera(
      45,
      this.width / this.height,
      0.1,
      100
    );
    this.camera.position.set(0, 0, 9.5);

    // 3. Renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: appState.qualityTier !== 'LOW',
      alpha: true,
      powerPreference: 'high-performance',
    });
    this.renderer.setSize(this.width, this.height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 4. Lighting
    this.ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(this.ambientLight);

    this.dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    this.dirLight.position.set(5, 8, 5);
    this.scene.add(this.dirLight);

    // 5. Starfield / Floating Knowledge Dust
    this.initStarfield();
  }

  initStarfield() {
    const starCount = appState.qualityTier === 'HIGH' ? 400 : 150;
    const starGeo = new THREE.BufferGeometry();
    const starPos = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount * 3; i += 3) {
      starPos[i] = (Math.random() - 0.5) * 30;
      starPos[i + 1] = (Math.random() - 0.5) * 20;
      starPos[i + 2] = (Math.random() - 0.5) * 20 - 5;
    }

    starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
    const starMat = new THREE.PointsMaterial({
      color: 0x667eea,
      size: 0.05,
      transparent: true,
      opacity: 0.5,
    });
    this.starfield = new THREE.Points(starGeo, starMat);
    this.scene.add(this.starfield);
  }

  initComponents() {
    this.sphere = new ConversationSphere(this.scene);
    this.modeOrbs = new ModeOrbs(this.scene);
    this.difficultyWheel = new DifficultyWheel(this.scene);
    this.scoreCube = new ScoreCube(this.scene);
    this.knowledgeGraph = new KnowledgeGraph(this.scene);
    this.progressHelix = new ProgressHelix(this.scene);
    this.diffIndicator = new DifficultyIndicator(this.scene);

    // Set initial active states
    this.modeOrbs.setActiveMode(appState.mode);
    this.difficultyWheel.setDifficulty(appState.difficulty);
    this.diffIndicator.setTier(appState.difficulty);
  }

  bindEvents() {
    window.addEventListener('resize', () => this.onResize());

    // Mouse Move for Parallax and Raycasting
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      // Gentle Camera Parallax
      this.camera.position.x += (this.mouse.x * 0.4 - this.camera.position.x) * 0.05;
      this.camera.position.y += (-this.mouse.y * 0.3 - this.camera.position.y) * 0.05;
      this.camera.lookAt(0, 0, 0);
    });

    // Raycast Clicks on 3D objects
    window.addEventListener('click', (e) => {
      // Ignore if clicking on UI panels
      if (e.target.closest('.left-panel, .right-panel, .app-header, .hud-top-center, .mobile-nav-bar')) {
        return;
      }

      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.scene.children, true);

      if (intersects.length > 0) {
        const obj = intersects[0].object;
        if (obj.userData?.isModeOrb) {
          actions.setMode(obj.userData.modeName);
        } else if (obj.userData?.isKnowledgeNode) {
          actions.setTopic(obj.userData.topicName);
        } else if (obj.userData?.isDiffBead) {
          actions.setDifficulty(obj.userData.tierName);
        }
      }
    });

    // Listen to App State Events
    events.on('modeChanged', ({ to }) => {
      this.modeOrbs.setActiveMode(to);
    });

    events.on('difficultyChanged', ({ to }) => {
      this.difficultyWheel.setDifficulty(to);
      this.diffIndicator.setTier(to);
    });

    events.on('topicSelected', (topic) => {
      this.knowledgeGraph.highlightTopic(topic);
    });

    events.on('aiStateChange', (state) => {
      this.sphere.setState(state);
    });

    events.on('quizEvaluated', ({ isCorrect, score, total, progress }) => {
      this.scoreCube.updateScore(score, total);
      this.progressHelix.updateProgress(progress);
      this.sphere.setState(isCorrect ? 'SUCCESS' : 'ERROR');
      setTimeout(() => this.sphere.setState('IDLE'), 1800);
    });
  }

  onResize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.camera.aspect = this.width / this.height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.width, this.height);
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    const delta = this.clock.getDelta();

    if (this.sphere) this.sphere.update(delta);
    if (this.modeOrbs) this.modeOrbs.update(delta);
    if (this.difficultyWheel) this.difficultyWheel.update(delta);
    if (this.scoreCube) this.scoreCube.update(delta);
    if (this.knowledgeGraph) this.knowledgeGraph.update(delta);
    if (this.progressHelix) this.progressHelix.update(delta);
    if (this.diffIndicator) this.diffIndicator.update(delta);

    if (this.starfield) {
      this.starfield.rotation.y += delta * 0.02;
    }

    this.renderer.render(this.scene, this.camera);
  }
}
