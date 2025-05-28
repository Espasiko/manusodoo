import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Typography, Progress, Space } from 'antd';
import { ShoppingOutlined, InboxOutlined, ShoppingCartOutlined, UserOutlined } from '@ant-design/icons';
import { odooService, DashboardStats } from './odooService';

const { Title } = Typography;

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalProducts: 0,
    lowStock: 0,
    salesThisMonth: 0,
    activeCustomers: 0,
    topCategories: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Try to login first with default credentials
        const loginSuccess = await odooService.login('admin', 'admin_password_secure');
        if (loginSuccess) {
          const dashboardStats = await odooService.getDashboardStats();
          setStats(dashboardStats);
        } else {
          throw new Error('Authentication failed');
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Fallback to default data if API fails
        setStats({
          totalProducts: 248,
          lowStock: 15,
          salesThisMonth: 42500,
          activeCustomers: 156,
          topCategories: [
            { name: 'Refrigeradores', percentage: 28 },
            { name: 'Lavadoras', percentage: 22 },
            { name: 'Televisores', percentage: 18 },
            { name: 'Hornos', percentage: 12 },
          ],
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <Title level={3} style={{ marginBottom: '24px', color: '#fff' }}>Dashboard</Title>
      
      {/* Tarjetas de estadísticas */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Total Productos"
              value={stats.totalProducts}
              valueStyle={{ color: '#1890ff' }}
              prefix={<ShoppingOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Productos con Stock Bajo"
              value={stats.lowStock}
              valueStyle={{ color: '#ff4d4f' }}
              prefix={<InboxOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Ventas del Mes"
              value={stats.salesThisMonth}
              valueStyle={{ color: '#52c41a' }}
              prefix={<ShoppingCartOutlined />}
              suffix="€"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Clientes Activos"
              value={stats.activeCustomers}
              valueStyle={{ color: '#722ed1' }}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Gráficos y datos adicionales */}
      <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
        <Col xs={24} lg={12}>
          <Card title="Evolución de Ventas" style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            {/* Aquí iría un gráfico de líneas con Chart.js o similar */}
            <div style={{ height: '200px', background: '#141414', borderRadius: '4px', padding: '16px' }}>
              {/* Placeholder para el gráfico */}
              <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de evolución de ventas</Typography.Text>
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Productos por Categoría" style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              {stats.topCategories.map((category, index) => (
                <div key={index}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography.Text>{category.name}</Typography.Text>
                    <Typography.Text>{category.percentage}%</Typography.Text>
                  </div>
                  <Progress percent={category.percentage} showInfo={false} strokeColor="#1890ff" />
                </div>
              ))}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
