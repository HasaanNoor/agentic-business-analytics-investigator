import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

const nodeGlobal = globalThis as typeof globalThis & {
  process?: { env?: Record<string, string | undefined> };
};

export default defineConfig({
  base: nodeGlobal.process?.env?.VITE_BASE_PATH || '/',
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
  },
});
