import { useState, useEffect } from 'react';
import { message } from 'antd';
import { odooService, Customer, PaginatedResponse } from '../services/odooService';

export interface UseCustomersReturn {
  customers: Customer[];
  loading: boolean;
  error: string | null;
  totalCustomers: number;
  currentPage: number;
  pageSize: number;
  searchTerm: string;
  setCurrentPage: (page: number) => void;
  setPageSize: (size: number) => void;
  setSearchTerm: (term: string) => void;
  refreshCustomers: () => Promise<void>;
  createCustomer: (customerData: Omit<Customer, 'id'>) => Promise<boolean>;
  updateCustomer: (id: number, customerData: Partial<Customer>) => Promise<boolean>;
  deleteCustomer: (id: number) => Promise<boolean>;
  getCustomerById: (id: number) => Promise<Customer | null>;
}

export const useCustomers = (): UseCustomersReturn => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [totalCustomers, setTotalCustomers] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response: PaginatedResponse<Customer> = await odooService.getCustomers({
        page: currentPage,
        limit: pageSize,
        search: searchTerm || undefined
      });
      
      setCustomers(response.data);
      setTotalCustomers(response.total);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al cargar clientes';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error fetching customers:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshCustomers = async () => {
    await fetchCustomers();
  };

  const createCustomer = async (customerData: Omit<Customer, 'id'>): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.createCustomer(customerData);
      message.success('Cliente creado exitosamente');
      await fetchCustomers(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al crear cliente';
      message.error(errorMessage);
      console.error('Error creating customer:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const updateCustomer = async (id: number, customerData: Partial<Customer>): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.updateCustomer(id, customerData);
      message.success('Cliente actualizado exitosamente');
      await fetchCustomers(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al actualizar cliente';
      message.error(errorMessage);
      console.error('Error updating customer:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const deleteCustomer = async (id: number): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.deleteCustomer(id);
      message.success('Cliente eliminado exitosamente');
      await fetchCustomers(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al eliminar cliente';
      message.error(errorMessage);
      console.error('Error deleting customer:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const getCustomerById = async (id: number): Promise<Customer | null> => {
    try {
      setLoading(true);
      const customer = await odooService.getCustomerById(id);
      return customer;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener cliente';
      message.error(errorMessage);
      console.error('Error fetching customer by id:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Effect to fetch customers when dependencies change
  useEffect(() => {
    fetchCustomers();
  }, [currentPage, pageSize, searchTerm]);

  // Reset to first page when search term changes
  useEffect(() => {
    if (searchTerm !== '') {
      setCurrentPage(1);
    }
  }, [searchTerm]);

  return {
    customers,
    loading,
    error,
    totalCustomers,
    currentPage,
    pageSize,
    searchTerm,
    setCurrentPage,
    setPageSize,
    setSearchTerm,
    refreshCustomers,
    createCustomer,
    updateCustomer,
    deleteCustomer,
    getCustomerById
  };
};