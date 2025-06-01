#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import os
import sys

# Configuración de Odoo
url = 'http://localhost:8069'
db = 'pelotazo'  # Cambiado de 'manusodoo' a 'pelotazo'
username = 'admin'
password = 'admin'

# Crear directorio para logs si no existe
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configurar log
log_file = os.path.join(log_dir, 'verificacion_modulo.log')

def log(mensaje):
    """Función para registrar mensajes en el log y mostrarlos en pantalla"""
    print(mensaje)
    with open(log_file, 'a') as f:
        f.write(mensaje + '\n')

log('Iniciando verificación del módulo custom_electrodomesticos...')
log(f'Conectando con Odoo en {url}, base de datos: {db}')

try:
    # Conectar con Odoo
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    
    # Verificar versión de Odoo
    version_info = common.version()
    log(f'Versión de Odoo: {version_info["server_version"]}')
    
    # Autenticar
    uid = common.authenticate(db, username, password, {})
    log(f'UID: {uid}')
    
    if not uid:
        log('Error de autenticación. Verifique las credenciales.')
        sys.exit(1)
    
    # Conectar con los modelos
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Actualizar lista de módulos
    log('Actualizando lista de módulos disponibles...')
    try:
        models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [])
        log('Lista de módulos actualizada correctamente')
    except Exception as e:
        log(f'Error al actualizar la lista de módulos: {e}')
    
    # Buscar el módulo
    module_name = 'custom_electrodomesticos'
    log(f'Buscando el módulo {module_name}...')
    module_ids = models.execute_kw(db, uid, password, 'ir.module.module', 'search', [[['name', '=', module_name]]])
    log(f'IDs de módulos encontrados: {module_ids}')
    
    # Obtener información del módulo
    if module_ids:
        module_info = models.execute_kw(db, uid, password, 'ir.module.module', 'read', [module_ids, ['name', 'state', 'latest_version']])
        log(f'Información del módulo: {module_info}')
        
        # Verificar estado e instrucciones
        estado = module_info[0]['state']
        log(f'Estado actual del módulo: {estado}')
        
        if estado == 'installed':
            log('El módulo está correctamente instalado.')
        else:
            log('El módulo no está instalado. Instrucciones para instalarlo:')
            log('1. Acceda a la interfaz web de Odoo: http://localhost:8069')
            log('2. Inicie sesión con usuario admin y contraseña admin')
            log('3. Vaya a Aplicaciones -> Actualizar lista de aplicaciones')
            log('4. Busque "custom_electrodomesticos" y haga clic en Instalar')
            log('O ejecute el siguiente comando en la terminal:')
            log(f'docker exec last_odoo_1 odoo -d {db} -i {module_name} --stop-after-init')
    else:
        log(f'El módulo {module_name} no se encuentra en la base de datos.')
        log('Verifique que el directorio del módulo esté correctamente ubicado en /mnt/extra-addons dentro del contenedor.')
        log('Ejecute el siguiente comando para verificar:')
        log('docker exec last_odoo_1 ls -la /mnt/extra-addons/custom_electrodomesticos')

except Exception as e:
    log(f'Error durante la verificación: {e}')
    sys.exit(1)

log('Verificación completada.')