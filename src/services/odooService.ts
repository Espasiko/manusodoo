import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Extender AxiosRequestConfig para incluir la propiedad _retry
interface ExtendedAxiosRequestConfig extends AxiosRequestConfig {
  _retry?: boolean;
}

// TypeScript interfaces mejoradas
export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  address: string;
  total_purchases: number;
}

export interface Provider {
  id: number;
  name: string;
  tax_calculation_method: string;
  discount_type: string;
  payment_term: string;
  incentive_rules?: string;
  status: string;
}

export interface Product {
  id: number;
  name: string;
  code: string;
  category: string;
  price: number;
  stock: number;
  image_url: string;
}

export interface Sale {
  id: number;
  customer_id: number;
  customer_name: string;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  total: number;
  date: string;
  status: string;
}

export interface InventoryItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  location: string;
  last_updated: string;
}

export interface CategoryData {
  name: string;
  percentage: number;
}

export interface DashboardStats {
  total_products: number;
  total_sales: number;
  total_customers: number;
  pending_orders: number;
  low_stock_products: number;
  monthly_revenue: number;
  top_selling_product: string;
  recent_sales: Array<{
    id: number;
    customer_name: string;
    product_name: string;
    total: number;
    date: string;
  }>;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface ApiError {
  message: string;
  status: number;
  details?: any;
}

export interface SessionResponse {
  uid: number;
  username: string;
  name: string;
  session_id: string;
  db: string;
}

class OdooService {
  private apiClient: AxiosInstance;
  private token: string | null = null;
  private isAuthenticated: boolean = false;
  private refreshPromise: Promise<string> | null = null;

  constructor() {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    // Crear instancia de axios con configuración base
    this.apiClient = axios.create({
      baseURL: apiUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Configurar interceptores
    this.setupInterceptors();
    
    // Cargar token desde localStorage
    this.loadTokenFromStorage();
  }

  private setupInterceptors(): void {
    // Interceptor de request - agregar token automáticamente
    this.apiClient.interceptors.request.use(
      (config: AxiosRequestConfig) => {
        if (this.token && config.headers) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        
        // Log de requests en desarrollo
        if (import.meta.env.DEV) {
          console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        }
        
        return config;
      },
      (error: AxiosError) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Interceptor de response - manejo de errores y refresh token
    this.apiClient.interceptors.response.use(
      (response: AxiosResponse) => {
        // Log de responses exitosas en desarrollo
        if (import.meta.env.DEV) {
          console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        }
        return response;
      },
      async (error: AxiosError) => {
        const originalRequest = error.config as ExtendedAxiosRequestConfig;
        
        // Manejo de error 401 - token expirado
        if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            // Intentar refrescar el token
            await this.refreshAuthToken();
            
            // Reintentar la request original
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${this.token}`;
            }
            
            return this.apiClient(originalRequest);
          } catch (refreshError) {
            // Si el refresh falla, logout
            this.logout();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        // Log de errores
        console.error('❌ API Error:', {
          status: error.response?.status,
          message: error.response?.data?.detail || error.message,
          url: error.config?.url
        });
        
        return Promise.reject(this.formatError(error));
      }
    );
  }

  private formatError(error: AxiosError): ApiError {
    return {
      message: error.response?.data?.detail || error.message || 'Error desconocido',
      status: error.response?.status || 500,
      details: error.response?.data
    };
  }

  private loadTokenFromStorage(): void {
    const storedToken = localStorage.getItem('odoo_token');
    if (storedToken) {
      this.token = storedToken;
      this.isAuthenticated = true;
    }
  }

  private saveTokenToStorage(token: string): void {
    localStorage.setItem('odoo_token', token);
    this.token = token;
    this.isAuthenticated = true;
  }

  private clearTokenFromStorage(): void {
    localStorage.removeItem('odoo_token');
    this.token = null;
    this.isAuthenticated = false;
  }

  private async refreshAuthToken(): Promise<string> {
    // Evitar múltiples requests de refresh simultáneos
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = this.performTokenRefresh();
    
    try {
      const newToken = await this.refreshPromise;
      return newToken;
    } finally {
      this.refreshPromise = null;
    }
  }

  private async performTokenRefresh(): Promise<string> {
    // En una implementación real, aquí se haría el refresh del token
    // Por ahora, simplemente lanzamos un error para forzar re-login
    throw new Error('Token refresh not implemented');
  }

  // Métodos públicos
  async login(username: string, password: string): Promise<boolean> {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await this.apiClient.post('/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.data.access_token) {
        this.saveTokenToStorage(response.data.access_token);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error en el servicio de login:', error);
      return false;
    }
  }

  logout(): void {
    this.clearTokenFromStorage();
  }

  isLoggedIn(): boolean {
    return this.isAuthenticated && !!this.token;
  }

  async getSession(): Promise<SessionResponse> {
    const response = await this.apiClient.get<SessionResponse>('/api/v1/auth/session');
    return response.data;
  }

  // Métodos de productos
  async getProducts(params: { page: number; limit: number; search?: string }): Promise<PaginatedResponse<Product>> {
    const response = await this.apiClient.get<PaginatedResponse<Product>>('/api/v1/products', {
      params
    });
    return response.data;
  }

  async getProduct(id: number): Promise<Product> {
    const response = await this.apiClient.get<Product>(`/api/v1/products/${id}`);
    return response.data;
  }

  async createProduct(product: Omit<Product, 'id'>): Promise<Product> {
    const response = await this.apiClient.post<Product>('/api/v1/products', product);
    return response.data;
  }

  async updateProduct(id: number, product: Partial<Product>): Promise<Product> {
    const response = await this.apiClient.put<Product>(`/api/v1/products/${id}`, product);
    return response.data;
  }

  async deleteProduct(id: number): Promise<void> {
    await this.apiClient.delete(`/api/v1/products/${id}`);
  }

  // Métodos de proveedores
  async getProviders(params: { page: number; limit: number; search?: string }): Promise<PaginatedResponse<Provider>> {
    const response = await this.apiClient.get<PaginatedResponse<Provider>>('/api/v1/providers', {
      params
    });
    return response.data;
  }

  async getProvider(id: number): Promise<Provider> {
    const response = await this.apiClient.get<Provider>(`/api/v1/providers/${id}`);
    return response.data;
  }

  async createProvider(provider: Omit<Provider, 'id'>): Promise<Provider> {
    const response = await this.apiClient.post<Provider>('/api/v1/providers', provider);
    return response.data;
  }

  async updateProvider(id: number, provider: Partial<Provider>): Promise<Provider> {
    const response = await this.apiClient.put<Provider>(`/api/v1/providers/${id}`, provider);
    return response.data;
  }

  async deleteProvider(id: number): Promise<void> {
    await this.apiClient.delete(`/api/v1/providers/${id}`);
  }

  // Métodos de inventario
  async getInventory(params: { page: number; limit: number; search?: string }): Promise<PaginatedResponse<InventoryItem>> {
    const response = await this.apiClient.get<PaginatedResponse<InventoryItem>>('/api/v1/inventory', {
      params
    });
    return response.data;
  }

  async getInventoryItem(id: number): Promise<InventoryItem> {
    const response = await this.apiClient.get<InventoryItem>(`/api/v1/inventory/${id}`);
    return response.data;
  }

  async createInventoryItem(item: Omit<InventoryItem, 'id'>): Promise<InventoryItem> {
    const response = await this.apiClient.post<InventoryItem>('/api/v1/inventory', item);
    return response.data;
  }

  async updateInventoryItem(id: number, item: Partial<InventoryItem>): Promise<InventoryItem> {
    const response = await this.apiClient.put<InventoryItem>(`/api/v1/inventory/${id}`, item);
    return response.data;
  }

  async deleteInventoryItem(id: number): Promise<void> {
    await this.apiClient.delete(`/api/v1/inventory/${id}`);
  }

  // Métodos de ventas
  async getSales(params: { page: number; limit: number; search?: string }): Promise<PaginatedResponse<Sale>> {
    const response = await this.apiClient.get<PaginatedResponse<Sale>>('/api/v1/sales', {
      params
    });
    return response.data;
  }

  async getSale(id: number): Promise<Sale> {
    const response = await this.apiClient.get<Sale>(`/api/v1/sales/${id}`);
    return response.data;
  }

  async createSale(sale: Omit<Sale, 'id'>): Promise<Sale> {
    const response = await this.apiClient.post<Sale>('/api/v1/sales', sale);
    return response.data;
  }

  async updateSale(id: number, sale: Partial<Sale>): Promise<Sale> {
    const response = await this.apiClient.put<Sale>(`/api/v1/sales/${id}`, sale);
    return response.data;
  }

  async deleteSale(id: number): Promise<void> {
    await this.apiClient.delete(`/api/v1/sales/${id}`);
  }

  // Métodos de clientes
  async getCustomers(params: { page: number; limit: number; search?: string }): Promise<PaginatedResponse<Customer>> {
    const response = await this.apiClient.get<PaginatedResponse<Customer>>('/api/v1/customers', {
      params
    });
    return response.data;
  }

  async getCustomerById(id: number): Promise<Customer> {
    const response = await this.apiClient.get<Customer>(`/api/v1/customers/${id}`);
    return response.data;
  }

  async createCustomer(customer: Omit<Customer, 'id'>): Promise<Customer> {
    const response = await this.apiClient.post<Customer>('/api/v1/customers', customer);
    return response.data;
  }

  async updateCustomer(id: number, customer: Partial<Customer>): Promise<Customer> {
    const response = await this.apiClient.put<Customer>(`/api/v1/customers/${id}`, customer);
    return response.data;
  }

  async deleteCustomer(id: number): Promise<void> {
    await this.apiClient.delete(`/api/v1/customers/${id}`);
  }

  // Métodos del dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await this.apiClient.get<DashboardStats>('/api/v1/dashboard/stats');
    return response.data;
  }

  async getCategories(): Promise<{ categories: Array<{ id: number; name: string; count: number }> }> {
    const response = await this.apiClient.get('/api/v1/dashboard/categories');
    return response.data;
  }

  async getDashboardCategories(): Promise<CategoryData[]> {
    const response = await this.apiClient.get<{ categories: CategoryData[] }>('/api/v1/dashboard/categories');
    return response.data.categories;
  }
}

// Exportar instancia singleton
export const odooService = new OdooService();

// Exportar clase para testing
export { OdooService };
