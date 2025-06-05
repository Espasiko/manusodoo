# Notas de Autenticación y Backend (FastAPI)

## Usuarios y Contraseñas (Fake DB)
- El usuario `admin` está definido en el backend como:
  - username: `admin`
  - email: `admin@example.com`
  - hashed_password: `admin_password_secure`
- **IMPORTANTE:** La contraseña real para login es `admin_password_secure` (no `admin`).
- Si se usa autenticación directa (sin hash), la comparación es `plain_password == hashed_password`.
- Si se usa un hash real, revisar el método de verificación.

## Errores comunes
- Error 401 al llamar `/token` suele deberse a contraseña incorrecta.
- Para la tienda online (puerto 3002) y dashboard (puerto 3001), usar siempre las credenciales correctas del backend.

## Flujo de login correcto
1. Hacer POST a `/token` con usuario y contraseña.
2. Guardar el `access_token` JWT recibido.
3. Enviar el token en la cabecera `Authorization: Bearer <token>` en todas las peticiones protegidas.

---

## Resumen de integración actual
- El frontend (React) debe loguearse con `admin` / `admin_password_secure` antes de pedir productos reales.
- Si cambian las credenciales en el backend, actualizarlas también en el frontend.
- Si se implementa hashing real, actualizar el flujo de login en consecuencia.

---

*Última actualización: 2025-06-03*
