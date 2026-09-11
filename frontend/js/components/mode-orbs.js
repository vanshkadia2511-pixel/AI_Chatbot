/**
 * StudyBuddy - 3D Mode Orbs Component
 * Interactive mode satellites orbiting the knowledge engine
 */

export class ModeOrbs {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    this.orbs = [];
    this.orbitRadius = 3.6;
    this.orbitSpeed = 0.25;
    this.time = 0;

    this.modes = [
      { name: 'Study Mode', icon: '📚', color: 0x667eea, angleOffset: 0 },
      { name: 'Explain Mode', icon: '💡', color: 0x4ecdc4, angleOffset: Math.PI * 0.5 },
      { name: 'Quiz Mode', icon: '🧩', color: 0xffd93d, angleOffset: Math.PI },
      { name: 'Exam Mode', icon: '📝', color: 0xff6b9d, angleOffset: Math.PI * 1.5 },
    ];

    this.init();
    this.scene.add(this.group);
  }

  init() {
    this.modes.forEach((m, idx) => {
      const orbGroup = new THREE.Group();

      // Sphere Mesh
      const geo = new THREE.SphereGeometry(0.35, 24, 24);
      const mat = new THREE.MeshPhongMaterial({
        color: m.color,
        emissive: m.color,
        emissiveIntensity: 0.5,
        shininess: 80,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.userData = { isModeOrb: true, modeName: m.name, index: idx };
      orbGroup.add(mesh);

      // Outer Glow Ring
      const ringGeo = new THREE.RingGeometry(0.42, 0.48, 24);
      const ringMat = new THREE.MeshBasicMaterial({
        color: m.color,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.6,
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.rotation.x = Math.PI / 2;
      orbGroup.add(ringMesh);

      this.group.add(orbGroup);

      this.orbs.push({
        group: orbGroup,
        mesh: mesh,
        ring: ringMesh,
        modeName: m.name,
        angleOffset: m.angleOffset,
        baseColor: m.color,
      });
    });
  }

  setActiveMode(activeModeName) {
    this.orbs.forEach(orb => {
      const isActive = orb.modeName === activeModeName;
      orb.mesh.scale.setScalar(isActive ? 1.4 : 1.0);
      orb.mesh.material.emissiveIntensity = isActive ? 1.0 : 0.4;
      orb.ring.material.opacity = isActive ? 0.9 : 0.4;
      orb.ring.scale.setScalar(isActive ? 1.3 : 1.0);
    });
  }

  update(delta) {
    this.time += delta * this.orbitSpeed;

    this.orbs.forEach(orb => {
      const angle = this.time + orb.angleOffset;
      const x = Math.cos(angle) * this.orbitRadius;
      const z = Math.sin(angle) * this.orbitRadius;
      const y = Math.sin(angle * 2) * 0.4;

      orb.group.position.set(x, y, z);
      orb.mesh.rotation.y += delta * 1.5;
      orb.ring.rotation.z += delta * 1.0;
    });
  }
}
