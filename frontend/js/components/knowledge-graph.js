/**
 * StudyBuddy - 3D Knowledge Graph Component
 * Interactive network of academic topics & prerequisite relationships
 */

export class KnowledgeGraph {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    this.nodes = [];
    this.edges = [];
    this.activeTopic = 'Linear Regression';

    this.topicsData = [
      { id: 'math_found', name: 'Calculus', pos: [-3.2, 0.8, -2.5], color: 0x4ecdc4 },
      { id: 'lin_reg', name: 'Linear Regression', pos: [-2.0, -0.6, -1.8], color: 0x667eea },
      { id: 'stats', name: 'Statistics', pos: [-3.5, -1.8, -2.0], color: 0xff6b9d },
      { id: 'prob', name: 'Probability', pos: [-1.2, 1.4, -2.2], color: 0xffd93d },
      { id: 'ml', name: 'Machine Learning', pos: [-0.5, -1.5, -2.8], color: 0x6bcf7f },
    ];

    this.connections = [
      ['math_found', 'lin_reg'],
      ['stats', 'lin_reg'],
      ['prob', 'stats'],
      ['lin_reg', 'ml'],
    ];

    this.init();
    this.scene.add(this.group);
  }

  init() {
    // 1. Build Nodes
    this.topicsData.forEach(t => {
      const geo = new THREE.SphereGeometry(0.24, 20, 20);
      const mat = new THREE.MeshPhongMaterial({
        color: t.color,
        emissive: t.color,
        emissiveIntensity: 0.4,
        shininess: 90,
      });

      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(...t.pos);
      mesh.userData = { isKnowledgeNode: true, topicName: t.name, id: t.id };

      this.group.add(mesh);
      this.nodes.push({ data: t, mesh: mesh, mat: mat });
    });

    // 2. Build Connection Lines
    this.connections.forEach(([sourceId, targetId]) => {
      const source = this.topicsData.find(t => t.id === sourceId);
      const target = this.topicsData.find(t => t.id === targetId);

      if (source && target) {
        const points = [
          new THREE.Vector3(...source.pos),
          new THREE.Vector3(...target.pos),
        ];
        const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
        const lineMat = new THREE.LineBasicMaterial({
          color: 0x667eea,
          transparent: true,
          opacity: 0.35,
        });
        const line = new THREE.Line(lineGeo, lineMat);
        this.group.add(line);
        this.edges.push({ line, lineMat, sourceId, targetId });
      }
    });

    this.highlightTopic(this.activeTopic);
  }

  highlightTopic(topicName) {
    this.activeTopic = topicName;

    this.nodes.forEach(n => {
      const isCurrent = n.data.name.toLowerCase() === topicName.toLowerCase();
      n.mesh.scale.setScalar(isCurrent ? 1.6 : 1.0);
      n.mat.emissiveIntensity = isCurrent ? 1.0 : 0.4;
    });

    this.edges.forEach(e => {
      const sourceNode = this.topicsData.find(t => t.id === e.sourceId);
      const targetNode = this.topicsData.find(t => t.id === e.targetId);

      const isConnected =
        (sourceNode && sourceNode.name.toLowerCase() === topicName.toLowerCase()) ||
        (targetNode && targetNode.name.toLowerCase() === topicName.toLowerCase());

      e.lineMat.opacity = isConnected ? 0.85 : 0.2;
      e.lineMat.color.setHex(isConnected ? 0xffd93d : 0x667eea);
    });
  }

  update(delta) {
    // Gentle floating motion for nodes
    const time = Date.now() * 0.001;
    this.nodes.forEach((n, idx) => {
      n.mesh.position.y = n.data.pos[1] + Math.sin(time + idx * 1.5) * 0.08;
    });
  }
}
