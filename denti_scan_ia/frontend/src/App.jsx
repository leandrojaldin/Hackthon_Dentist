import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import GridMotionBackground from './components/GridMotionBackground';
import './index.css';

function App() {
  return (
    <>
      <GridMotionBackground />
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/registro" element={<RegisterPage />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;