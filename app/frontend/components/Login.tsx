import React, { useState } from 'react';

interface LoginProps {
  onLoginSuccess: () => void;
}

const CORRECT_PASSWORD = 'riot2025';

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === CORRECT_PASSWORD) {
      setError('');
      onLoginSuccess();
    } else {
      setError('Senha incorreta. Tente novamente.');
      setPassword('');
    }
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      fontFamily: 'sans-serif',
      backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('https://images.pexels.com/photos/162240/bull-calf-heifer-ko-162240.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }}>
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.15)',
        backdropFilter: 'blur(15px)',
        padding: '2.5rem 2rem',
        borderRadius: '12px',
        boxShadow: '0 4px 30px rgba(0,0,0,0.1)',
        width: '100%',
        maxWidth: '380px',
        textAlign: 'center',
        border: '1px solid rgba(255, 255, 255, 0.3)',
      }}>
        <h1 style={{ margin: '0 0 0.5rem 0', fontSize: '2rem', color: '#fff', textShadow: '0 2px 4px rgba(0,0,0,0.5)' }}>
          R-IoT Login
        </h1>
        <p style={{ margin: '0 0 2rem 0', color: '#eee', textShadow: '0 1px 2px rgba(0,0,0,0.5)' }}>
          Monitoramento Rural Inteligente
        </p>
        <form onSubmit={handleSubmit} noValidate>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Senha"
            aria-label="Senha"
            autoComplete="current-password"
            style={{
              width: '100%',
              padding: '0.8rem 1rem',
              marginBottom: '1rem',
              border: `1px solid ${error ? 'rgba(255, 100, 100, 0.7)' : 'rgba(255, 255, 255, 0.4)'}`,
              borderRadius: '8px',
              fontSize: '1rem',
              boxSizing: 'border-box',
              backgroundColor: 'rgba(0, 0, 0, 0.2)',
              color: '#fff',
              outline: 'none',
              transition: 'border-color 0.2s',
            }}
          />
          {error && <p style={{ color: '#ffb3b3', fontSize: '0.875rem', margin: '-0.5rem 0 1rem 0', fontWeight: 'bold' }}>{error}</p>}
          <button
            type="submit"
            style={{
              width: '100%',
              padding: '0.8rem',
              border: 'none',
              borderRadius: '8px',
              backgroundColor: '#0d6efd',
              color: 'white',
              fontSize: '1rem',
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'background-color 0.2s',
            }}
            onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#0b5ed7')}
            onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#0d6efd')}
          >
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;