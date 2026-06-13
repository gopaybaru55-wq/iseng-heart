import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js";

// =====================
// BASIC SETUP
// =====================
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.z = 18;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// =====================
// PARTICLES
// =====================
const COUNT = 1500;

const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(COUNT * 3);

geometry.setAttribute(
  "position",
  new THREE.BufferAttribute(positions, 3)
);

const material = new THREE.PointsMaterial({
  color: 0x4cc3ff,
  size: 0.08
});

const points = new THREE.Points(geometry, material);
scene.add(points);

// =====================
// SHAPES
// =====================
function sphere() {
  for (let i = 0; i < COUNT; i++) {
    const i3 = i * 3;
    const r = 5;

    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);

    positions[i3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i3 + 2] = r * Math.cos(phi);
  }
}

function heart() {
  for (let i = 0; i < COUNT; i++) {
    const i3 = i * 3;
    const t = Math.random() * Math.PI * 2;

    positions[i3] = 16 * Math.pow(Math.sin(t), 3);
    positions[i3 + 1] =
      13 * Math.cos(t) -
      5 * Math.cos(2 * t) -
      2 * Math.cos(3 * t) -
      Math.cos(4 * t);

    positions[i3 + 2] = (Math.random() - 0.5) * 2;
  }
}

function text() {
  for (let i = 0; i < COUNT; i++) {
    const i3 = i * 3;
    positions[i3] = (Math.random() - 0.5) * 12;
    positions[i3 + 1] = Math.sin(i * 0.05) * 2;
    positions[i3 + 2] = 0;
  }
}

function saturn() {
  for (let i = 0; i < COUNT; i++) {
    const i3 = i * 3;

    const angle = Math.random() * Math.PI * 2;
    const radius = i % 2 === 0 ? 3 : 6;

    positions[i3] = Math.cos(angle) * radius;
    positions[i3 + 1] = (Math.random() - 0.5) * 0.3;
    positions[i3 + 2] = Math.sin(angle) * radius;
  }
}

// default
sphere();

// =====================
// KEYBOARD CONTROL
// =====================
window.addEventListener("keydown", (e) => {
  switch (e.key) {
    case "1":
    case "F1":
      sphere();
      break;

    case "2":
    case "F2":
      saturn();
      break;

    case "3":
    case "F3":
      text();
      break;

    case "4":
    case "F4":
      heart();
      break;
  }
});

// =====================
// ANIMATION LOOP
// =====================
function animate() {
  requestAnimationFrame(animate);

  points.rotation.y += 0.002;

  geometry.attributes.position.needsUpdate = true;

  renderer.render(scene, camera);
}

animate();

// =====================
// RESIZE
// =====================
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
