import React, { useState } from 'react';
import InteractiveBackground from '../components/InteractiveBackground';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    birthDate: '',
  });
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validar que todos los campos estén completos
    if (!formData.name.trim()) {
      alert('Por favor, ingresa tu nombre completo.');
      return;
    }
    
    if (!formData.email.trim()) {
      alert('Por favor, ingresa tu correo electrónico.');
      return;
    }
    
    if (!formData.birthDate) {
      alert('Por favor, selecciona tu fecha de nacimiento.');
      return;
    }
    
    if (!image) {
      alert('Por favor, sube una imagen dental.');
      return;
    }
    
    setIsLoading(true);

    const data = new FormData();
    data.append('name', formData.name.trim());
    data.append('email', formData.email.trim());
    data.append('birthDate', formData.birthDate);
    data.append('dentalImage', image);

    try {
      console.log('Enviando datos:', {
        name: formData.name.trim(),
        email: formData.email.trim(),
        birthDate: formData.birthDate,
        imageName: image.name
      });
      
      // Aquí va la llamada a tu backend FastAPI
      const response = await fetch('http://localhost:8000/analyze_dental_image', {
        method: 'POST',
        body: data,
      });
      
      if (!response.ok) {
        throw new Error(`Error del servidor: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('Análisis recibido:', result);
      
      if (result.status === 'success') {
        alert(`¡Análisis completado exitosamente!\n\nDiagnóstico: ${result.data.diagnosis}\nConfianza: ${(result.data.confidence * 100).toFixed(1)}%\n\nRecomendaciones:\n${result.data.recommendations.join('\n')}`);
      } else {
        alert(`Error: ${result.message || 'Error desconocido'}`);
      }
    } catch (error) {
      console.error('Error al enviar el formulario:', error);
      alert(`Hubo un error al procesar tu solicitud: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative w-screen min-h-screen overflow-hidden flex items-center justify-center p-4">
      <div className="absolute inset-0 opacity-30">
        <InteractiveBackground />
      </div>
      <div className="relative z-10 w-full max-w-4xl bg-[#1C2541]/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8 text-white">
        <h2 className="text-3xl font-bold text-center mb-6">Registro y Análisis Dental</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Columna de Datos */}
          <div className="space-y-6">
            <div>
              <label htmlFor="name" className="block mb-2 text-sm font-medium">
                Nombre Completo <span className="text-red-400">*</span>
              </label>
              <input 
                type="text" 
                name="name" 
                id="name" 
                value={formData.name}
                onChange={handleInputChange} 
                className="w-full bg-gray-700/50 border border-gray-600 rounded-lg p-2.5 focus:ring-[#3A86FF] focus:border-[#3A86FF] transition-colors" 
                placeholder="Ej: Juan Pérez"
                required 
              />
            </div>
            <div>
              <label htmlFor="email" className="block mb-2 text-sm font-medium">
                Correo Electrónico <span className="text-red-400">*</span>
              </label>
              <input 
                type="email" 
                name="email" 
                id="email" 
                value={formData.email}
                onChange={handleInputChange} 
                className="w-full bg-gray-700/50 border border-gray-600 rounded-lg p-2.5 focus:ring-[#3A86FF] focus:border-[#3A86FF] transition-colors" 
                placeholder="ejemplo@email.com"
                required 
              />
            </div>
            <div>
              <label htmlFor="birthDate" className="block mb-2 text-sm font-medium">
                Fecha de Nacimiento <span className="text-red-400">*</span>
              </label>
              <input 
                type="date" 
                name="birthDate" 
                id="birthDate" 
                value={formData.birthDate}
                onChange={handleInputChange} 
                className="w-full bg-gray-700/50 border border-gray-600 rounded-lg p-2.5 focus:ring-[#3A86FF] focus:border-[#3A86FF] transition-colors" 
                required 
              />
            </div>
          </div>
          {/* Columna de Imagen */}
          <div className="flex flex-col items-center justify-center">
            <label htmlFor="dentalImage" className="w-full h-48 border-2 border-dashed border-gray-500 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-gray-700/30 transition-colors">
              {imagePreview ? (
                <img src={imagePreview} alt="Vista previa" className="h-full w-full object-cover rounded-lg"/>
              ) : (
                <div className="text-center">
                  <p className="text-gray-400">Arrastra y suelta tu imagen aquí</p>
                  <p className="text-sm text-gray-500">o haz clic para seleccionar</p>
                </div>
              )}
            </label>
            <input type="file" id="dentalImage" name="dentalImage" accept="image/*" onChange={handleImageChange} className="hidden" />
          </div>

          {/* Botón de envío */}
          <div className="md:col-span-2 text-center mt-4">
            <button type="submit" disabled={isLoading} className="w-full md:w-auto bg-[#3A86FF] hover:bg-[#2a75e8] disabled:bg-gray-500 disabled:cursor-not-allowed font-bold py-3 px-12 rounded-full text-lg transition-all duration-300">
              {isLoading ? 'Analizando...' : 'Enviar para Análisis'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
