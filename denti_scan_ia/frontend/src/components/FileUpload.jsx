import React, { useState } from 'react';

function FileUpload({ onImageUpload, loading }) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setSelectedImage(null);
      setPreviewUrl(null);
    }
  };

  const handleAnalyzeClick = () => {
    if (selectedImage) {
      onImageUpload(selectedImage);
    }
  };

  return (
    <div className="mb-6 p-4 border rounded-lg shadow-sm bg-gray-50">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Cargar Imagen Dental</h2>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="block w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-blue-50 file:text-blue-700
          hover:file:bg-blue-100
        "
      />
      {previewUrl && (
        <div className="mt-4 text-center">
          <h3 className="text-lg font-medium text-gray-700 mb-2">Vista Previa:</h3>
          <img src={previewUrl} alt="Preview" className="max-w-full h-auto rounded-lg shadow-md mx-auto" />
        </div>
      )}
      <button
        onClick={handleAnalyzeClick}
        disabled={!selectedImage || loading}
        className={`mt-6 w-full py-3 px-4 rounded-lg text-white font-bold transition duration-300
          ${selectedImage && !loading ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-400 cursor-not-allowed'}
        `}
      >
        {loading ? 'Analizando...' : 'Analizar Imagen'}
      </button>
    </div>
  );
}

export default FileUpload;