import React from 'react';
import { DashboardIcon, MapIcon, ChatBotIcon } from './Icons';

type MobileView = 'dashboard' | 'map' | 'chat';

interface BottomNavProps {
  activeView: MobileView;
  setView: (view: MobileView) => void;
}

const NavButton = ({
  label,
  icon,
  isActive,
  onClick,
}: {
  label: string;
  icon: React.ReactNode;
  isActive: boolean;
  onClick: () => void;
}) => {
  const activeColor = '#007bff';
  const inactiveColor = '#6c757d';

  return (
    <button
      onClick={onClick}
      style={{
        flex: 1,
        background: 'none',
        border: 'none',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '0.25rem 0',
        color: isActive ? activeColor : inactiveColor,
        cursor: 'pointer',
        gap: '2px'
      }}
    >
      {icon}
      <span style={{ fontSize: '0.7rem', fontWeight: isActive ? 'bold' : 'normal' }}>{label}</span>
    </button>
  );
};

const BottomNav: React.FC<BottomNavProps> = ({ activeView, setView }) => {
  return (
    <nav
      style={{
        display: 'flex',
        height: '60px',
        width: '100%',
        backgroundColor: 'white',
        borderTop: '1px solid #ddd',
        boxShadow: '0 -2px 5px rgba(0,0,0,0.05)',
        flexShrink: 0,
      }}
    >
      <NavButton
        label="Dashboard"
        icon={<DashboardIcon />}
        isActive={activeView === 'dashboard'}
        onClick={() => setView('dashboard')}
      />
      <NavButton
        label="Mapa"
        icon={<MapIcon />}
        isActive={activeView === 'map'}
        onClick={() => setView('map')}
      />
      <NavButton
        label="Chat"
        icon={<ChatBotIcon />}
        isActive={activeView === 'chat'}
        onClick={() => setView('chat')}
      />
    </nav>
  );
};

export default BottomNav;