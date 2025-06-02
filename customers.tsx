import React, { useState, useEffect } from 'react';
import { Table, Card, Typography, Space, Button, Tag } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import { odooService, Customer } from './odooService';

const { Title } = Typography;

const Customers: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const customersData = await odooService.getCustomers();
        setCustomers(customersData);
      } catch (error) {
        console.error('Error fetching customers:', error);
        // Fallback to default data if API fails
        setCustomers([
          {
            id: 1,
            name: 'María García',
            email: 'maria.garcia@example.com',
            phone: '+34 612 345 678',
            city: 'Madrid',
            country: 'España',
            status: 'Activo',
          },
          {
            id: 2,
            name: 'Juan Pérez',
            email: 'juan.perez@example.com',
            phone: '+34 623 456 789',
            city: 'Barcelona',
            country: 'España',
            status: 'Activo',
          },
          {
            id: 3,
            name: 'Ana Martínez',
            email: 'ana.martinez@example.com',
            phone: '+34 634 567 890',
            city: 'Valencia',
            country: 'España',
            status: 'Inactivo',
          },
          {
            id: 4,
            name: 'Carlos Rodríguez',
            email: 'carlos.rodriguez@example.com',
            phone: '+34 645 678 901',
            city: 'Sevilla',
            country: 'España',
            status: 'Activo',
          },
          {
            id: 5,
            name: 'Laura Sánchez',
            email: 'laura.sanchez@example.com',
            phone: '+34 656 789 012',
            city: 'Bilbao',
            country: 'España',
            status: 'Activo',
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  const columns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Teléfono',
      dataIndex: 'phone',
      key: 'phone',
    },
    {
      title: 'Ciudad',
      dataIndex: 'city',
      key: 'city',
    },
    {
      title: 'País',
      dataIndex: 'country',
      key: 'country',
    },
    {
      title: 'Estado',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const color = status === 'Activo' ? 'green' : 'red';
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
        <Title level={3} style={{ margin: 0, color: '#fff' }}>Clientes</Title>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Cliente
        </Button>
      </Space>
      
      <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
        <Table 
          columns={columns} 
          dataSource={customers} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
          loading={loading}
        />
      </Card>
    </div>
  );
};

export default Customers;
