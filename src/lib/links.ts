// Внутренние ссылки. Сайт лежит в подпапке (base), а русские страницы — под /ru/,
// поэтому все ссылки строятся только здесь.

import { defaultLocale, type Locale } from '../i18n/config.ts'

/** Чистая функция: собирает адрес из base, языка и пути страницы. */
export function buildHref(base: string, path: string, locale: Locale = defaultLocale): string {
  const cleanBase = base.replace(/^\/+|\/+$/g, '')
  const cleanPath = path.replace(/^\/+/, '')
  const segments = [cleanBase, locale === defaultLocale ? '' : locale].filter(Boolean)
  const prefix = segments.length > 0 ? `/${segments.join('/')}/` : '/'
  return prefix + cleanPath
}

/** Ссылка на страницу сайта с учётом base из настроек Astro. */
export function href(path: string, locale: Locale = defaultLocale): string {
  return buildHref(import.meta.env.BASE_URL, path, locale)
}
