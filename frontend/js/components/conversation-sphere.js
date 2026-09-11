/**
 * StudyBuddy - 3D Central Conversation Sphere
 * Intelligent Knowledge Engine Visualization
 */

export class ConversationSphere {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    this.state = 'IDLE'; // IDLE, THINKING, RESPONDING, SUCCESS, ERROR, QUIZ_EVALUATION
    this.time = 0;

    this.init();
    this.scene.add(this.group);
  }

  init() {
    // 1. Core Sphere (Internal glowing energy)
    const coreGeo = new THREE.SphereGeometry(1.4, 32, 32);
    this.coreMat = new THREE.MeshPhongMaterial({
      color: 0x667eea,
      emissive: 0x3b4992,
      emissiveIntensity: 0.6,
      shininess: 90,
      transparent: true,
      opacity: 0.88,
    });
    this.coreMesh = new THREE.Mesh(coreGeo, this.coreMat);
    this.group.add(this.coreMesh);

    // 2. Outer Geodesic / Wireframe Lattice
    const wireGeo = new THREE.IcosahedronGeometry(1.85, 2);
    this.wireMat = new THREE.MeshBasicMaterial({
      color: 0x4ecdc4,
      wireframe: true,
      transparent: true,
      opacity: 0.35,
    });
    this.wireMesh = new THREE.Mesh(wireGeo, this.wireMat);
    this.group.add(this.wireMesh);

    // 3. Ambient Particle Halo
    const particleCount = 200;
    const pGeo = new THREE.BufferGeometry();
    const pPos = new Float32Array(particleCount * 3);
    const pColors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);
      const r = 2.0 + Math.random() * 0.8;

      pPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pPos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pPos[i * 3 + 2] = r * Math.cos(phi);

      pColors[i * 3] = 0.4 + Math.random() * 0.2;
      pColors[i * 3 + 1] = 0.6 + Math.random() * 0.4;
      pColors[i * 3 + 2] = 0.9 + Math.random() * 0.1;
    }

    pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
    pGeo.setAttribute('color', new THREE.BufferAttribute(pColors, 3));

    const pMat = new THREE.PointsMaterial({
      size: 0.06,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
      blending: THREE.AdditiveBlending,
    });

    this.particles = new THREE.Points(pGeo, pMat);
    this.group.add(this.particles);

    // 4. Point Light emanating from core
    this.light = new THREE.PointLight(0x667eea, 2.5, 12);
    this.group.add(this.light);
  }

  setState(newState) {
    this.state = newState;

    if (newState === 'THINKING') {
      this.coreMat.color.setHex(0x4ecdc4);
      this.coreMat.emissive.setHex(0x2a9d8f);
      this.wireMat.color.setHex(0x667eea);
      this.light.color.setHex(0x4ecdc4);
    } else if (newState === 'SUCCESS') {
      this.coreMat.color.setHex(0x6bcf7f);
      this.coreMat.emissive.setHex(0x38b000);
      this.wireMat.color.setHex(0x6bcf7f);
      this.light.color.setHex(0x6bcf7f);
    } else if (newState === 'ERROR') {
      this.coreMat.color.setHex(0xff5252);
      this.coreMat.emissive.setHex(0xd90429);
      this.wireMat.color.setHex(0xff5252);
      this.light.color.setHex(0xff5252);
    } else if (newState === 'QUIZ_EVALUATION') {
      this.coreMat.color.setHex(0xffd93d);
      this.coreMat.emissive.setHex(0xf48c06);
      this.wireMat.color.setHex(0xffd93d);
      this.light.color.setHex(0xffd93d);
    } else {
      // IDLE / NORMAL
      this.coreMat.color.setHex(0x667eea);
      this.coreMat.emissive.setHex(0x3b4992);
      this.wireMat.color.setHex(0x4ecdc4);
      this.light.color.setHex(0x667eea);
    }
  }

  update(delta) {
    this.time += delta;

    const rotSpeed = this.state === 'THINKING' ? 1.8 : 0.4;

    this.coreMesh.rotation.y += delta * rotSpeed * 0.5;
    this.wireMesh.rotation.x += delta * rotSpeed * 0.3;
    this.wireMesh.rotation.y += delta * rotSpeed * 0.6;
    this.particles.rotation.y -= delta * rotSpeed * 0.2;

    // Gentle Breathing Scale
    const breathe = Math.sin(this.time * (this.state === 'THINKING' ? 6 : 2)) * 0.05 + 1;
    this.coreMesh.scale.set(breathe, breathe, breathe);
  }
}
