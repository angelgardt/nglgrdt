import { describe, expect, it } from 'vitest'
import { buildHref } from './links.ts'

describe('buildHref', () => {
  it('добавляет base к странице языка по умолчанию', () => {
    expect(buildHref('/nglgrdt', '/')).toBe('/nglgrdt/')
    expect(buildHref('/nglgrdt', '/cv/')).toBe('/nglgrdt/cv/')
  })

  it('добавляет префикс языка для русского', () => {
    expect(buildHref('/nglgrdt', '/', 'ru')).toBe('/nglgrdt/ru/')
    expect(buildHref('/nglgrdt', '/cv/', 'ru')).toBe('/nglgrdt/ru/cv/')
  })

  it('не добавляет префикс для языка по умолчанию', () => {
    expect(buildHref('/nglgrdt', '/cv/', 'en')).toBe('/nglgrdt/cv/')
  })

  it('не зависит от слэшей в base и пути', () => {
    expect(buildHref('/nglgrdt/', 'cv/', 'ru')).toBe('/nglgrdt/ru/cv/')
    expect(buildHref('/', '/cv/', 'ru')).toBe('/ru/cv/')
    expect(buildHref('', '/')).toBe('/')
  })

  it('сохраняет параметры и якорь', () => {
    expect(buildHref('/nglgrdt', '/cv/?tags=stats#work', 'ru')).toBe(
      '/nglgrdt/ru/cv/?tags=stats#work',
    )
  })
})
