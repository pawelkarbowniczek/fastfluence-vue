/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  // tu możesz dopisywać kolejne zmienne
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
