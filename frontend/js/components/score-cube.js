/**
 * StudyBuddy - 3D Score Cube
 * Quiz performance and accuracy visualizer
 */

export class ScoreCube {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    this.targetScale = 1.0;

    this.init();
    this.group.position.set(-4.2, 2.2, -1.0);
    this.scene.add(this.group);
  }

  init() {
    // 1. Core Glassy Cube
    const cubeGeo = new THREE.BoxGeometry(0.8, 0.8, 0.8);
    this.cubeMat = new THREE.MeshPhongMaterial({
      color: 0x6bcf7f,
      emissive: 0x38b000,
      emissiveIntensity: 0.5,
      shininess: 90,
      transparent: true,
      opacity: 0.85,
    });
    this.cubeMesh = new THREE.Mesh(cubeGeo, this.cubeMat);
    this.group.add(this.cubeMesh);

    // 2. Outer Wireframe Outline
    const wireGeo = new THREE.BoxGeometry(0.92, 0.92, 0.92);
    this.wireMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      wireframe: true,
      transparent: true,
      opacity: 0.35,
    });
    this.wireMesh = new THREE.Mesh(wireGeo, this.wireMat);
    this.group.add(this.wireMesh);
  }

  updateScore(score, total) {
    const accuracy = total > 0 ? (score / total) : 1;

    let targetColor = 0x6bcf7f; // High
    let emissiveColor = 0x38b000;

    if (accuracy < 0.5) {
      targetColor = 0xff5252; // Low
      emissiveColor = 0xd90429;
    } else if (accuracy < 0.8) {
      targetColor = 0xffd93d; // Medium
      emissiveColor = 0xf48c06;
    }

    this.cubeMat.color.setHex(targetColor);
    this.cubeMat.emissive.setHex(emissiveColor);

    // Trigger scale bounce
    this.cubeMesh.scale.set(1.4, 1.4, 1.4);
  }

  update(delta) {
    this.cubeMesh.rotation.x += delta * 0.8;
    this.cubeMesh.rotation.y += delta * 1.2;
    this.wireMesh.rotation.x -= delta * 0.4;
    this.wireMesh.rotation.y -= delta * 0.6;

    // Decay scale back to 1.0
    this.cubeMesh.scale.lerp(new THREE.Vector3(1, 1, 1), 6 * delta);
  }
}
