import React from 'react';
import { ConfigProvider, Layout, theme } from 'antd';
import { darkTheme } from './darkTheme';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Refine } from '@refinedev/core';
import { RefineKbar, RefineKbarProvider } from '@refinedev/kbar';
import routerBindings, {
  NavigateToResource,
  UnsavedChangesNotifier,
} from '@refinedev/react-router-v6';
import dataProvider from '@refinedev/simple-rest';
import { 
  notificationProvider,
  ThemedLayoutV2,
  ErrorComponent,
} from '@refinedev/antd';

// Importar componentes
import Sider from './sider';
import Header from './header';

// Importar páginas
import Dashboard from './dashboard';
import Products from './products';
import Inventory from './inventory';
import Sales from './sales';
import Customers from './customers';
import Reports from './reports';
import Providers from './providers';

// Importar contexto de Odoo
import { OdooProvider } from './OdooContext';

const { Content } = Layout;

const App: React.FC = () => {
  // URL base para la API de Odoo (se configurará en la fase de integración)
  const API_URL = import.meta.env.VITE_ODOO_URL || "http://localhost:8069";

  return (
    <Router>
      <OdooProvider>
        <ConfigProvider theme={darkTheme}>
          <RefineKbarProvider>
            <Refine
              dataProvider={dataProvider(API_URL)}
              notificationProvider={notificationProvider}
              routerProvider={routerBindings}
              resources={[
                {
                  name: "dashboard",
                  list: "/dashboard",
                  meta: {
                    label: "Dashboard",
                    icon: "DashboardOutlined",
                  },
                },
                {
                  name: "products",
                  list: "/products",
                  meta: {
                    label: "Productos",
                    icon: "ShoppingOutlined",
                  },
                },
                {
                  name: "inventory",
                  list: "/inventory",
                  meta: {
                    label: "Inventario",
                    icon: "InboxOutlined",
                  },
                },
                {
                  name: "sales",
                  list: "/sales",
                  meta: {
                    label: "Ventas",
                    icon: "ShoppingCartOutlined",
                  },
                },
                {
                  name: "customers",
                  list: "/customers",
                  meta: {
                    label: "Clientes",
                    icon: "UserOutlined",
                  },
                },
                {
                  name: "reports",
                  list: "/reports",
                  meta: {
                    label: "Informes",
                    icon: "BarChartOutlined",
                  },
                },
                {
                  name: "providers",
                  list: "/providers",
                  meta: {
                    label: "Proveedores",
                    icon: "TeamOutlined",
                  },
                },
              ]}
              options={{
                syncWithLocation: true,
                warnWhenUnsavedChanges: true,
                projectId: "odoo-dashboard",
              }}
            >
              <ThemedLayoutV2 
                Header={() => <Header collapsed={false} setCollapsed={() => {}} />}
                Sider={Sider}
                Title={() => <div style={{ fontSize: "20px", fontWeight: "bold", color: "#fff" }}>Electrodomésticos ERP</div>}
              >
                <Routes>
                  <Route
                    index
                    element={<NavigateToResource resource="dashboard" />}
                  />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/products" element={<Products />} />
                  <Route path="/inventory" element={<Inventory />} />
                  <Route path="/sales" element={<Sales />} />
                  <Route path="/customers" element={<Customers />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="/providers" element={<Providers />} />
                  <Route path="*" element={<ErrorComponent />} />
                </Routes>
              </ThemedLayoutV2>
              <RefineKbar />
              <UnsavedChangesNotifier />
            </Refine>
          </RefineKbarProvider>
        </ConfigProvider>
      </OdooProvider>
    </Router>
  );
};

export default App;
