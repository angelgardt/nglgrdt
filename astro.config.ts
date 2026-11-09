import { defineConfig } from 'astro/config'
import { defaultLocale, locales } from './src/i18n/config'

// Сайт публикуется на GitHub Pages в подпапке /nglgrdt, поэтому нужны и site, и base.
export default defineConfig({
  site: 'https://angelgardt.github.io',
  base: '/nglgrdt',
  output: 'static',
  i18n: {
    locales: [...locales],
    defaultLocale,
    // Язык по умолчанию (английский) живёт без префикса: /, русский — под /ru/.
    routing: { prefixDefaultLocale: false },
  },
})
