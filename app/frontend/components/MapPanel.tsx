import React, { useEffect, useRef } from 'react';
import type { Animal, Herd } from '../types';
import { AnimalStatus } from '../types';

// Declaração para o TypeScript reconhecer a variável global L do Leaflet
declare const L: any;

interface MapPanelProps {
  animals: Animal[];
  herds: Herd[];
  onSelectAnimal: (animal: Animal) => void;
  selectedAnimal: Animal | null;
  herdColors: string[];
  onDeselectAnimal: () => void;
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

const createTooltipContent = (animal: Animal, herdShortName: string, statusInfo: { text: string; color: string }) => {
    const alertHtml = animal.alert ? `<div style="font-weight: bold; color: #dc3545; margin-top: 4px;">ALERTA: ${animal.alert}</div>` : '';

    return `
        <div style="font-family: sans-serif; font-size: 13px; line-height: 1.5; min-width: 220px;">
            <div style="font-size: 16px; font-weight: bold; color: #333; margin-bottom: 4px;">${animal.name}</div>
            <div style="border-bottom: 1px solid #eee; margin-bottom: 6px; padding-bottom: 6px;">
                <strong>Rebanho:</strong> ${herdShortName}<br>
                <strong>Status:</strong> <span style="color: ${statusInfo.color}; font-weight: bold;">${statusInfo.text}</span>
                ${alertHtml}
            </div>
            <div>
                <strong>Colar:</strong> ${animal.collarId}<br>
                <strong>Temp:</strong> ${animal.temperature.toFixed(1)}°C | <strong>Passos:</strong> ${animal.steps}<br>
                <strong>Tipo:</strong> ${animal.type} (${animal.breed})<br>
                <strong>Idade:</strong> ${animal.age} meses | <strong>Peso:</strong> ${animal.weight} kg<br>
                <strong>Local:</strong> ${animal.location.lat.toFixed(4)}, ${animal.location.lng.toFixed(4)}
            </div>
        </div>
    `;
};


const MapPanel: React.FC<MapPanelProps> = ({ animals, herds, onSelectAnimal, selectedAnimal, herdColors, onDeselectAnimal }) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const markersRef = useRef<any>(null);

  // Efeito para inicializar o mapa (executa apenas uma vez)
  useEffect(() => {
    if (mapContainerRef.current && !mapRef.current) {
      const getCenter = () => {
        if (herds.length === 0) return { lat: -5.83, lng: -35.20 }; // Natal, RN
        const avgLat = herds.reduce((sum, h) => sum + h.location.lat, 0) / herds.length;
        const avgLng = herds.reduce((sum, h) => sum + h.location.lng, 0) / herds.length;
        return { lat: avgLat, lng: avgLng };
      };

      const center = getCenter();
      
      const map = L.map(mapContainerRef.current).setView([center.lat, center.lng], 12);
      mapRef.current = map;

      map.on('click', () => {
        onDeselectAnimal();
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);

      markersRef.current = L.layerGroup().addTo(map);
    }
  }, [herds, onDeselectAnimal]);

  // Efeito para atualizar marcadores
  useEffect(() => {
    if (mapRef.current && markersRef.current) {
      const markersLayer = markersRef.current;
      markersLayer.clearLayers();

      // 1. Desenhar áreas dos rebanhos e marcadores de nome
      herds.forEach((herd, index) => {
        const color = herdColors[index % herdColors.length];

        // Desenhar polígono fixo do rebanho
        if (herd.polygon && herd.polygon.length > 2) {
            L.polygon(herd.polygon, {
                color: color,
                fillColor: color,
                fillOpacity: 0.15,
                weight: 1.5,
            }).addTo(markersLayer);
        } else {
            // Fallback caso não haja polígono definido
             L.circle([herd.location.lat, herd.location.lng], {
                radius: 500, // 500 metros
                color: color,
                fillColor: color,
                fillOpacity: 0.1,
                weight: 1,
                dashArray: '5, 5'
            }).addTo(markersLayer);
        }
        
        // Ícone com nome no centro do rebanho
        const herdIcon = L.divIcon({
          className: 'herd-label-icon',
          html: `<span style="color: ${color};">${herd.name}</span>`
        });
        L.marker([herd.location.lat, herd.location.lng], { icon: herdIcon }).addTo(markersLayer);
      });
      
      // 2. Desenhar marcadores dos animais
      animals.forEach(animal => {
        const isSelected = selectedAnimal?.id === animal.id;
        const hasAlert = !!animal.alert;
        const statusInfo = getStatusInfo(animal.status);

        const marker = L.circleMarker([animal.location.lat, animal.location.lng], {
          radius: isSelected ? 10 : 6,
          fillColor: statusInfo.color,
          color: hasAlert && !isSelected ? '#dc3545' : (isSelected ? '#fff' : '#000'),
          weight: hasAlert || isSelected ? 3 : 1,
          opacity: 1,
          fillOpacity: 0.8
        }).addTo(markersLayer);

        const herd = herds.find(h => h.id === animal.herdId);
        const herdShortName = herd ? herd.name.replace('Rebanho ', '').replace(/ \(.+\)/, '') : 'Desconhecido';

        const tooltipContent = createTooltipContent(animal, herdShortName, statusInfo);

        marker.bindTooltip(tooltipContent, {
            sticky: true,
        });

        marker.on('click', (e: any) => {
          L.DomEvent.stopPropagation(e);
          onSelectAnimal(animal);
        });
      });
    }
  }, [animals, herds, selectedAnimal, onSelectAnimal, herdColors]);


  return <div ref={mapContainerRef} style={{ width: '100%', height: '100%', borderRadius: '8px', overflow: 'hidden' }} />;
};

export default MapPanel;