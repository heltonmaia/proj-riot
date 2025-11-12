import React from 'react';
import type { Animal } from '../types';
import { AnimalStatus } from '../types';

interface StatsPanelProps {
  animals: Animal[];
}

const StatsPanel: React.FC<StatsPanelProps> = ({ animals }) => {
  const totalAnimals = animals.length;
  if (totalAnimals === 0) return null;

  const healthyCount = animals.filter(a => a.status === AnimalStatus.Healthy).length;
  const warningCount = animals.filter(a => a.status === AnimalStatus.Warning).length;
  const dangerCount = animals.filter(a => a.status === AnimalStatus.Danger).length;

  const StatCard = ({ label, value, color }: { label: string, value: string | number, color?: string }) => (
    <div style={{ flex: 1, backgroundColor: 'white', padding: '1rem', borderRadius: '8px', textAlign: 'center', border: '1px solid #ddd' }}>
      <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: color || '#333' }}>{value}</div>
      <div style={{ fontSize: '0.8rem', color: '#666', textTransform: 'uppercase' }}>{label}</div>
    </div>
  );

  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <StatCard label="Total de Animais" value={totalAnimals} />
      <StatCard label="Saudáveis" value={healthyCount} color="#28a745" />
      <StatCard label="Alerta" value={warningCount} color="#ffc107" />
      <StatCard label="Perigo" value={dangerCount} color="#dc3545" />
    </div>
  );
};

export default StatsPanel;