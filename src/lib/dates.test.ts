import { describe, expect, it } from 'vitest'
import { isRangeOrdered, isValidDate, normalizeDate, periodEnd, periodStart } from './dates.ts'

describe('isValidDate', () => {
  it.each(['2021', '2021-10', '2024-03-14', '2024-02-29'])('принимает %s', (value) => {
    expect(isValidDate(value)).toBe(true)
  })

  it.each([
    '21',
    '2021-13',
    '2021-00',
    '2021-1',
    '2023-02-29',
    '2024-04-31',
    '14.03.2024',
    'март 2024',
    'present',
    '',
  ])('отклоняет %s', (value) => {
    expect(isValidDate(value)).toBe(false)
  })
})

describe('normalizeDate — даты без кавычек в YAML', () => {
  it('год-число превращает в строку', () => {
    expect(normalizeDate(2021)).toBe('2021')
  })

  it('объект Date превращает в YYYY-MM-DD', () => {
    expect(normalizeDate(new Date('2024-03-14T00:00:00Z'))).toBe('2024-03-14')
  })

  it('обрезает пробелы у строки', () => {
    expect(normalizeDate(' 2021-10 ')).toBe('2021-10')
  })

  it('не трогает present и правильные строки', () => {
    expect(normalizeDate('present')).toBe('present')
    expect(normalizeDate('2021-10')).toBe('2021-10')
  })

  it('остальное возвращает как есть, чтобы схема показала ошибку', () => {
    expect(normalizeDate(true)).toBe(true)
    expect(normalizeDate(20.5)).toBe(20.5)
    expect(normalizeDate(undefined)).toBe(undefined)
  })
})

describe('границы периода', () => {
  it('год: с 1 января по 31 декабря', () => {
    expect(periodStart('2021')).toBe(20210101)
    expect(periodEnd('2021')).toBe(20211231)
  })

  it('месяц: с первого по последний день', () => {
    expect(periodStart('2023-09')).toBe(20230901)
    expect(periodEnd('2023-09')).toBe(20230930)
    expect(periodEnd('2023-02')).toBe(20230228)
    expect(periodEnd('2024-02')).toBe(20240229)
  })

  it('день: сам день', () => {
    expect(periodStart('2024-03-14')).toBe(20240314)
    expect(periodEnd('2024-03-14')).toBe(20240314)
  })
})

describe('isRangeOrdered — end не раньше start', () => {
  it.each([
    ['2021', '2023'],
    ['2023-09', '2023-09'],
    ['2023-09', '2024-01'],
    ['2021-10', 'present'],
    ['2021-12-25', '2021'],
    ['2021-06', '2021'],
    ['2024-03-01', '2024-03-14'],
  ])('%s — %s допустимо', (start, end) => {
    expect(isRangeOrdered(start, end)).toBe(true)
  })

  it.each([
    ['2023', '2021'],
    ['2024-01', '2023-09'],
    ['2024-03-14', '2024-03-01'],
    ['2022-01', '2021'],
  ])('%s — %s недопустимо', (start, end) => {
    expect(isRangeOrdered(start, end)).toBe(false)
  })
})
