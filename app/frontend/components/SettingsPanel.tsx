import React, { useState } from 'react';
import { useGeminiConfig } from '../contexts/GeminiConfigContext';

interface SettingsPanelProps {
  isMobile?: boolean;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ isMobile = false }) => {
  const { config, updateConfig } = useGeminiConfig();
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [isKeyLoaded, setIsKeyLoaded] = useState(!!config.apiKey);

  const handleLoadKey = () => {
    if (apiKey.trim()) {
      console.log('Carregando chave:', apiKey.substring(0, 10) + '...');
      updateConfig({ apiKey: apiKey.trim() });
      setIsKeyLoaded(true);
      console.log('Chave carregada com sucesso!');
    }
  };

  const handleModelChange = (value: 'gemini-2.5-flash' | 'gemini-2.5-pro-exp-03-25') => {
    updateConfig({ model: value });
  };

  const handleTemperatureChange = (value: number) => {
    updateConfig({ temperature: value });
  };

  return (
    <div style={{
      height: '100%',
      padding: isMobile ? '1rem' : '2rem',
      overflowY: 'auto',
      backgroundColor: 'white',
      borderRadius: '8px'
    }}>
      <h2 style={{ marginTop: 0, color: '#333' }}>Configurações do Sistema</h2>

      {/* Google Gemini Configuration */}
      <div style={{
        backgroundColor: '#f8f9fa',
        padding: '1.5rem',
        borderRadius: '8px',
        marginBottom: '1.5rem',
        border: '1px solid #e0e0e0'
      }}>
        <h3 style={{ marginTop: 0, marginBottom: '1rem', color: '#0056b3' }}>
          Configuração do Google Gemini
        </h3>

        {/* API Key */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: 'bold',
            color: '#555'
          }}>
            Chave da API:
          </label>
          <div style={{ position: 'relative' }}>
            <input
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Digite sua chave do Gemini"
              style={{
                width: '100%',
                padding: '0.75rem',
                paddingRight: '80px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '0.95rem',
                fontFamily: 'monospace',
                boxSizing: 'border-box'
              }}
            />
            <button
              onClick={() => setShowKey(!showKey)}
              style={{
                position: 'absolute',
                right: '8px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'transparent',
                border: '1px solid #ccc',
                borderRadius: '4px',
                padding: '0.3rem 0.6rem',
                cursor: 'pointer',
                fontSize: '0.75rem',
                color: '#666'
              }}
            >
              {showKey ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>
          <button
            onClick={handleLoadKey}
            disabled={!apiKey.trim()}
            style={{
              marginTop: '0.75rem',
              width: '100%',
              padding: '0.75rem',
              backgroundColor: apiKey.trim() ? '#0056b3' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '0.95rem',
              fontWeight: 'bold',
              cursor: apiKey.trim() ? 'pointer' : 'not-allowed',
              transition: 'all 0.2s'
            }}
            onMouseOver={(e) => {
              if (apiKey.trim()) {
                e.currentTarget.style.backgroundColor = '#004494';
              }
            }}
            onMouseOut={(e) => {
              if (apiKey.trim()) {
                e.currentTarget.style.backgroundColor = '#0056b3';
              }
            }}
          >
            Carregar
          </button>
          <small style={{ color: '#666', fontSize: '0.85rem', display: 'block', marginTop: '0.5rem' }}>
            A chave será válida durante toda a sessão
          </small>
        </div>

        {/* Model Selection */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: 'bold',
            color: '#555'
          }}>
            Modelo:
          </label>
          <select
            value={config.model}
            onChange={(e) => handleModelChange(e.target.value as 'gemini-2.5-flash' | 'gemini-2.5-pro-exp-03-25')}
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontSize: '0.95rem',
              backgroundColor: 'white',
              cursor: 'pointer'
            }}
          >
            <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
            <option value="gemini-2.5-pro-exp-03-25">Gemini 2.5 Pro (Experimental)</option>
          </select>
          <small style={{ color: '#666', fontSize: '0.85rem' }}>
            Flash: Mais rápido | Pro: Mais preciso
          </small>
        </div>

        {/* Temperature */}
        <div style={{ marginBottom: '0.5rem' }}>
          <label style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: 'bold',
            color: '#555'
          }}>
            Temperatura: {config.temperature.toFixed(1)}
          </label>
          <input
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={config.temperature}
            onChange={(e) => handleTemperatureChange(parseFloat(e.target.value))}
            style={{
              width: '100%',
              cursor: 'pointer'
            }}
          />
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            fontSize: '0.8rem',
            color: '#666',
            marginTop: '0.25rem'
          }}>
            <span>0.0 (Preciso)</span>
            <span>1.0 (Balanceado)</span>
            <span>2.0 (Criativo)</span>
          </div>
          <small style={{ color: '#666', fontSize: '0.85rem', display: 'block', marginTop: '0.5rem' }}>
            Controla a aleatoriedade das respostas da IA
          </small>
        </div>
      </div>

      {/* Status */}
      {isKeyLoaded ? (
        <div style={{
          backgroundColor: '#d4edda',
          padding: '1rem',
          borderRadius: '8px',
          border: '1px solid #c3e6cb',
          fontSize: '0.9rem'
        }}>
          <strong style={{ color: '#155724' }}>
            ✓ Configuração salva
          </strong>
          <p style={{ margin: '0.5rem 0 0 0', color: '#666', fontSize: '0.85rem' }}>
            O chat com IA está pronto para uso com as configurações acima.
          </p>
        </div>
      ) : (
        <div style={{
          backgroundColor: '#fff3cd',
          padding: '1rem',
          borderRadius: '8px',
          border: '1px solid #ffeaa7',
          fontSize: '0.9rem'
        }}>
          <strong style={{ color: '#856404' }}>
            ⚠ Chave da API não configurada
          </strong>
          <p style={{ margin: '0.5rem 0 0 0', color: '#666', fontSize: '0.85rem' }}>
            Digite uma chave válida e clique em "Carregar" para habilitar o chat com IA.
          </p>
        </div>
      )}
    </div>
  );
};

export default SettingsPanel;
