import React, { useState, useEffect } from 'react';
import { Table, Card, Typography, Space, Button, Tag } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import { odooService, Product } from './odooService';

const { Title } = Typography;

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        // Try to login first with default credentials
        const loginSuccess = await odooService.login('admin', 'admin_password_secure');
        if (loginSuccess) {
          const productsData = await odooService.getProducts();
          setProducts(productsData);
        } else {
          throw new Error('Authentication failed');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        // Fallback to default data if API fails
        setProducts([
          {
            id: 1,
            name: 'Refrigerador Samsung RT38K5982BS',
            code: 'REF-SAM-001',
            category: 'Refrigeradores',
            price: 899.99,
            stock: 12,
          },
          {
            id: 2,
            name: 'Lavadora LG F4WV5012S0W',
            code: 'LAV-LG-002',
            category: 'Lavadoras',
            price: 649.99,
            stock: 8,
          },
          {
            id: 3,
            name: 'Televisor Sony KD-55X80J',
            code: 'TV-SONY-003',
            category: 'Televisores',
            price: 799.99,
            stock: 5,
          },
          {
            id: 4,
            name: 'Horno Balay 3HB4331X0',
            code: 'HOR-BAL-004',
            category: 'Hornos',
            price: 349.99,
            stock: 15,
          },
          {
            id: 5,
            name: 'Microondas Bosch BFL523MS0',
            code: 'MIC-BOS-005',
            category: 'Microondas',
            price: 199.99,
            stock: 20,
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const columns = [
    {
      title: 'Código',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Categoría',
      dataIndex: 'category',
      key: 'category',
      render: (text: string) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: 'Precio',
      dataIndex: 'price',
      key: 'price',
      render: (price: number) => `${price.toFixed(2)} €`,
    },
    {
      title: 'Stock',
      dataIndex: 'stock',
      key: 'stock',
      render: (stock: number) => {
        let color = 'green';
        if (stock < 5) {
          color = 'red';
        } else if (stock < 10) {
          color = 'orange';
        }
        return <Tag color={color}>{stock}</Tag>;
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
        <Title level={3} style={{ margin: 0, color: '#fff' }}>Productos</Title>
        <Button type="primary" icon={<PlusOutlined />}>
          Añadir Producto
        </Button>
      </Space>
      
      <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
        <Table 
          columns={columns} 
          dataSource={products} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
          loading={loading}
        />
      </Card>
    </div>
  );
};

export default Products;
