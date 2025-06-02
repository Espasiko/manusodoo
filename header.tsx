import React from 'react';
import { Layout, Typography, Button, Avatar, Space, Dropdown } from 'antd';
import { MenuUnfoldOutlined, MenuFoldOutlined, UserOutlined, BellOutlined, SettingOutlined, LogoutOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

interface HeaderProps {
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
}

const Header: React.FC<HeaderProps> = ({ collapsed, setCollapsed }) => {
  const items: MenuProps['items'] = [
    {
      key: '1',
      label: 'Perfil',
      icon: <UserOutlined />,
    },
    {
      key: '2',
      label: 'Configuración',
      icon: <SettingOutlined />,
    },
    {
      key: '3',
      label: 'Cerrar sesión',
      icon: <LogoutOutlined />,
    },
  ];

  return (
    <AntHeader style={{ padding: '0 16px', background: '#1f1f1f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <Button
        type="text"
        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        onClick={() => setCollapsed(!collapsed)}
        style={{ fontSize: '16px', width: 64, height: 64, color: '#fff' }}
      />
      <Space>
        <Button type="text" icon={<BellOutlined />} style={{ color: '#fff' }} />
        <Dropdown menu={{ items }} placement="bottomRight">
          <Space style={{ cursor: 'pointer' }}>
            <Avatar icon={<UserOutlined />} />
            <Text style={{ color: '#fff' }}>Admin</Text>
          </Space>
        </Dropdown>
      </Space>
    </AntHeader>
  );
};

export default Header;
