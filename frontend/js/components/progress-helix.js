/**
 * StudyBuddy - 3D Progress Helix
 * Spiraling learning journey from Start (0%) to Mastery (100%)
 */

export class ProgressHelix {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    this.progress = 0.78; // 78% default

    this.init();
    this.group.position.set(4.2, 0, -2.0);
    this.scene.add(this.group);
  }

  init() {
    // 1. Generate 3D Spiral Points
    const helixPoints = [];
    const height = 4.5;
    const turns = 2.5;
    const radius = 0.6;
    const count = 120;

    for (let i = 0; i <= count; i++) {
      const t = i / count;
      const angle = t * Math.PI * 2 * turns;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = (t - 0.5) * height;
      helixPoints.push(new THREE.Vector3(x, y, z));
    }

    this.helixCurve = new THREE.CatmullRomCurve3(helixPoints);

    // Helix Backbone Tube
    const tubeGeo = new THREE.TubeGeometry(this.helixCurve, 64, 0.03, 8, false);
    const tubeMat = new THREE.MeshBasicMaterial({
      color: 0x667eea,
      transparent: true,
      opacity: 0.4,
    });
    this.tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    this.group.add(this.tubeMesh);

    // 2. Progress Indicator Beacon Orb
    const beaconGeo = new THREE.SphereGeometry(0.18, 16, 16);
    this.beaconMat = new THREE.MeshPhongMaterial({
      color: 0xffd93d,
      emissive: 0xf48c06,
      emissiveIntensity: 0.8,
    });
    this.beaconMesh = new THREE.Mesh(beaconGeo, this.beaconMat);
    this.group.add(this.beaconMesh);

    this.updateProgress(this.progress * 100);
  }

  updateProgress(percent) {
    this.progress = Math.max(0, Math.min(100, percent)) / 100;
    const pt = this.helixCurve.getPointAt(this.progress);
    this.beaconMesh.position.copy(pt);
  }

  update(delta) {
    this.group.rotation.y += delta * 0.4;
  }
}
