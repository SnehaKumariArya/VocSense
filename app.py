import streamlit as st
import streamlit.components.v1 as components

# --- FULL-PAGE ZERO-SCROLL SETUP ---
st.set_page_config(
    page_title="VocSense",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    #MainMenu, header, footer { visibility: hidden !important; height: 0 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], .main {
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
        max-height: 100vh !important;
        background-color: #0b0f17 !important;
    }
    iframe {
        display: block;
        border: none;
        width: 100vw !important;
        height: 100vh !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

threejs_centered_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: radial-gradient(ellipse at 50% 50%, #141e2e 0%, #0c131d 55%, #05070a 100%);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    #canvas-container { width: 100vw; height: 100vh; position: absolute; inset: 0; }

    #hint {
      position: absolute;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(12, 19, 29, 0.85);
      border: 1px solid #0284c7;
      color: #f1f5f9;
      padding: 8px 24px;
      border-radius: 24px;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.4px;
      pointer-events: none;
      backdrop-filter: blur(8px);
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.7);
      z-index: 10;
    }

    #floating-tag {
      position: absolute;
      background: #0284c7;
      border: 2px solid #38bdf8;
      color: #ffffff;
      padding: 5px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.3px;
      pointer-events: none;
      white-space: nowrap;
      opacity: 0;
      transform: translate(-50%, -130%);
      transition: opacity 0.2s ease, transform 0.2s ease;
      box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5);
      z-index: 20;
    }
    #floating-tag.visible { opacity: 1; }
    #floating-tag::after {
      content: '';
      position: absolute;
      width: 8px;
      height: 8px;
      background: #0284c7;
      bottom: -4px;
      left: 50%;
      transform: translateX(-50%) rotate(45deg);
    }

    #detail-card {
      position: absolute;
      bottom: 24px;
      right: 24px;
      width: 310px;
      background: rgba(12, 19, 29, 0.92);
      border: 1.5px solid #0284c7;
      border-radius: 12px;
      padding: 16px 18px;
      color: #f8fafc;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(12px);
      opacity: 0;
      transform: translateY(12px);
      transition: all 0.25s ease-out;
      pointer-events: none;
      z-index: 20;
    }
    #detail-card.active {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
    #card-title { font-size: 15px; font-weight: 700; color: #38bdf8; margin-bottom: 2px; }
    #card-role { font-size: 11px; font-weight: 700; color: #10b981; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    #card-desc { font-size: 12px; color: #cbd5e1; line-height: 1.45; margin-bottom: 8px; }
    #card-spec { font-size: 11px; color: #94a3b8; border-top: 1px solid #1e293b; padding-top: 6px; font-family: monospace; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="hint">👆 Click any component to inspect (USB-C Port, Power, Speaker, Pod, EMG, Strain, LiPo)</div>
  <div id="floating-tag">Component</div>

  <div id="detail-card">
    <div id="card-title">Component Name</div>
    <div id="card-role">Subsystem</div>
    <div id="card-desc">Description of function and anatomy.</div>
    <div id="card-spec">SPEC: --</div>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(32, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 6, 26);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 0, 0);

    // Studio Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.95));
    const mainLight = new THREE.DirectionalLight(0xffffff, 1.4);
    mainLight.position.set(12, 24, 16);
    scene.add(mainLight);

    const edgeLight = new THREE.DirectionalLight(0x38bdf8, 1.2);
    edgeLight.position.set(-16, -10, -10);
    scene.add(edgeLight);

    // Materials
    const strapMat = new THREE.MeshStandardMaterial({ color: 0x181e26, roughness: 0.6, metalness: 0.15, side: THREE.DoubleSide });
    const metalMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.95, roughness: 0.18 });
    const podMat = new THREE.MeshStandardMaterial({ color: 0x10151d, roughness: 0.35, metalness: 0.25 });
    const strainMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.3, metalness: 0.45 });
    const lipoMat = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.85, roughness: 0.25 });
    const buttonMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.3, metalness: 0.3 });
    const darkVoidMat = new THREE.MeshBasicMaterial({ color: 0x05070a });
    const portRimMat = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.9, roughness: 0.2 });

    const interactiveObjects = [];

    // 1. Neckband Chassis
    const strapGeom = new THREE.CylinderGeometry(10, 10, 2.3, 80, 1, true);
    strapGeom.scale(1, 1, 0.78);
    scene.add(new THREE.Mesh(strapGeom, strapMat));

    // 2. Transduction Nodes (EMG + Strain Sensors)
    const electrodeGeom = new THREE.BoxGeometry(0.35, 1.5, 1.8);
    const strainGeom = new THREE.BoxGeometry(0.2, 1.2, 3.2);

    const hardwareData = [
      {
        x: -6.8, z: 4.8, rot: 0.9, geom: electrodeGeom, mat: metalMat,
        shortName: "📍 EMG Sensor: Anterior Digastric",
        title: "sEMG Sensor (Anterior Digastric)",
        role: "Primary Myoelectric Transduction",
        desc: "Dry sintered Ag/AgCl contact acquiring submental microvolt potentials during tongue depression and vocal shaping.",
        spec: "Dry Contact | Imp: <8.2 kΩ | Bandwidth: 20-450 Hz"
      },
      {
        x: 6.8, z: 4.8, rot: -0.9, geom: electrodeGeom, mat: metalMat,
        shortName: "📍 EMG Sensor: Thyrohyoid Node",
        title: "sEMG Sensor (Thyrohyoid)",
        role: "Laryngeal Elevation Tracking",
        desc: "Captures thyroid displacement and pitch intent corresponding to vowel modulation with low contact resistance.",
        spec: "Dry Contact | Imp: <7.4 kΩ | CMRR: >100 dB"
      },
      {
        x: -8.8, z: 0.0, rot: 0.0, geom: strainGeom, mat: strainMat,
        shortName: "📍 Strain Sensor: Left Neck Kinematics",
        title: "Piezoresistive Strain Sensor (Left)",
        role: "Biomechanical Motion Detection",
        desc: "Flexible conductive gauge sensing physical throat perimeter expansion, isolating speech from jaw flex.",
        spec: "Gauge Factor: >25 | Latency: <8 ms"
      },
      {
        x: 8.8, z: 0.0, rot: 0.0, geom: strainGeom, mat: strainMat,
        shortName: "📍 Strain Sensor: Right Neck Kinematics",
        title: "Piezoresistive Strain Sensor (Right)",
        role: "Biomechanical Motion Detection",
        desc: "Symmetric strain gauge measuring dynamic neck skin stretching to cancel gross motion artifacts.",
        spec: "Gauge Factor: >25 | Latency: <8 ms"
      }
    ];

    hardwareData.forEach(data => {
      const mesh = new THREE.Mesh(data.geom, data.mat.clone());
      mesh.position.set(data.x, 0, data.z);
      mesh.rotation.y = data.rot;
      mesh.userData = data;
      scene.add(mesh);
      interactiveObjects.push(mesh);
    });

    // 3. Central Front Processing Pod
    const podGroup = new THREE.Group();
    const podMesh = new THREE.Mesh(new THREE.BoxGeometry(7.6, 2.6, 1.4), podMat.clone());
    podMesh.userData = {
      shortName: "⚡ ESP32 MCU + 6-DOF IMU Pod",
      title: "ESP32 SoC + 6-DOF IMU Pod",
      role: "Edge Processing & Motion Cancellation",
      desc: "Dual-core 240MHz MCU executing INT8 quantized neural inference (<15ms). Integrated MPU-6050 cancels dynamic motion baseline drift.",
      spec: "Xtensa 32-bit | TFLite Micro INT8 | 6-DOF Fusion"
    };
    podGroup.add(podMesh);
    interactiveObjects.push(podMesh);

    // Front Status LEDs
    const ledGreen = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.2, 16), new THREE.MeshBasicMaterial({ color: 0x22c55e }));
    ledGreen.rotation.x = Math.PI / 2;
    ledGreen.position.set(-0.2, -0.2, 0.72);
    podGroup.add(ledGreen);

    const ledBlue = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.2, 16), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
    ledBlue.rotation.x = Math.PI / 2;
    ledBlue.position.set(0.5, -0.2, 0.72);
    podGroup.add(ledBlue);

    // Tactile Power Switch
    const btnGeom = new THREE.CylinderGeometry(0.42, 0.45, 0.35, 24);
    const powerBtn = new THREE.Mesh(btnGeom, buttonMat.clone());
    powerBtn.rotation.x = Math.PI / 2;
    powerBtn.position.set(-2.5, 0.0, 0.76);
    powerBtn.userData = {
      shortName: "🔘 Power Switch (ON/OFF)",
      title: "Hardware Power Toggle & Calibration Key",
      role: "System Power & Standby State",
      desc: "Soft-latch tactile power button for system boot, deep-sleep mode, and triggering the 60-second recalibration routine.",
      spec: "Latching Switch | Deep Sleep: <10 µA"
    };
    podGroup.add(powerBtn);
    interactiveObjects.push(powerBtn);

    // Micro-Speaker
    const speakerGroup = new THREE.Group();
    const speakerBase = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.2, 32), podMat.clone());
    speakerBase.rotation.x = Math.PI / 2;
    speakerBase.position.set(2.4, 0.0, 0.73);
    speakerGroup.add(speakerBase);

    const holeGeom = new THREE.CircleGeometry(0.08, 12);
    const holeOffsets = [
      [0, 0], [0.3, 0], [-0.3, 0], [0, 0.3], [0, -0.3],
      [0.22, 0.22], [-0.22, 0.22], [0.22, -0.22], [-0.22, -0.22]
    ];
    holeOffsets.forEach(([dx, dy]) => {
      const hole = new THREE.Mesh(holeGeom, darkVoidMat);
      hole.position.set(2.4 + dx, dy, 0.84);
      speakerGroup.add(hole);
    });

    speakerBase.userData = {
      shortName: "🔊 Micro-Acoustic Speaker",
      title: "Integrated Speech Synthesizer Speaker",
      role: "Real-Time Acoustic Voice Synthesis",
      desc: "Miniature electromagnetic transducer delivering instantaneous local voice playback of decoded silent speech tokens.",
      spec: "Output: 1.5W Class-D | SPL: 85 dB @ 10cm"
    };
    podGroup.add(speakerGroup);
    interactiveObjects.push(speakerBase);

    podGroup.position.set(0, 0, 7.8);
    scene.add(podGroup);

    // Flush USB-C Port
    const usbcPortGroup = new THREE.Group();
    const portBezel = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.5, 0.08), portRimMat);
    usbcPortGroup.add(portBezel);

    const portCutout = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.12, 16), darkVoidMat);
    portCutout.rotation.x = Math.PI / 2;
    portCutout.scale.set(2.2, 0.7, 1.0);
    portCutout.position.set(0, 0, 0.02);
    usbcPortGroup.add(portCutout);

    const portLed = new THREE.Mesh(new THREE.CircleGeometry(0.06, 12), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
    portLed.position.set(0.9, 0, 0.05);
    usbcPortGroup.add(portLed);

    usbcPortGroup.position.set(5.8, 0.0, 6.3);
    usbcPortGroup.rotation.y = -0.68;

    portBezel.userData = {
      shortName: "⚡ Flush USB-C Fast Charging Port",
      title: "Embedded USB Type-C Fast Charge Port",
      role: "Power Delivery & Calibration Interface",
      desc: "Chassis-integrated USB-C port supporting 5V/2A fast charging and direct USB-UART flashing for edge firmware updates.",
      spec: "Rate: 5V @ 1.5A | Full Charge: <40 mins"
    };
    interactiveObjects.push(portBezel);
    scene.add(usbcPortGroup);

    // 4. Rear Compartment: LiPo Battery Module
    const lipoMesh = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.5, 1.2), lipoMat.clone());
    lipoMesh.position.set(0, 0, -7.8);
    lipoMesh.userData = {
      shortName: "🔋 3.7V LiPo Battery Module",
      title: "500 mAh LiPo Battery Module",
      role: "Autonomous Power Delivery",
      desc: "Ultra-compact rechargeable lithium-polymer cell with TP4056 PMIC, yielding 14+ hours of uninterrupted continuous operation.",
      spec: "500 mAh | 3.7V Nominal | Current: ~38 mA"
    };
    scene.add(lipoMesh);
    interactiveObjects.push(lipoMesh);

    // Raycasting & User Clicks
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let selectedObject = null;

    const floatingTag = document.getElementById('floating-tag');
    const card = document.getElementById('detail-card');
    const cardTitle = document.getElementById('card-title');
    const cardRole = document.getElementById('card-role');
    const cardDesc = document.getElementById('card-desc');
    const cardSpec = document.getElementById('card-spec');

    window.addEventListener('pointerdown', (e) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(interactiveObjects, true);

      if (intersects.length > 0) {
        let hit = intersects[0].object;
        while (hit && !hit.userData.title && hit.parent) {
          hit = hit.parent;
        }
        const data = hit.userData;
        if (!data || !data.title) return;

        if (selectedObject && selectedObject.material && selectedObject.material.emissive) {
          selectedObject.material.emissive.setHex(0x000000);
        }

        selectedObject = hit;
        if (selectedObject.material && selectedObject.material.emissive) {
          selectedObject.material.emissive.setHex(0x0284c7);
        }

        floatingTag.innerText = data.shortName;
        floatingTag.classList.add('visible');

        cardTitle.innerText = data.title;
        cardRole.innerText = data.role;
        cardDesc.innerText = data.desc;
        cardSpec.innerText = "SPEC: " + data.spec;
        card.classList.add('active');
      }
    });

    function updateFloatingTag() {
      if (!selectedObject) return;
      const worldPos = new THREE.Vector3();
      selectedObject.getWorldPosition(worldPos);
      worldPos.y += 1.6;

      const projected = worldPos.project(camera);
      const x = (projected.x * 0.5 + 0.5) * window.innerWidth;
      const y = (-(projected.y * 0.5) + 0.5) * window.innerHeight;

      floatingTag.style.left = `${x}px`;
      floatingTag.style.top = `${y}px`;
      floatingTag.style.display = projected.z > 1 ? 'none' : 'block';
    }

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      updateFloatingTag();
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
"""

components.html(threejs_centered_html, height=750)