/**
 * StudyBuddy - 3D Difficulty Wheel
 * Segmented ring visualizing the 4 learning difficulty tiers
 */

export class DifficultyWheel {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    this.segments = [];
    this.currentDifficulty = 'Intermediate';
    this.targetRotationY = 0;

    this.tiers = [
      { name: 'Beginner', color: 0x4ecdc4, angle: 0 },
      { name: 'Intermediate', color: 0x667eea, angle: Math.PI * 0.5 },
      { name: 'Advanced', color: 0x764ba2, angle: Math.PI },
      { name: 'Exam-Focused', color: 0xff6b9d, angle: Math.PI * 1.5 },
    ];

    this.init();
    this.group.position.set(0, -2.8, 0);
    this.scene.add(this.group);
  }

  init() {
    const radius = 2.8;
    const tubeRadius = 0.08;

    this.tiers.forEach((tier, i) => {
      const arcLength = (Math.PI * 2) / 4 - 0.15;
      const startAngle = i * (Math.PI / 2) + 0.075;

      // Arc geometry for segmented ring
      const curve = new THREE.EllipseCurve(
        0, 0,
        radius, radius,
        startAngle, startAngle + arcLength,
        false, 0
      );

      const points = curve.getPoints(32);
      const geo = new THREE.BufferGeometry().setFromPoints(points);
      const mat = new THREE.LineBasicMaterial({
        color: tier.color,
        linewidth: 3,
        transparent: true,
        opacity: 0.7,
      });

      const line = new THREE.Line(geo, mat);
      line.rotation.x = Math.PI / 2;
      this.group.add(line);

      // Add a bead/marker at segment center
      const midAngle = startAngle + arcLength / 2;
      const beadGeo = new THREE.SphereGeometry(0.16, 16, 16);
      const beadMat = new THREE.MeshPhongMaterial({
        color: tier.color,
        emissive: tier.color,
        emissiveIntensity: 0.5,
      });
      const bead = new THREE.Mesh(beadGeo, beadMat);
      bead.position.set(
        Math.cos(midAngle) * radius,
        0,
        Math.sin(midAngle) * radius
      );
      bead.userData = { isDiffBead: true, tierName: tier.name };
      this.group.add(bead);

      this.segments.push({
        name: tier.name,
        line: line,
        bead: bead,
        mat: mat,
        beadMat: beadMat,
        angle: tier.angle,
        baseColor: tier.color,
      });
    });
  }

  setDifficulty(tierName) {
    this.currentDifficulty = tierName;
    const selected = this.segments.find(s => s.name === tierName);
    if (selected) {
      this.targetRotationY = -selected.angle;
    }

    this.segments.forEach(s => {
      const isActive = s.name === tierName;
      s.mat.opacity = isActive ? 1.0 : 0.4;
      s.beadMat.emissiveIntensity = isActive ? 1.0 : 0.3;
      s.bead.scale.setScalar(isActive ? 1.5 : 1.0);
    });
  }

  update(delta) {
    // Smooth interpolation towards target rotation
    this.group.rotation.y += (this.targetRotationY - this.group.rotation.y) * 4 * delta;
  }
}
