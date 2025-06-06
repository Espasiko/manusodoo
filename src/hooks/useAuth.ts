import { useState, useEffect } from 'react';
import { message } from 'antd';
import { odooService, SessionResponse } from '../services/odooService';

export interface UseAuthReturn {
  isAuthenticated: boolean;
  user: any | null;
  sessionId: string | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  checkSession: () => Promise<void>;
  refreshSession: () => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already authenticated on component mount
  useEffect(() => {
    if (odooService.isLoggedIn()) {
      checkSession();
    }
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await odooService.login(username, password);
      
      if (response) {
        // Update authentication state
        setIsAuthenticated(true);
        setUser({ username }); // You might want to get more user info from the session
        
        // Get session info
        await checkSession();
        
        message.success('Inicio de sesión exitoso');
        return true;
      } else {
        throw new Error('Error en el inicio de sesión');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al iniciar sesión';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error during login:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    try {
      // Clear token using odooService
      odooService.logout();
      
      // Reset authentication state
      setIsAuthenticated(false);
      setUser(null);
      setSessionId(null);
      setError(null);
      
      message.success('Sesión cerrada exitosamente');
    } catch (err) {
      console.error('Error during logout:', err);
      message.error('Error al cerrar sesión');
    }
  };

  const checkSession = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const sessionData: SessionResponse = await odooService.getSession();
      
      if (sessionData.uid) {
        setIsAuthenticated(true);
        setUser({ 
          uid: sessionData.uid,
          username: sessionData.username,
          name: sessionData.name 
        });
        setSessionId(sessionData.session_id);
      } else {
        // Session is not valid, clear authentication
        logout();
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al verificar sesión';
      setError(errorMessage);
      console.error('Error checking session:', err);
      
      // If session check fails, assume user is not authenticated
      logout();
    } finally {
      setLoading(false);
    }
  };

  const refreshSession = async () => {
    await checkSession();
  };

  return {
    isAuthenticated,
    user,
    sessionId,
    loading,
    error,
    login,
    logout,
    checkSession,
    refreshSession
  };
};