import React, { useState, useEffect } from 'react';
import { Table, Card, Typography, Space, Button, Tag } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import { odooService, Sale } from './odooService';

const { Title } = Typography;

const Sales: React.FC = () => {
  const [sales, setSales] = useState<Sale[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSales = async () => {
      try {
        const salesData = await odooService.getSales();
        setSales(salesData);
      } catch (error) {
        console.error('Error fetching sales:', error);
        // Fallback to default data if API fails
        setSales([
          {
            id: 1,
            reference: 'S00123',
            customer: 'María García',
            date: '2025-05-20',
            total: 1299.99,
            status: 'Completado',
          },
          {
            id: 2,
            reference: 'S00124',
            customer: 'Juan Pérez',
            date: '2025-05-21',
            total: 849.50,
            status: 'Pendiente',
          },
          {
            id: 3,
            reference: 'S00125',
            customer: 'Ana Martínez',
            date: '2025-05-22',
            total: 1599.99,
            status: 'Completado',
          },
          {
            id: 4,
            reference: 'S00126',
            customer: 'Carlos Rodríguez',
            date: '2025-05-23',
            total: 399.99,
            status: 'Cancelado',
          },
          {
            id: 5,
            reference: 'S00127',
            customer: 'Laura Sánchez',
            date: '2025-05-24',
            total: 749.99,
            status: 'Pendiente',
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchSales();
  }, []);

  const columns = [
    {
      title: 'Referencia',
      dataIndex: 'reference',
      key: 'reference',
    },
    {
      title: 'Cliente',
      dataIndex: 'customer',
      key: 'customer',
    },
    {
      title: 'Fecha',
      dataIndex: 'date',
      key: 'date',
    },
    {
      title: 'Total',
      dataIndex: 'total',
      key: 'total',
      render: (total: number) => `${total.toFixed(2)} €`,
    },
    {
      title: 'Estado',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = 'green';
        if (status === 'Pendiente') {
          color = 'orange';
        } else if (status === 'Cancelado') {
          color = 'red';
        }
        return <Tag color={color}>{status}</Tag>;
      },
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button type="text" icon={<EditOutlined />} />
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <Space style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
        <Title level={3} style={{ margin: 0, color: '#fff' }}>Ventas</Title>
        <Button type="primary" icon={<PlusOutlined />}>
          Nueva Venta
        </Button>
      </Space>
      
      <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
        <Table 
          columns={columns} 
          dataSource={sales} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
          loading={loading}
        />
      </Card>
    </div>
  );
};

export default Sales;
