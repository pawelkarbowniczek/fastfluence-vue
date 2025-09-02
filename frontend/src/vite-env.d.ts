/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string

  // Auth0 variables
  readonly VITE_AUTH0_DOMAIN: string
  readonly VITE_AUTH0_CLIENT_ID: string
  readonly VITE_AUTH0_AUDIENCE: string
  readonly VITE_AUTH0_CALLBACK_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}