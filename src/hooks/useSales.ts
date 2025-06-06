import { useState, useEffect } from 'react';
import { message } from 'antd';
import { odooService, Sale, PaginatedResponse } from '../services/odooService';

export interface UseSalesReturn {
  sales: Sale[];
  loading: boolean;
  error: string | null;
  totalSales: number;
  currentPage: number;
  pageSize: number;
  searchTerm: string;
  setCurrentPage: (page: number) => void;
  setPageSize: (size: number) => void;
  setSearchTerm: (term: string) => void;
  refreshSales: () => Promise<void>;
  createSale: (saleData: Omit<Sale, 'id'>) => Promise<boolean>;
  updateSale: (id: number, saleData: Partial<Sale>) => Promise<boolean>;
  deleteSale: (id: number) => Promise<boolean>;
  getSaleById: (id: number) => Promise<Sale | null>;
}

export const useSales = (): UseSalesReturn => {
  const [sales, setSales] = useState<Sale[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [totalSales, setTotalSales] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchSales = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response: PaginatedResponse<Sale> = await odooService.getSales({
        page: currentPage,
        limit: pageSize,
        search: searchTerm || undefined
      });
      
      setSales(response.data);
      setTotalSales(response.total);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al cargar ventas';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error fetching sales:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshSales = async () => {
    await fetchSales();
  };

  const createSale = async (saleData: Omit<Sale, 'id'>): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.createSale(saleData);
      message.success('Venta creada exitosamente');
      await fetchSales(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al crear venta';
      message.error(errorMessage);
      console.error('Error creating sale:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const updateSale = async (id: number, saleData: Partial<Sale>): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.updateSale(id, saleData);
      message.success('Venta actualizada exitosamente');
      await fetchSales(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al actualizar venta';
      message.error(errorMessage);
      console.error('Error updating sale:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const deleteSale = async (id: number): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.deleteSale(id);
      message.success('Venta eliminada exitosamente');
      await fetchSales(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al eliminar venta';
      message.error(errorMessage);
      console.error('Error deleting sale:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const getSaleById = async (id: number): Promise<Sale | null> => {
    try {
      setLoading(true);
      const sale = await odooService.getSale(id);
      return sale;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener venta';
      message.error(errorMessage);
      console.error('Error fetching sale by id:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Effect to fetch sales when dependencies change
  useEffect(() => {
    fetchSales();
  }, [currentPage, pageSize, searchTerm]);

  // Reset to first page when search term changes
  useEffect(() => {
    if (searchTerm !== '') {
      setCurrentPage(1);
    }
  }, [searchTerm]);

  return {
    sales,
    loading,
    error,
    totalSales,
    currentPage,
    pageSize,
    searchTerm,
    setCurrentPage,
    setPageSize,
    setSearchTerm,
    refreshSales,
    createSale,
    updateSale,
    deleteSale,
    getSaleById
  };
};