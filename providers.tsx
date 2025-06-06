import React, { useState, useEffect } from 'react';
import { Table, Card, Typography, Space, Button, Tag, Form, Input, Select, Modal, message } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined, TeamOutlined } from '@ant-design/icons';
import { odooService, Provider } from './odooService';

const { Title } = Typography;
const { Option } = Select;

// La interfaz Provider ahora se importa desde odooService.ts

const Providers: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingProvider, setEditingProvider] = useState<Provider | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchProviders();
  }, []);

  const fetchProviders = async () => {
    try {
      setLoading(true);
      // Obtener datos de Odoo
      const providersData = await odooService.getProviders();
      
      if (providersData && providersData.length > 0) {
        setProviders(providersData);
      } else {
        setProviders([]);
        message.error('No se pudieron obtener proveedores del backend.');
      }
    } catch (error) {
      console.error('Error fetching providers:', error);
      message.error('Error al cargar los proveedores');
      setProviders([]);
    } finally {
      setLoading(false);
    }
  };

  const showModal = (provider?: Provider) => {
    setEditingProvider(provider || null);
    if (provider) {
      form.setFieldsValue(provider);
    } else {
      form.resetFields();
    }
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setEditingProvider(null);
    form.resetFields();
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingProvider) {
        // Actualizar proveedor existente
        const result = await odooService.updateProvider(editingProvider.id, values);
        if (result) {
          // Actualizar la lista local
          const updatedProviders = providers.map(p => 
            p.id === editingProvider.id ? { ...p, ...values } : p
          );
          setProviders(updatedProviders);
          message.success('Proveedor actualizado correctamente');
        } else {
          throw new Error('Error al actualizar el proveedor');
        }
      } else {
        // Crear nuevo proveedor
        const providerData = {
          ...values,
          status: 'Activo',
        };
        const result = await odooService.createProvider(providerData);
        if (result) {
          // Añadir el nuevo proveedor a la lista local
          setProviders([...providers, result]);
          message.success('Proveedor creado correctamente');
        } else {
          throw new Error('Error al crear el proveedor');
        }
      }
      handleCancel();
    } catch (error) {
      console.error('Error saving provider:', error);
      message.error('Error al guardar el proveedor');
    }
  };

  const handleDelete = (id: number) => {
    Modal.confirm({
      title: '¿Estás seguro de que quieres eliminar este proveedor?',
      content: 'Esta acción no se puede deshacer.',
      okText: 'Sí, eliminar',
      okType: 'danger',
      cancelText: 'Cancelar',
      onOk: async () => {
        try {
          const success = await odooService.deleteProvider(id);
          if (success) {
            setProviders(providers.filter(p => p.id !== id));
            message.success('Proveedor eliminado correctamente');
          } else {
            throw new Error('Error al eliminar el proveedor');
          }
        } catch (error) {
          console.error('Error deleting provider:', error);
          message.error('Error al eliminar el proveedor');
        }
      },
    });
  };

  const getTaxMethodLabel = (method: string) => {
    switch (method) {
      case 'standard': return 'IVA Estándar (21%)';
      case 'recargo': return 'IVA + Recargo (26.2%)';
      default: return method;
    }
  };

  const getDiscountTypeLabel = (type: string) => {
    switch (type) {
      case 'fixed': return 'Descuento Fijo';
      case 'volume': return 'Por Volumen';
      case 'seasonal': return 'Temporal';
      default: return type;
    }
  };

  const getPaymentTermLabel = (term: string) => {
    switch (term) {
      case 'immediate': return 'Inmediato';
      case '30_days': return '30 Días';
      case '45_days': return '45 Días';
      case '60_days': return '60 Días';
      default: return term;
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <strong>{text}</strong>,
    },
    {
      title: 'Método de Cálculo IVA',
      dataIndex: 'tax_calculation_method',
      key: 'tax_calculation_method',
      render: (method: string) => getTaxMethodLabel(method),
    },
    {
      title: 'Tipo de Descuento',
      dataIndex: 'discount_type',
      key: 'discount_type',
      render: (type: string) => getDiscountTypeLabel(type),
    },
    {
      title: 'Términos de Pago',
      dataIndex: 'payment_term',
      key: 'payment_term',
      render: (term: string) => getPaymentTermLabel(term),
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
      render: (record: Provider) => (
        <Space>
          <Button
            type="primary"
            icon={<EditOutlined />}
            size="small"
            onClick={() => showModal(record)}
          >
            Editar
          </Button>
          <Button
            type="primary"
            danger
            icon={<DeleteOutlined />}
            size="small"
            onClick={() => handleDelete(record.id)}
          >
            Eliminar
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <Title level={3} style={{ margin: 0, color: '#fff' }}>
            <TeamOutlined style={{ marginRight: '8px' }} />
            Gestión de Proveedores
          </Title>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => showModal()}
            size="large"
          >
            Nuevo Proveedor
          </Button>
        </div>
        
        <Table
          columns={columns}
          dataSource={providers}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} de ${total} proveedores`,
          }}
          style={{
            background: '#141414',
          }}
        />
      </Card>

      <Modal
        title={editingProvider ? 'Editar Proveedor' : 'Nuevo Proveedor'}
        open={isModalVisible}
        onCancel={handleCancel}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          style={{ marginTop: '20px' }}
        >
          <Form.Item
            label="Nombre"
            name="name"
            rules={[{ required: true, message: 'Por favor ingresa el nombre del proveedor' }]}
          >
            <Input placeholder="Nombre del proveedor" />
          </Form.Item>

          <Form.Item
            label="Método de Cálculo IVA"
            name="tax_calculation_method"
            rules={[{ required: true, message: 'Por favor selecciona el método de cálculo IVA' }]}
          >
            <Select placeholder="Selecciona el método de cálculo">
              <Option value="standard">IVA Estándar (21%)</Option>
              <Option value="recargo">IVA + Recargo (26.2%)</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Tipo de Descuento"
            name="discount_type"
          >
            <Select placeholder="Selecciona el tipo de descuento">
              <Option value="fixed">Descuento Fijo</Option>
              <Option value="volume">Por Volumen</Option>
              <Option value="seasonal">Temporal</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Términos de Pago"
            name="payment_term"
          >
            <Select placeholder="Selecciona los términos de pago">
              <Option value="immediate">Inmediato</Option>
              <Option value="30_days">30 Días</Option>
              <Option value="45_days">45 Días</Option>
              <Option value="60_days">60 Días</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Reglas de Incentivos"
            name="incentive_rules"
          >
            <Input.TextArea 
              rows={4} 
              placeholder="Descripción de reglas de incentivos y descuentos especiales" 
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={handleCancel}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit">
                {editingProvider ? 'Actualizar' : 'Crear'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Providers;