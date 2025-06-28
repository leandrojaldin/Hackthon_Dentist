import React from 'react';
import Cubes from './Cubes';

const CubesBackground = () => (
  <div style={{
    position: 'fixed',
    inset: 0,
    zIndex: 0,
    width: '100vw',
    height: '100vh',
    pointerEvents: 'none',
  }}>
    <Cubes 
      gridSize={8}
      maxAngle={60}
      radius={4}
      borderStyle="2px dashed #5227FF"
      faceColor="#1a1a2e"
      rippleColor="#ff6b6b"
      rippleSpeed={1.5}
      autoAnimate={true}
      rippleOnClick={true}
    />
  </div>
);

export default CubesBackground;
