import React, { createContext, useContext, useState, ReactNode } from 'react';

interface GeminiConfig {
  apiKey: string;
  model: 'gemini-2.5-flash' | 'gemini-2.5-pro-exp-03-25';
  temperature: number;
}

interface GeminiConfigContextType {
  config: GeminiConfig;
  updateConfig: (newConfig: Partial<GeminiConfig>) => void;
}

const defaultConfig: GeminiConfig = {
  apiKey: import.meta.env.VITE_GEMINI_API_KEY || '',
  model: 'gemini-2.5-flash',
  temperature: 0.7,
};

const GeminiConfigContext = createContext<GeminiConfigContextType | undefined>(undefined);

export const GeminiConfigProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [config, setConfig] = useState<GeminiConfig>(defaultConfig);

  const updateConfig = (newConfig: Partial<GeminiConfig>) => {
    setConfig((prev) => ({ ...prev, ...newConfig }));
  };

  return (
    <GeminiConfigContext.Provider value={{ config, updateConfig }}>
      {children}
    </GeminiConfigContext.Provider>
  );
};

export const useGeminiConfig = () => {
  const context = useContext(GeminiConfigContext);
  if (!context) {
    throw new Error('useGeminiConfig must be used within GeminiConfigProvider');
  }
  return context;
};
