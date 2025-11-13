import React, { useMemo } from 'react';
import type { Animal, Herd } from '../types';
import { AnimalStatus } from '../types';
import { ThermometerIcon, StepsIcon, CloseIcon, CowIcon, BreedIcon, AgeIcon, WeightIcon, TagIcon } from './Icons';
import { API_BASE_URL } from '../config';

interface AnimalDetailPanelProps {
  animal: Animal;
  herds: Herd[];
  onClose: () => void;
}

// Lista de vídeos disponíveis
const AVAILABLE_VIDEOS = [
  'bezerra deitada.mp4',
  'bezerro mamando.mp4',
  'bezerro ócio.mp4',
  'vaca amamentando.mp4',
  'vaca atrás do bezerro.mp4',
  'vaca ordenha com teteira.mp4',
  'vaca ordenha sem teteiras.mp4',
  'vaca pastejo alto escore.mp4',
  'vaca_pastejo_baixo_escore.mp4',
  'vaca sala de espera.mp4',
];

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
  const [showVideo, setShowVideo] = React.useState(false);
  const statusInfo = getStatusInfo(animal.status);
  const herd = herds.find(h => h.id === animal.herdId);
  const herdShortName = herd ? herd.name.replace('Rebanho ', '').replace(/ \(.+\)/, '') : 'Desconhecido';

  // Seleciona vídeo aleatório baseado no ID do animal (sempre o mesmo vídeo para o mesmo animal)
  const videoFilename = useMemo(() => {
    const index = animal.id % AVAILABLE_VIDEOS.length;
    const filename = AVAILABLE_VIDEOS[index];
    console.log('Animal:', animal.name, 'ID:', animal.id, 'Video:', filename);
    console.log('URL do vídeo:', `${API_BASE_URL}/api/videos/${encodeURIComponent(filename)}`);
    return filename;
  }, [animal.id, animal.name]);

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

      {/* Vídeo do animal */}
      <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
        <div style={{
          fontSize: '0.9rem',
          fontWeight: 'bold',
          marginBottom: '0.5rem',
          color: '#333'
        }}>
          📹 Vídeo do Animal
        </div>

        {!showVideo ? (
          /* Thumbnail placeholder */
          <div style={{
            width: '100%',
            height: '200px',
            backgroundColor: '#f0f0f0',
            borderRadius: '8px',
            border: '2px solid #ddd',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '1rem',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
          onClick={() => setShowVideo(true)}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#e8e8e8';
            e.currentTarget.style.borderColor = '#0056b3';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = '#f0f0f0';
            e.currentTarget.style.borderColor = '#ddd';
          }}
          >
            <div style={{
              fontSize: '48px',
              color: '#0056b3'
            }}>
              ▶
            </div>
            <div style={{
              fontSize: '0.9rem',
              color: '#666',
              textAlign: 'center',
              padding: '0 1rem'
            }}>
              Clique para assistir o vídeo
            </div>
          </div>
        ) : (
          /* Player de vídeo com iframe */
          <div style={{ position: 'relative' }}>
            <iframe
              src={`${API_BASE_URL}/api/videos/${encodeURIComponent(videoFilename)}`}
              style={{
                width: '100%',
                height: '250px',
                border: 'none',
                borderRadius: '8px',
                backgroundColor: '#000'
              }}
              title="Vídeo do Animal"
              allow="autoplay"
            />
            <button
              onClick={() => setShowVideo(false)}
              style={{
                position: 'absolute',
                top: '8px',
                right: '8px',
                backgroundColor: 'rgba(255,255,255,0.9)',
                border: 'none',
                borderRadius: '4px',
                padding: '4px 8px',
                cursor: 'pointer',
                fontSize: '0.85rem',
                fontWeight: 'bold'
              }}
            >
              ✕ Fechar
            </button>
          </div>
        )}

        <div style={{
          fontSize: '0.75rem',
          color: '#888',
          marginTop: '0.5rem',
          textAlign: 'center'
        }}>
          {videoFilename}
        </div>
      </div>

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