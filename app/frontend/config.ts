/**
 * Configurações da aplicação
 */

// URL base da API do backend
// Em produção: usa caminho relativo /riot (mesmo domínio via nginx)
// Em desenvolvimento: usa http://localhost:8001
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Endpoints da API
export const API_ENDPOINTS = {
  animals: `${API_BASE_URL}/api/animals`,
  herds: `${API_BASE_URL}/api/herds`,
  data: `${API_BASE_URL}/api/data`,
  animalById: (id: number) => `${API_BASE_URL}/api/animals/${id}`,
  herdById: (id: number) => `${API_BASE_URL}/api/herds/${id}`,
  health: `${API_BASE_URL}/health`,
};

// Intervalo de polling (em ms)
export const POLLING_INTERVAL = 2000;
