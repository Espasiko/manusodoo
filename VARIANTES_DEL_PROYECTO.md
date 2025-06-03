# Memoria de variantes del proyecto ManusOdoo

## Resumen de variantes activas

### manusodoo-roto
- **Odoo:** puerto 8070
- **PostgreSQL:** puerto 5434
- **Base de datos:** odoo
- **Addons/configuración:** /manusodoo-roto/addons, /config
- **FastAPI:** 8000/8001
- **Frontend:** VITE_ODOO_URL=http://localhost:8070

### last_odoo_1
- **Odoo:** puerto 8071
- **PostgreSQL:** puerto 5435
- **Base de datos:** odoo
- **Addons/configuración:** /manusodoo/last/addons, /last/config
- **FastAPI:** depende setup
- **Frontend:** VITE_ODOO_URL=http://localhost:8071

## Esquema de puertos y comandos útiles

| Variante         | Odoo (puerto) | PostgreSQL (puerto) | Base de datos | FastAPI      | Frontend (VITE_ODOO_URL)           |
|------------------|--------------|---------------------|--------------|--------------|------------------------------------|
| manusodoo-roto   | 8070         | 5434                | odoo         | 8000/8001    | http://localhost:8070              |
| last_odoo_1      | 8071         | 5435                | odoo         | depende setup| http://localhost:8071              |

### Comandos para inspección y gestión

- Ver logs de Odoo:
  ```bash
  docker logs -f manusodoo-roto_odoo_1
  docker logs -f last_odoo_1
  ```
- Ver logs de la base de datos:
  ```bash
  docker logs -f manusodoo-roto_db_1
  docker logs -f last_db_1
  ```
- Ver configuración de Odoo:
  ```bash
  docker exec -it manusodoo-roto_odoo_1 cat /etc/odoo/odoo.conf
  docker exec -it last_odoo_1 cat /etc/odoo/odoo.conf
  ```
- Ver tablas y bases de datos:
  ```bash
  docker exec -it manusodoo-roto_db_1 psql -U odoo -d odoo -c "\dt"
  docker exec -it last_db_1 psql -U odoo -d odoo -c "\dt"
  ```
- Parar servicios:
  ```bash
  docker-compose down
  ```
- Arrancar servicios:
  ```bash
  ./start.sh
  ```

## Recomendaciones para aclararte

- Revisa siempre los archivos `.env` y `docker-compose.yml` de cada variante para ver a qué servicios apunta cada frontend y backend.
- Si tienes dudas sobre qué frontend ves en el navegador, revisa la variable `VITE_ODOO_URL` y la URL donde está corriendo el servidor de desarrollo o build.
- Consulta la configuración de Odoo de cada contenedor para saber a qué base de datos y usuario se conecta.
- Si ves errores 500 en Odoo, revisa los logs del contenedor y la configuración de los addons personalizados o módulos instalados recientemente.
- Mantén separadas las bases de datos y volúmenes de cada variante para evitar conflictos.

---

*Documento generado automáticamente para ayudarte a gestionar y entender las variantes y puertos activos de tu proyecto ManusOdoo.*
