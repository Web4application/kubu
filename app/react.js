import React, { useEffect, useRef, useState } from 'react';
import * as BABYLON from 'babylonjs';
import 'babylonjs-loaders';

type NodeData = {
  emissiveR: number;
  emissiveG: number;
  emissiveB: number;
};

const KubuHai3DScene: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const engineRef = useRef<BABYLON.Engine>();
  const sceneRef = useRef<BABYLON.Scene>();
  const sphereRef = useRef<BABYLON.Mesh>();
  const pbrMatRef = useRef<BABYLON.PBRMaterial>();

  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!canvasRef.current) return;

    const engine = new BABYLON.Engine(canvasRef.current, true, { stencil: true });
    engineRef.current = engine;

    const scene = new BABYLON.Scene(engine);
    sceneRef.current = scene;

    // Camera setup
    const camera = new BABYLON.ArcRotateCamera('camera', Math.PI / 2, Math.PI / 3, 12, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvasRef.current, true);
    camera.lowerRadiusLimit = 6;
    camera.upperRadiusLimit = 30;
    camera.wheelDeltaPercentage = 0.01;

    // Lighting
    const hemiLight = new BABYLON.HemisphericLight('hemiLight', new BABYLON.Vector3(0, 1, 0), scene);
    hemiLight.intensity = 0.8;

    const dirLight = new BABYLON.DirectionalLight('dirLight', new BABYLON.Vector3(-1, -2, -1), scene);
    dirLight.position = new BABYLON.Vector3(25, 40, 25);
    dirLight.intensity = 1.2;
    dirLight.shadowEnabled = true;

    const shadowGen = new BABYLON.ShadowGenerator(2048, dirLight);
    shadowGen.useBlurExponentialShadowMap = true;
    shadowGen.blurKernel = 32;

    // Sphere
    const sphere = BABYLON.MeshBuilder.CreateSphere('nodeSphere', { diameter: 2.5, segments: 64 }, scene);
    sphere.position.y = 1.5;
    sphereRef.current = sphere;

    const pbrMat = new BABYLON.PBRMaterial('pbrNodeMat', scene);
    pbrMat.albedoColor = new BABYLON.Color3(0.05, 0.65, 0.85);
    pbrMat.metallic = 0.9;
    pbrMat.roughness = 0.1;
    pbrMat.emissiveColor = new BABYLON.Color3(0, 0.2, 0.3);
    pbrMatRef.current = pbrMat;

    sphere.material = pbrMat;
    shadowGen.addShadowCaster(sphere);

    // Ground
    const groundMat = new BABYLON.PBRMaterial('groundMat', scene);
    groundMat.albedoColor = new BABYLON.Color3(0.15, 0.15, 0.15);
    groundMat.metallic = 0.3;
    groundMat.roughness = 0.7;

    const ground = BABYLON.MeshBuilder.CreateGround('kubuGround', { width: 15, height: 15, subdivisions: 6 }, scene);
    ground.material = groundMat;
    ground.receiveShadows = true;

    // Render loop
    engine.runRenderLoop(() => {
      scene.render();
    });

    // Resize
    window.addEventListener('resize', () => engine.resize());

    // Clean up on unmount
    return () => {
      engine.dispose();
      window.removeEventListener('resize', () => engine.resize());
    };
  }, []);

  // WebSocket connection & data updates
  useEffect(() => {
    if (!pbrMatRef.current) return;

    // Mock WebSocket — replace URL with your backend WS endpoint
    const ws = new WebSocket('wss://your-kubu-hai-backend/ws/blockchain-events');

    ws.onopen = () => {
      setConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data: NodeData = JSON.parse(event.data);

        // Update sphere emissive color dynamically
        const color = new BABYLON.Color3(data.emissiveR, data.emissiveG, data.emissiveB);
        pbrMatRef.current!.emissiveColor = color;
      } catch (e) {
        console.error('Invalid data from WS:', event.data);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.onerror = (err) => {
      console.error('WebSocket error:', err);
    };

    return () => ws.close();
  }, []);

  return (
    <div>
      <canvas ref={canvasRef} id="renderCanvas" style={{ width: '100vw', height: '100vh', display: 'block' }} />
      <div style={{ position: 'fixed', top: 10, right: 10, color: connected ? 'lime' : 'red' }}>
        WebSocket: {connected ? 'Connected' : 'Disconnected'}
      </div>
    </div>
  );
};

export default KubuHai3DScene;
