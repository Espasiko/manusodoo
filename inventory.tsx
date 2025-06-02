import React from 'react';
import { Table, Card, Typography, Space, Button, Tag } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';

const { Title } = Typography;

const Inventory: React.FC = () => {
  // Datos de ejemplo para la tabla de inventario
  const inventory = [
    {
      id: 1,
      product: 'Refrigerador Samsung RT38K5982BS',
      code: 'REF-SAM-001',
      location: 'Almacén Principal',
      quantity: 12,
      reserved: 2,
    },
    {
      id: 2,
      product: 'Lavadora LG F4WV5012S0W',
      code: 'LAV-LG-002',
      location: 'Almacén Principal',
      quantity: 8,
      reserved: 1,
    },
    {
      id: 3,
      product: 'Televisor Sony KD-55X80J',
      code: 'TV-SONY-003',
      location: 'Almacén Secundario',
      quantity: 5,
      reserved: 0,
    },
    {
      id: 4,
      product: 'Horno Balay 3HB4331X0',
      code: 'HOR-BAL-004',
      location: 'Almacén Principal',
      quantity: 15,
      reserved: 3,
    },
    {
      id: 5,
      product: 'Microondas Bosch BFL523MS0',
      code: 'MIC-BOS-005',
      location: 'Almacén Secundario',
      quantity: 20,
      reserved: 5,
    },
  ];

  const columns = [
    {
      title: 'Código',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: 'Producto',
      dataIndex: 'product',
      key: 'product',
    },
    {
      title: 'Ubicación',
      dataIndex: 'location',
      key: 'location',
      render: (text: string) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: 'Cantidad',
      dataIndex: 'quantity',
      key: 'quantity',
    },
    {
      title: 'Reservado',
      dataIndex: 'reserved',
      key: 'reserved',
    },
    {
      title: 'Disponible',
      key: 'available',
      render: (record: any) => {
        const available = record.quantity - record.reserved;
        let color = 'green';
        if (available < 5) {
          color = 'red';
        } else if (available < 10) {
          color = 'orange';
        }
        return <Tag color={color}>{available}</Tag>;
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
        <Title level={3} style={{ margin: 0, color: '#fff' }}>Inventario</Title>
        <Button type="primary" icon={<PlusOutlined />}>
          Ajustar Stock
        </Button>
      </Space>
      
      <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
        <Table 
          columns={columns} 
          dataSource={inventory} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default Inventory;
