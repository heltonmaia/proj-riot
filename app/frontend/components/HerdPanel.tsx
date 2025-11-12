import React from 'react';
import type { Animal, Herd } from '../types';
import { AnimalStatus } from '../types';

interface HerdPanelProps {
  herds: Herd[];
  animals: Animal[];
  herdColors: string[];
}

const HerdPanel: React.FC<HerdPanelProps> = ({ herds, animals, herdColors }) => {
  const getHerdStats = (herdId: number) => {
    const herdAnimals = animals.filter(a => a.herdId === herdId);
    const total = herdAnimals.length;
    const healthy = herdAnimals.filter(a => a.status === AnimalStatus.Healthy).length;
    const warning = herdAnimals.filter(a => a.status === AnimalStatus.Warning).length;
    const danger = herdAnimals.filter(a => a.status === AnimalStatus.Danger).length;
    const outOfBounds = herdAnimals.filter(a => a.alert?.includes('Fora da área')).length;
    return { total, healthy, warning, danger, outOfBounds };
  };

  return (
    <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', border: '1px solid #ddd' }}>
      <h2 style={{ marginTop: 0, borderBottom: '1px solid #eee', paddingBottom: '0.5rem' }}>Rebanhos</h2>
      <div>
        {herds.map((herd, index) => {
          const stats = getHerdStats(herd.id);
          const color = herdColors[index % herdColors.length];
          return (
            <div key={herd.id} style={{ marginBottom: '1rem', borderBottom: '1px solid #f0f0f0', paddingBottom: '1rem' }}>
              <h3 style={{
                  marginBottom: '0.5rem',
                  marginTop: 0,
                  color: '#333',
                  backgroundColor: `${color}33`, // Fundo suave com a cor do rebanho
                  padding: '0.25rem 0.5rem',
                  borderRadius: '4px',
                  display: 'inline-block',
                  fontWeight: 'bold',
                  fontSize: '1rem',
              }}>
                {herd.name.replace('Rebanho ', '').replace(/ \(.+\)/, '')} ({stats.total} animais)
              </h3>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', padding: '0 0.5rem' }}>
                <span style={{ color: '#28a745' }}><strong>{stats.healthy}</strong> Saudáveis</span>
                <span style={{ color: '#ffc107' }}><strong>{stats.warning}</strong> Alerta</span>
                <span style={{ color: '#dc3545' }}><strong>{stats.danger}</strong> Perigo</span>
              </div>
              {stats.outOfBounds > 0 && (
                <div style={{ fontSize: '0.85rem', fontWeight: 'bold', color: '#dc3545', marginTop: '0.5rem', padding: '0.25rem 0.5rem', backgroundColor: '#dc35451a', borderRadius: '4px' }}>
                    {stats.outOfBounds} animal(s) fora da área designada!
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default HerdPanel;