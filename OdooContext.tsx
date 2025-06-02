import React, { createContext, useContext, useState, ReactNode } from 'react';
import OdooClient from './odooClient';
import { odooService } from './odooService';

interface OdooContextType {
  client: OdooClient;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const OdooContext = createContext<OdooContextType | undefined>(undefined);

interface OdooProviderProps {
  children: ReactNode;
}

export const OdooProvider: React.FC<OdooProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const client = new OdooClient();

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const success = await odooService.login(username, password);
      setIsAuthenticated(success);
      return success;
    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      return false;
    }
  };

  const logout = () => {
    odooService.logout();
    setIsAuthenticated(false);
  };

  return (
    <OdooContext.Provider value={{ client, isAuthenticated, login, logout }}>
      {children}
    </OdooContext.Provider>
  );
};

export const useOdoo = (): OdooContextType => {
  const context = useContext(OdooContext);
  if (!context) {
    throw new Error('useOdoo debe ser utilizado dentro de un OdooProvider');
  }
  return context;
};
