import React, { useState, useEffect, useRef } from 'react';
import type { Animal, Herd, ChatMessage, UserLocation } from '../types';
import { askQuestion } from '../services/geminiService';
import { ChatBotIcon, SendIcon } from './Icons';
import { AnimalStatus } from '../types';

interface ChatPanelProps {
  animals: Animal[];
  herds: Herd[];
  selectedAnimal: Animal | null;
  isMobile: boolean;
}

const parseMarkdownToHTML = (text: string): string => {
    // Basic escaping to prevent unwanted HTML injection from the model
    const escapedText = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    const lines = escapedText.split('\n');
    let html = '';
    let inList = false;

    lines.forEach((line) => {
        // Apply markdown formatting after escaping
        let processedLine = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        if (processedLine.trim().startsWith('- ')) {
            if (!inList) {
                html += '<ul style="margin: 0.5rem 0; padding-left: 1.25rem;">';
                inList = true;
            }
            html += `<li style="margin-bottom: 0.25rem;">${processedLine.trim().substring(2)}</li>`;
        } else {
            if (inList) {
                html += '</ul>';
                inList = false;
            }
            
            if (html.length > 0 && !html.endsWith('</ul>')) {
                 html += '<br />';
            }
            html += processedLine;
        }
    });

    if (inList) {
        html += '</ul>';
    }
    
    return html.replace(/^<br \/>/, ''); // Remove leading break if any
};


const ChatPanel: React.FC<ChatPanelProps> = ({ animals, herds, selectedAnimal, isMobile }) => {
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    try {
        const savedMessages = sessionStorage.getItem('chatHistory');
        if (savedMessages) {
            return JSON.parse(savedMessages);
        }
    } catch (error) {
        console.error("Falha ao carregar o histórico do chat do sessionStorage", error);
    }
    return [{
        id: 'initial',
        text: 'Olá! Sou seu assistente para o monitoramento do rebanho. Como posso ajudar?',
        isUser: false
    }];
  });

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userLocation, setUserLocation] = useState<UserLocation | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
     if (messages.length > 1 || (messages.length === 1 && messages[0].id !== 'initial')) {
        sessionStorage.setItem('chatHistory', JSON.stringify(messages));
     }
  }, [messages]);

  useEffect(() => {
    if (!userLocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setUserLocation({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                });
            },
            (error) => {
                console.error("Erro ao obter a localização do usuário:", error);
            }
        );
    }
  }, [userLocation]);
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);


  const generateContext = () => {
    const statusMap = {
        [AnimalStatus.Healthy]: 'Saudável',
        [AnimalStatus.Warning]: 'Alerta',
        [AnimalStatus.Danger]: 'Perigo',
    }
    const generalStats = `
      RESUMO GERAL:
      - Total de animais: ${animals.length}
      - Saudáveis: ${animals.filter(a => a.status === AnimalStatus.Healthy).length}
      - Em alerta: ${animals.filter(a => a.status === AnimalStatus.Warning).length}
      - Em perigo: ${animals.filter(a => a.status === AnimalStatus.Danger).length}
    `;

    const herdSummary = herds.map(herd => {
        const herdAnimals = animals.filter(a => a.herdId === herd.id);
        const statusCounts = herdAnimals.reduce((acc, animal) => {
            acc[animal.status] = (acc[animal.status] || 0) + 1;
            return acc;
        }, {} as Record<AnimalStatus, number>);
        
        const outOfBoundsAnimals = herdAnimals.filter(a => a.alert?.includes('Fora da área designada'));
        const outOfBoundsCount = outOfBoundsAnimals.length;
        let outOfBoundsInfo = `Animais fora da área: ${outOfBoundsCount}.`;
        if (outOfBoundsCount > 0) {
            const animalNames = outOfBoundsAnimals.map(a => a.name).join(', ');
            outOfBoundsInfo = `Animais fora da área: ${outOfBoundsCount} (${animalNames}).`;
        }

        return `- Rebanho "${herd.name}": ${herdAnimals.length} animais. (Saudáveis: ${statusCounts[AnimalStatus.Healthy] || 0}, Alerta: ${statusCounts[AnimalStatus.Warning] || 0}, Perigo: ${statusCounts[AnimalStatus.Danger] || 0}). ${outOfBoundsInfo}`;
    }).join('\n');
    
    const herdSummaryContext = `
RESUMO POR REBANHO:
${herdSummary}
    `;

    let selectedAnimalContext = '';
    if (selectedAnimal) {
        const animalData = animals.find(a => a.id === selectedAnimal.id);
        const herd = herds.find(h => h.id === selectedAnimal.herdId);
        const herdInfo = herd ? `do Rebanho ${herd.name} (Região: ${herd.region})` : '';

        let historyContext = '';
        if (animalData?.history && animalData.history.length > 0) {
            const weeklyHistory = animalData.history;
            historyContext = `
HISTÓRICO DA SEMANA:
${weeklyHistory.map(h => 
`- Data: ${h.date}, Status: ${statusMap[h.status]}, Temp: ${h.temperature.toFixed(1)}°C, Passos: ${h.steps}`
).join('\n')}
`;
        }
        
        selectedAnimalContext = `
DADOS DO ANIMAL SELECIONADO (HOJE):
- Nome: ${selectedAnimal.name} (Colar: ${selectedAnimal.collarId})
- Rebanho: ${herdInfo}
- Tipo: ${selectedAnimal.type}
- Raça: ${selectedAnimal.breed}
- Idade: ${selectedAnimal.age} meses
- Peso: ${selectedAnimal.weight} kg
- Status: ${statusMap[selectedAnimal.status]}
${selectedAnimal.alert ? `- ALERTA ATIVO: ${selectedAnimal.alert}\n` : ''}- Temperatura: ${selectedAnimal.temperature}°C
- Passos: ${selectedAnimal.steps}
- Localização: Lat ${selectedAnimal.location.lat.toFixed(4)}, Lng ${selectedAnimal.location.lng.toFixed(4)}
${historyContext}`;
    }

    return `CONTEXTO ATUAL DA FAZENDA:\n${generalStats}\n${herdSummaryContext}\n${selectedAnimalContext}`;
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { id: Date.now().toString(), text: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const context = generateContext();
      const { text, sources } = await askQuestion(input, context, userLocation);
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text,
        isUser: false,
        sources,
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Falha ao obter resposta do Gemini:", error);
      const errorMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          text: "Ocorreu um erro ao buscar a resposta. Tente novamente.",
          isUser: false,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };
  
  const mobileStyles: React.CSSProperties = {
      position: 'relative',
      width: '100%',
      height: '100%',
      top: 0,
      left: 0,
      borderRadius: 0,
      border: 'none',
      boxShadow: 'none',
  };
  
  const desktopStyles: React.CSSProperties = {
      width: '100%',
      height: '450px',
      maxHeight: '50vh',
      borderRadius: '8px',
      border: '1px solid #ddd',
  };

  return (
    <div
      style={{
        backgroundColor: 'white',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        ...(isMobile ? mobileStyles : desktopStyles)
    }}>
        <div 
          style={{
            padding: '0 1rem',
            borderBottom: '1px solid #eee',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexShrink: 0,
            height: '50px',
            userSelect: 'none',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <ChatBotIcon /> 
            <h2 style={{ margin: 0, fontSize: '1.1rem' }}>Assistente R-IoT</h2>
          </div>
        </div>
      
        <>
          <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 0.5rem 0 1rem' }}>
            {messages.map((msg) => (
              <div key={msg.id} style={{ marginBottom: '1rem', display: 'flex', flexDirection: msg.isUser ? 'row-reverse' : 'row' }}>
                <div style={{
                  backgroundColor: msg.isUser ? '#dcf8c6' : '#f1f0f0',
                  padding: '0.5rem 1rem',
                  borderRadius: '10px',
                  maxWidth: '80%',
                  marginRight: msg.isUser ? '0.5rem' : '0',
                }}>
                  {msg.isUser ? (
                    <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{msg.text}</p>
                   ) : (
                    <div 
                        style={{ margin: 0, whiteSpace: 'normal', wordBreak: 'break-word', lineHeight: '1.5' }}
                        dangerouslySetInnerHTML={{ __html: parseMarkdownToHTML(msg.text) }} 
                    />
                   )}
                  {msg.sources && msg.sources.length > 0 && (
                    <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', borderTop: '1px solid #ccc', paddingTop: '0.5rem' }}>
                      <strong>Fontes:</strong>
                      <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>
                        {msg.sources.map((source, i) => source.maps && (
                          <li key={i}><a href={source.maps.uri} target="_blank" rel="noopener noreferrer">{source.maps.title || 'Ver no mapa'}</a></li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && <div style={{textAlign: 'center', color: '#666'}}>Pensando...</div>}
            <div ref={messagesEndRef} />
          </div>
          <div style={{ padding: '1rem', borderTop: '1px solid #eee', backgroundColor: '#fafafa', flexShrink: 0 }}>
            <div style={{ display: 'flex', border: '1px solid #ccc', borderRadius: '20px', backgroundColor: 'white' }}>
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Pergunte sobre o rebanho..."
                disabled={isLoading}
                style={{ flex: 1, border: 'none', padding: '0.75rem', borderRadius: '20px 0 0 20px', outline: 'none', background: 'transparent', color: '#333' }}
              />
              <button onClick={handleSend} disabled={isLoading || !input.trim()} style={{ background: 'none', border: 'none', padding: '0.75rem', cursor: 'pointer', color: '#007bff' }}>
                <SendIcon />
              </button>
            </div>
          </div>
        </>
    </div>
  );
};

export default ChatPanel;