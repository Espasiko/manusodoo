/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_ODOO_URL: string
  readonly VITE_ODOO_DB: string
  readonly VITE_ODOO_USERNAME: string
  readonly VITE_ODOO_PASSWORD: string
  readonly VITE_ODOO_API_KEY: string
  readonly VITE_API_URL: string
  readonly DEV: boolean
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}