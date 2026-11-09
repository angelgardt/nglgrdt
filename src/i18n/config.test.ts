import { describe, expect, it } from 'vitest'
import { dataLocale, defaultLocale, englishMode, locales } from './config'

describe('настройки языков', () => {
  it('язык сайта по умолчанию — английский, язык данных — русский', () => {
    expect(defaultLocale).toBe('en')
    expect(dataLocale).toBe('ru')
  })

  it('оба языка входят в список языков сайта', () => {
    expect(locales).toContain(defaultLocale)
    expect(locales).toContain(dataLocale)
  })

  it('в списке языков нет повторов', () => {
    expect(new Set(locales).size).toBe(locales.length)
  })

  it('в версии 1 на английском показывается только визитка', () => {
    expect(englishMode).toBe('card')
  })
})
