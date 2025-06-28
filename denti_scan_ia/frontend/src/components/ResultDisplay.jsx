import React from 'react';

function ResultDisplay({ result }) {
  if (!result) {
    return null;
  }

  const { diagnosis_result, confidence_score, recommendations, highlighted_image_url, warning_message } = result;

  return (
    <div className="mt-6 p-4 border rounded-lg shadow-sm bg-white">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Resultados del Análisis</h2>

      {highlighted_image_url && (
        <div className="mb-4 text-center">
          <h3 className="text-lg font-medium text-gray-700 mb-2">Imagen Procesada:</h3>
          <img
            src={`http://localhost:8000${highlighted_image_url}`}
            alt="Highlighted Result"
            className="max-w-full h-auto rounded-lg shadow-md mx-auto"
          />
        </div>
      )}

      <div className="mb-3">
        <p className="text-lg font-medium text-gray-700">Diagnóstico:</p>
        <p className="text-xl font-bold text-blue-600">{diagnosis_result}</p>
      </div>

      <div className="mb-3">
        <p className="text-lg font-medium text-gray-700">Puntuación de Confianza:</p>
        <p className="text-xl font-bold text-blue-600">{(confidence_score * 100).toFixed(2)}%</p>
      </div>

      <div className="mb-4">
        <p className="text-lg font-medium text-gray-700">Recomendaciones:</p>
        <p className="text-md text-gray-800">{recommendations}</p>
      </div>

      {warning_message && (
        <div className="p-3 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 rounded-md">
          <p className="font-bold">Advertencia:</p>
          <p className="text-sm">{warning_message}</p>
        </div>
      )}
    </div>
  );
}

export default ResultDisplay;