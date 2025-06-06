import { useState, useEffect } from 'react';
import { message } from 'antd';
import { odooService, InventoryItem, PaginatedResponse } from '../services/odooService';

export interface UseInventoryReturn {
  inventory: InventoryItem[];
  loading: boolean;
  error: string | null;
  totalItems: number;
  currentPage: number;
  pageSize: number;
  searchTerm: string;
  setCurrentPage: (page: number) => void;
  setPageSize: (size: number) => void;
  setSearchTerm: (term: string) => void;
  refreshInventory: () => Promise<void>;
  createInventoryItem: (itemData: Omit<InventoryItem, 'id'>) => Promise<boolean>;
  updateInventoryItem: (id: number, itemData: Partial<InventoryItem>) => Promise<boolean>;
  deleteInventoryItem: (id: number) => Promise<boolean>;
  getInventoryItemById: (id: number) => Promise<InventoryItem | null>;
}

export const useInventory = (): UseInventoryReturn => {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [totalItems, setTotalItems] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchInventory = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response: PaginatedResponse<InventoryItem> = await odooService.getInventory({
        page: currentPage,
        limit: pageSize,
        search: searchTerm || undefined
      });
      
      setInventory(response.data);
      setTotalItems(response.total);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al cargar inventario';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error fetching inventory:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshInventory = async () => {
    await fetchInventory();
  };

  const createInventoryItem = async (itemData: Omit<InventoryItem, 'id'>): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.createInventoryItem(itemData);
      message.success('Artículo de inventario creado exitosamente');
      await fetchInventory(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al crear artículo de inventario';
      message.error(errorMessage);
      console.error('Error creating inventory item:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const updateInventoryItem = async (id: number, itemData: Partial<InventoryItem>): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.updateInventoryItem(id, itemData);
      message.success('Artículo de inventario actualizado exitosamente');
      await fetchInventory(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al actualizar artículo de inventario';
      message.error(errorMessage);
      console.error('Error updating inventory item:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const deleteInventoryItem = async (id: number): Promise<boolean> => {
    try {
      setLoading(true);
      await odooService.deleteInventoryItem(id);
      message.success('Artículo de inventario eliminado exitosamente');
      await fetchInventory(); // Refresh the list
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al eliminar artículo de inventario';
      message.error(errorMessage);
      console.error('Error deleting inventory item:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const getInventoryItemById = async (id: number): Promise<InventoryItem | null> => {
    try {
      setLoading(true);
      const item = await odooService.getInventoryItem(id);
      return item;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener artículo de inventario';
      message.error(errorMessage);
      console.error('Error fetching inventory item by id:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Effect to fetch inventory when dependencies change
  useEffect(() => {
    fetchInventory();
  }, [currentPage, pageSize, searchTerm]);

  // Reset to first page when search term changes
  useEffect(() => {
    if (searchTerm !== '') {
      setCurrentPage(1);
    }
  }, [searchTerm]);

  return {
    inventory,
    loading,
    error,
    totalItems,
    currentPage,
    pageSize,
    searchTerm,
    setCurrentPage,
    setPageSize,
    setSearchTerm,
    refreshInventory,
    createInventoryItem,
    updateInventoryItem,
    deleteInventoryItem,
    getInventoryItemById
  };
};