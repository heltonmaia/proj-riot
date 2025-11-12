import type { GroundingChunk as GenAIGroundingChunk } from '@google/genai';

export enum AnimalStatus {
  Healthy,
  Warning,
  Danger,
}

export interface Herd {
  id: number;
  name: string;
  region: string;
  location: {
    lat: number;
    lng: number;
  };
  polygon: { lat: number; lng: number; }[];
}

export interface AnimalHistoryRecord {
  date: string;
  status: AnimalStatus;
  location: {
    lat: number;
    lng: number;
  };
  temperature: number;
  steps: number;
}

export interface Animal {
  id: number;
  collarId: string;
  herdId: number;
  name: string;
  status: AnimalStatus;
  alert?: string;
  location: {
    lat: number;
    lng: number;
  };
  temperature: number;
  steps: number;
  type: 'Vaca' | 'Touro' | 'Bezerro';
  breed: string;
  age: number; // in months
  weight: number; // in kg
  history?: AnimalHistoryRecord[];
}

export interface UserLocation {
  latitude: number;
  longitude: number;
}

export type GroundingChunk = GenAIGroundingChunk;

export interface ChatMessage {
    id: string;
    text: string;
    isUser: boolean;
    sources?: GroundingChunk[];
}