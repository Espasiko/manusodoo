import React from 'react';
import { Card, Typography, Space, Tabs } from 'antd';
import { BarChartOutlined, LineChartOutlined, PieChartOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { TabPane } = Tabs;

const Reports: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <Title level={3} style={{ marginBottom: '24px', color: '#fff' }}>Informes</Title>
      
      <Tabs defaultActiveKey="1" style={{ color: '#fff' }}>
        <TabPane 
          tab={<span><BarChartOutlined /> Ventas</span>}
          key="1"
        >
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Title level={4} style={{ color: '#fff' }}>Informe de Ventas</Title>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div style={{ height: '300px', background: '#141414', borderRadius: '4px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de ventas por mes</Typography.Text>
              </div>
              <div style={{ height: '300px', background: '#141414', borderRadius: '4px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de ventas por categoría</Typography.Text>
              </div>
            </Space>
          </Card>
        </TabPane>
        
        <TabPane 
          tab={<span><LineChartOutlined /> Inventario</span>}
          key="2"
        >
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Title level={4} style={{ color: '#fff' }}>Informe de Inventario</Title>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div style={{ height: '300px', background: '#141414', borderRadius: '4px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de niveles de stock</Typography.Text>
              </div>
              <div style={{ height: '300px', background: '#141414', borderRadius: '4px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de rotación de inventario</Typography.Text>
              </div>
            </Space>
          </Card>
        </TabPane>
        
        <TabPane 
          tab={<span><PieChartOutlined /> Clientes</span>}
          key="3"
        >
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Title level={4} style={{ color: '#fff' }}>Informe de Clientes</Title>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div style={{ height: '300px', background: '#141414', borderRadius: '4px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de clientes por región</Typography.Text>
              </div>
              <div style={{ height: '300px', background: '#141414', borderRadius: '4px', padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de valor de cliente</Typography.Text>
              </div>
            </Space>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default Reports;
