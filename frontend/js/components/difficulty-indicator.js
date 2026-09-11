/**
 * StudyBuddy - 3D Difficulty Indicator Component
 * Visual level badge in 3D space
 */

export class DifficultyIndicator {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();

    this.init();
    this.group.position.set(0, -3.8, 0);
    this.scene.add(this.group);
  }

  init() {
    const ringGeo = new THREE.RingGeometry(0.6, 0.65, 32);
    this.ringMat = new THREE.MeshBasicMaterial({
      color: 0x667eea,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.6,
    });
    this.ring = new THREE.Mesh(ringGeo, this.ringMat);
    this.ring.rotation.x = Math.PI / 2;
    this.group.add(this.ring);
  }

  setTier(tierName) {
    let color = 0x667eea;
    if (tierName === 'Beginner') color = 0x4ecdc4;
    if (tierName === 'Intermediate') color = 0x667eea;
    if (tierName === 'Advanced') color = 0x764ba2;
    if (tierName === 'Exam-Focused') color = 0xff6b9d;

    this.ringMat.color.setHex(color);
  }

  update(delta) {
    this.ring.rotation.z += delta * 0.5;
  }
}
