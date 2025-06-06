import { useState, useEffect } from 'react';
import { message } from 'antd';
import { odooService, DashboardStats, CategoryData } from '../services/odooService';

export interface UseDashboardReturn {
  stats: DashboardStats | null;
  categories: CategoryData[];
  loading: boolean;
  error: string | null;
  refreshStats: () => Promise<void>;
  refreshCategories: () => Promise<void>;
  refreshAll: () => Promise<void>;
}

export const useDashboard = (): UseDashboardReturn => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [categories, setCategories] = useState<CategoryData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const statsData = await odooService.getDashboardStats();
      setStats(statsData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al cargar estadísticas del dashboard';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error fetching dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const categoriesData = await odooService.getDashboardCategories();
      setCategories(categoriesData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al cargar categorías del dashboard';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error fetching dashboard categories:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshStats = async () => {
    await fetchStats();
  };

  const refreshCategories = async () => {
    await fetchCategories();
  };

  const refreshAll = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch both stats and categories in parallel
      const [statsData, categoriesData] = await Promise.all([
        odooService.getDashboardStats(),
        odooService.getDashboardCategories()
      ]);
      
      setStats(statsData);
      setCategories(categoriesData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al cargar datos del dashboard';
      setError(errorMessage);
      message.error(errorMessage);
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  // Effect to fetch dashboard data on component mount
  useEffect(() => {
    refreshAll();
  }, []);

  return {
    stats,
    categories,
    loading,
    error,
    refreshStats,
    refreshCategories,
    refreshAll
  };
};