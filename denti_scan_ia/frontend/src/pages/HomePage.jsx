import React from 'react';
import { Link } from 'react-router-dom';
import InteractiveBackground from '../components/InteractiveBackground';

const HomePage = () => {
  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <InteractiveBackground />
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-white text-center px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-4 animate-fade-in-down">
          DentiScan <span className="text-[#3A86FF]">IA</span>
        </h1>
        <p className="text-lg md:text-2xl mb-8 max-w-3xl animate-fade-in-up">
          Tu Salud Dental, Analizada con Inteligencia Artificial. Sube una imagen y recibe un análisis preliminar en segundos.
        </p>
        <Link to="/registro">
          <button className="bg-[#3A86FF] hover:bg-[#2a75e8] text-white font-bold py-3 px-8 rounded-full text-xl transition-transform transform hover:scale-105 duration-300">
            Comenzar Análisis Gratuito
          </button>
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
