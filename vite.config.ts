import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'

export default defineConfig({
  base: './',
  publicDir: false,
  plugins: [
    react(),
    {
      name: 'verify-public-assets',
      closeBundle() {
        // Direct writes are reliable on the mounted delivery filesystem; cpSync
        // can otherwise race its own unlink/copy operations during a clean build.
        const source = resolve(__dirname, 'public')
        for (const name of readdirSync(source, { recursive: true, encoding: 'utf8' })) {
          const input = resolve(source, name)
          if (!statSync(input).isFile()) continue
          const output = resolve(__dirname, 'dist', name)
          mkdirSync(dirname(output), { recursive: true })
          writeFileSync(output, readFileSync(input))
        }
      },
    },
  ],
  build: { outDir: 'dist', emptyOutDir: true },
})
