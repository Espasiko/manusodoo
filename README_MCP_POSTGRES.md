# Configuración del Servidor MCP PostgreSQL para Odoo Docker

Este documento explica cómo configurar y utilizar el servidor MCP (Model Context Protocol) de PostgreSQL para conectarse a la base de datos PostgreSQL que se ejecuta en un contenedor Docker como parte de la instalación de Odoo.

## Requisitos previos

- Docker y Docker Compose instalados
- Node.js y npm instalados
- Claude Desktop instalado (opcional, si deseas usar la interfaz gráfica)

## Configuración del servidor MCP PostgreSQL

### 1. Archivo de configuración

Se ha creado un archivo de configuración `claude_desktop_config.json` en el directorio raíz del proyecto con la siguiente configuración:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://odoo:odoo@localhost:5435/manus_odoo"
      ]
    }
  }
}
```

Esta configuración permite que el servidor MCP PostgreSQL se conecte a la base de datos `manus_odoo` en el contenedor Docker de PostgreSQL que se ejecuta en el puerto 5435.

### 2. Uso con Claude Desktop

Si utilizas Claude Desktop:

1. Copia el archivo `claude_desktop_config.json` a la ubicación de configuración de Claude Desktop:
   - En Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - En macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - En Linux: `~/.config/Claude/claude_desktop_config.json`

2. Reinicia Claude Desktop para que los cambios surtan efecto.

### 3. Uso con herramientas de línea de comandos

Para usar el servidor MCP PostgreSQL directamente desde la línea de comandos:

```bash
npx -y @modelcontextprotocol/server-postgres postgresql://odoo:odoo@localhost:5435/manus_odoo
```

## Verificación de la conexión

Para verificar que la conexión al servidor MCP PostgreSQL funciona correctamente:

1. Asegúrate de que los contenedores Docker de Odoo estén en ejecución:

```bash
docker-compose ps
```

2. Prueba la conexión a la base de datos PostgreSQL:

```bash
docker-compose exec db psql -U odoo -d manus_odoo -c "SELECT datname FROM pg_database;"
```

## Funcionalidades disponibles

El servidor MCP PostgreSQL proporciona las siguientes funcionalidades:

- Inspección de esquemas de bases de datos
- Ejecución de consultas SQL de solo lectura
- Análisis de datos y generación de informes

## Solución de problemas

Si encuentras problemas al conectarte al servidor MCP PostgreSQL:

1. Verifica que los contenedores Docker estén en ejecución.
2. Comprueba que el puerto 5435 esté accesible.
3. Asegúrate de que las credenciales de la base de datos sean correctas.
4. Revisa los logs de Docker para ver si hay errores en el contenedor de PostgreSQL.

```bash
docker-compose logs db
```

## Referencias

- [Documentación oficial de MCP](https://modelcontextprotocol.io/)
- [Servidor MCP PostgreSQL](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)