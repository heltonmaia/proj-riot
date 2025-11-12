import React from 'react';
import type { Animal, Herd } from '../types';
import { AnimalStatus } from '../types';
import { ThermometerIcon, StepsIcon, CloseIcon, CowIcon, BreedIcon, AgeIcon, WeightIcon, TagIcon } from './Icons';

interface AnimalDetailPanelProps {
  animal: Animal;
  herds: Herd[];
  onClose: () => void;
}

const getStatusInfo = (status: AnimalStatus): { text: string; color: string } => {
    switch (status) {
        case AnimalStatus.Healthy:
            return { text: 'Saudável', color: '#28a745' };
        case AnimalStatus.Warning:
            return { text: 'Alerta', color: '#ffc107' };
        case AnimalStatus.Danger:
            return { text: 'Perigo', color: '#dc3545' };
        default:
            return { text: 'Desconhecido', color: '#6c757d' };
    }
};

const DetailItem = ({ icon, label, value }: { icon: React.ReactNode, label: string, value: string | number }) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.75rem' }}>
        <div style={{ flexShrink: 0 }}>{icon}</div>
        <span>{label}: <strong>{value}</strong></span>
    </div>
);


const AnimalDetailPanel: React.FC<AnimalDetailPanelProps> = ({ animal, herds, onClose }) => {
  const statusInfo = getStatusInfo(animal.status);
  const herd = herds.find(h => h.id === animal.herdId);
  const herdShortName = herd ? herd.name.replace('Rebanho ', '').replace(/ \(.+\)/, '') : 'Desconhecido';

  return (
    <div style={{ 
        backgroundColor: 'white',
        padding: '1rem', 
        borderRadius: '8px', 
        border: '1px solid #ddd', 
        position: 'relative',
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column'
    }}>
      <button onClick={onClose} style={{ position: 'absolute', top: '0.5rem', right: '0.5rem', background: 'none', border: 'none', cursor: 'pointer', padding: '0.25rem', zIndex: 1 }}>
        <CloseIcon />
      </button>
      <h2 style={{ marginTop: 0, paddingRight: '2rem', lineHeight: 1.2 }}>
        {animal.name}
        <span style={{ display: 'block', fontSize: '0.9rem', color: '#666', fontWeight: 'normal', marginTop: '0.25rem' }}>
          do Rebanho {herdShortName}
        </span>
      </h2>
      <div style={{ marginBottom: '0.5rem' }}>
        <strong>Status: </strong>
        <span style={{ color: statusInfo.color, fontWeight: 'bold' }}>
          {statusInfo.text}
        </span>
      </div>
      
      {animal.alert && (
        <div style={{
            padding: '0.5rem',
            borderRadius: '4px',
            backgroundColor: statusInfo.color + '20', // transparent version of status color
            color: statusInfo.color,
            border: `1px solid ${statusInfo.color}`,
            fontSize: '0.9rem',
            fontWeight: 'bold',
            textAlign: 'center',
        }}>
            {animal.alert.toUpperCase()}
        </div>
      )}
      
      <div style={{marginTop: '1rem'}}>
        <DetailItem icon={<TagIcon />} label="Colar" value={animal.collarId} />
        <DetailItem icon={<CowIcon />} label="Tipo" value={animal.type} />
        <DetailItem icon={<BreedIcon />} label="Raça" value={animal.breed} />
        <DetailItem icon={<AgeIcon />} label="Idade" value={`${animal.age} meses`} />
        <DetailItem icon={<WeightIcon />} label="Peso" value={`${animal.weight} kg`} />
        <DetailItem icon={<ThermometerIcon />} label="Temperatura" value={`${animal.temperature.toFixed(1)}°C`} />
        <DetailItem icon={<StepsIcon />} label="Passos hoje" value={animal.steps} />
      </div>
      
      <div style={{ marginTop: 'auto', paddingTop: '1rem', fontSize: '0.8rem', color: '#666' }}>
        <strong>Localização:</strong><br/>
        Lat: {animal.location.lat.toFixed(6)}, Lng: {animal.location.lng.toFixed(6)}
      </div>
    </div>
  );
};

export default AnimalDetailPanel;