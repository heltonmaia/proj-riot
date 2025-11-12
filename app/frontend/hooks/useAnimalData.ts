import { useState, useEffect } from 'react';
import type { Animal, Herd } from '../types';
import { API_ENDPOINTS, POLLING_INTERVAL } from '../config';

const useAnimalData = () => {
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [herds, setHerds] = useState<Herd[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar dados da API
  const fetchData = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.data);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: { animals: Animal[], herds: Herd[] } = await response.json();

      setAnimals(data.animals);
      setHerds(data.herds);
      setError(null);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch data';
      console.error("Failed to fetch data from API:", errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Efeito inicial: busca dados uma vez
  useEffect(() => {
    fetchData();
  }, []);

  // Efeito de polling: atualiza dados periodicamente
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, POLLING_INTERVAL);

    return () => clearInterval(interval);
  }, []);

  return { animals, herds, loading, error };
};

export default useAnimalData;