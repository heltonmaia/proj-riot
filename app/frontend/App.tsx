import React, { useState, useEffect } from 'react';
import useAnimalData from './hooks/useAnimalData';
import type { Animal } from './types';
import MapPanel from './components/MapPanel';
import StatsPanel from './components/StatsPanel';
import ChatPanel from './components/ChatPanel';
import AnimalDetailPanel from './components/AnimalDetailPanel';
import HerdPanel from './components/HerdPanel';
import { ChevronLeftIcon, ChevronRightIcon } from './components/Icons';
import Login from './components/Login';
import BottomNav from './components/BottomNav';

const useIsMobile = (breakpoint = 768) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth < breakpoint);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < breakpoint);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [breakpoint]);

  return isMobile;
};


const App: React.FC = () => {
  const { animals, herds } = useAnimalData();
  const [selectedAnimalId, setSelectedAnimalId] = useState<number | null>(null);
  const [isLeftPanelCollapsed, setIsLeftPanelCollapsed] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [mobileView, setMobileView] = useState<'dashboard' | 'map' | 'chat'>('dashboard');
  
  const isMobile = useIsMobile();
  
  const HERD_AREA_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'];

  const handleSelectAnimal = (animal: Animal) => {
    setSelectedAnimalId(animal.id);
    if (isMobile) {
      setMobileView('dashboard'); // Switch to dashboard to show details on mobile
    } else if (isLeftPanelCollapsed) {
      setIsLeftPanelCollapsed(false);
    }
  };

  const handleCloseDetail = () => {
    setSelectedAnimalId(null);
  };

  const toggleLeftPanel = () => {
    setIsLeftPanelCollapsed(!isLeftPanelCollapsed);
  };
  
  const handleLogout = () => {
    setIsAuthenticated(false);
    setSelectedAnimalId(null);
    sessionStorage.removeItem('chatHistory'); // Limpa o histórico do chat ao sair
  };

  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => setIsAuthenticated(true)} />;
  }
  
  const selectedAnimal = selectedAnimalId ? animals.find(a => a.id === selectedAnimalId) : null;

  // Mobile View
  if (isMobile) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', fontFamily: 'sans-serif', backgroundColor: '#f0f2f5', color: '#333' }}>
        <header style={{ padding: '0.75rem 1rem', flexShrink: 0, display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', borderBottom: '1px solid #ddd', zIndex: 10 }}>
          <h1 style={{ margin: 0, fontSize: '1.2rem' }}>R-IoT</h1>
           <button
                onClick={handleLogout}
                aria-label="Sair da aplicação"
                style={{
                    background: 'transparent',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    padding: '0.3rem 0.6rem',
                    cursor: 'pointer',
                    fontSize: '0.8rem',
                    color: '#dc3545',
                }}
              >
                Sair
              </button>
        </header>

        <main style={{ flex: 1, overflow: 'hidden', position: 'relative' }}>
          {mobileView === 'dashboard' && (
             <div style={{ height: '100%', overflowY: 'auto', padding: '1rem' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <StatsPanel animals={animals} />
                  {selectedAnimal ? (
                     <AnimalDetailPanel animal={selectedAnimal} herds={herds} onClose={handleCloseDetail} />
                  ) : (
                    <HerdPanel herds={herds} animals={animals} herdColors={HERD_AREA_COLORS} />
                  )}
                </div>
            </div>
          )}
          {mobileView === 'map' && (
             <div style={{ height: '100%', width: '100%'}}>
              <MapPanel animals={animals} herds={herds} onSelectAnimal={handleSelectAnimal} selectedAnimal={selectedAnimal} herdColors={HERD_AREA_COLORS} onDeselectAnimal={handleCloseDetail} />
            </div>
          )}
          {mobileView === 'chat' && (
            <div style={{ height: '100%', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ChatPanel animals={animals} herds={herds} selectedAnimal={selectedAnimal} isMobile={true} />
            </div>
          )}
        </main>

        <BottomNav activeView={mobileView} setView={setMobileView} />
      </div>
    );
  }

  // Desktop View
  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif', backgroundColor: '#f0f2f5', color: '#333' }}>
      <div style={{ position: 'relative', display: 'flex', zIndex: 10 }}>
        <div style={{
          width: isLeftPanelCollapsed ? '0px' : '400px',
          minWidth: isLeftPanelCollapsed ? '0px' : '400px',
          transition: 'width 0.3s ease-in-out, min-width 0.3s ease-in-out',
          overflow: 'hidden',
          backgroundColor: 'white',
          borderRight: '1px solid #ddd',
          display: 'flex',
          flexDirection: 'column',
        }}>
          <div style={{
            width: '400px',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            boxSizing: 'border-box',
          }}>
            <header style={{ padding: '1rem', flexShrink: 0, display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eee' }}>
              <h1 style={{ margin: 0, fontSize: '1.5rem', whiteSpace: 'nowrap' }}>R-IoT Dashboard</h1>
              <button
                onClick={handleLogout}
                aria-label="Sair da aplicação"
                style={{
                    background: 'transparent',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    padding: '0.4rem 0.8rem',
                    cursor: 'pointer',
                    fontSize: '0.9rem',
                    color: '#dc3545',
                    fontWeight: 'bold',
                    transition: 'all 0.2s'
                }}
                onMouseOver={(e) => {
                    e.currentTarget.style.backgroundColor = '#dc3545';
                    e.currentTarget.style.color = '#fff';
                    e.currentTarget.style.borderColor = '#dc3545';
                }}
                onMouseOut={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                    e.currentTarget.style.color = '#dc3545';
                    e.currentTarget.style.borderColor = '#ddd';
                }}
              >
                Sair
              </button>
            </header>

            <div style={{ flex: 1, minHeight: 0, padding: '1rem', boxSizing: 'border-box', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ flexShrink: 0 }}>
                {selectedAnimal ? (
                    <AnimalDetailPanel animal={selectedAnimal} herds={herds} onClose={handleCloseDetail} />
                ) : (
                    <HerdPanel herds={herds} animals={animals} herdColors={HERD_AREA_COLORS} />
                )}
              </div>
              <div style={{ marginTop: 'auto' }}>
                <ChatPanel animals={animals} herds={herds} selectedAnimal={selectedAnimal} isMobile={false} />
              </div>
            </div>
          </div>
        </div>
        <button
          onClick={toggleLeftPanel}
          aria-label={isLeftPanelCollapsed ? "Expandir painel" : "Minimizar painel"}
          style={{
            position: 'absolute',
            top: '50%',
            left: isLeftPanelCollapsed ? '5px' : '388px',
            transform: 'translateY(-50%)',
            zIndex: 1,
            width: '24px',
            height: '24px',
            borderRadius: '50%',
            border: '1px solid #ddd',
            backgroundColor: 'white',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            transition: 'left 0.3s ease-in-out',
          }}
        >
          {isLeftPanelCollapsed ? <ChevronRightIcon /> : <ChevronLeftIcon />}
        </button>
      </div>

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1rem', gap: '1rem', position: 'relative' }}>
        <div style={{ flexShrink: 0 }}>
          <StatsPanel animals={animals} />
        </div>
        <div style={{ flex: 1, minHeight: 0, position: 'relative' }}>
          <MapPanel animals={animals} herds={herds} onSelectAnimal={handleSelectAnimal} selectedAnimal={selectedAnimal} herdColors={HERD_AREA_COLORS} onDeselectAnimal={handleCloseDetail} />
        </div>
      </main>
    </div>
  );
};

export default App;