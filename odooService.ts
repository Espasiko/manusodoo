import axios from 'axios';

// TypeScript interfaces
export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  city: string;
  country: string;
  status: string;
}

export interface Product {
  id: number;
  name: string;
  code: string;
  category: string;
  price: number;
  stock: number;
}

export interface Sale {
  id: number;
  reference: string;
  customer: string;
  date: string;
  total: number;
  status: string;
}

export interface CategoryData {
  name: string;
  percentage: number;
}

export interface DashboardStats {
  totalProducts: number;
  lowStock: number;
  salesThisMonth: number;
  activeCustomers: number;
  topCategories: CategoryData[];
}

class OdooService {
  private apiUrl: string;
  private token: string | null = null;
  private isAuthenticated: boolean = false;

  constructor() {
    this.apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  }

  async login(username: string, password: string): Promise<boolean> {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post(`${this.apiUrl}/token`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.data.access_token) {
        this.token = response.data.access_token;
        this.isAuthenticated = true;
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error en el servicio de login:', error);
      return false;
    }
  }

  logout(): void {
    this.token = null;
    this.isAuthenticated = false;
  }

  private getAuthHeaders() {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json',
    };
  }

  async getProducts(limit: number = 10): Promise<Product[]> {
    try {
      const response = await axios.get(`${this.apiUrl}/api/v1/products`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo productos:', error);
      return [];
    }
  }

  async getInventory(limit: number = 10): Promise<Product[]> {
    try {
      const response = await axios.get(`${this.apiUrl}/api/v1/inventory`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo inventario:', error);
      return [];
    }
  }

  async getSales(limit: number = 10): Promise<Sale[]> {
    try {
      const response = await axios.get(`${this.apiUrl}/api/v1/sales`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo ventas:', error);
      return [];
    }
  }

  async getCustomers(limit: number = 10): Promise<Customer[]> {
    try {
      const response = await axios.get(`${this.apiUrl}/api/v1/customers`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo clientes:', error);
      return [];
    }
  }

  async getDashboardStats(): Promise<DashboardStats> {
    try {
      const response = await axios.get(`${this.apiUrl}/api/v1/dashboard/stats`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo estadísticas del dashboard:', error);
      return {
        totalProducts: 0,
        lowStock: 0,
        salesThisMonth: 0,
        activeCustomers: 0,
        topCategories: []
      };
    }
  }
}

export const odooService = new OdooService();
