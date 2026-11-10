// Даты в данных: строки YYYY, YYYY-MM или YYYY-MM-DD. Конец периода может быть 'present'.
// Здесь только разбор и сравнение; формат для вывода появится в итерации 3.

export const PRESENT = 'present'

const DATE_PATTERN = /^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?$/

function daysInMonth(year: number, month: number): number {
  // День 0 следующего месяца — это последний день нужного.
  return new Date(Date.UTC(year, month, 0)).getUTCDate()
}

function parts(date: string): { year: number; month?: number; day?: number } | null {
  const match = DATE_PATTERN.exec(date)
  if (!match) return null
  const year = Number(match[1])
  const month = match[2] === undefined ? undefined : Number(match[2])
  const day = match[3] === undefined ? undefined : Number(match[3])
  if (month !== undefined && (month < 1 || month > 12)) return null
  if (month !== undefined && day !== undefined && (day < 1 || day > daysInMonth(year, month))) {
    return null
  }
  return { year, month, day }
}

/** Проверяет формат и то, что такая дата есть в календаре. */
export function isValidDate(value: string): boolean {
  return parts(value) !== null
}

/**
 * Приводит дату из YAML к строке. Владелец может забыть кавычки: тогда YAML отдаёт
 * 2021 как число, а 2024-03-14 — как объект Date. Всё остальное возвращается как есть,
 * чтобы схема показала понятную ошибку.
 */
export function normalizeDate(value: unknown): unknown {
  if (typeof value === 'number' && Number.isInteger(value)) return String(value)
  if (value instanceof Date && !Number.isNaN(value.getTime())) {
    return value.toISOString().slice(0, 10)
  }
  if (typeof value === 'string') return value.trim()
  return value
}

function toNumber(year: number, month: number, day: number): number {
  return year * 10000 + month * 100 + day
}

/** Первый день периода числом ГГГГММДД: для 2021 — 1 января, для 2021-10 — 1 октября. */
export function periodStart(date: string): number {
  const p = parts(date)
  if (!p) throw new Error(`Неверная дата: ${date}`)
  return toNumber(p.year, p.month ?? 1, p.day ?? 1)
}

/** Последний день периода числом ГГГГММДД: для 2021 — 31 декабря, для 2023-02 — 28 февраля. */
export function periodEnd(date: string): number {
  const p = parts(date)
  if (!p) throw new Error(`Неверная дата: ${date}`)
  const month = p.month ?? 12
  return toNumber(p.year, month, p.day ?? daysInMonth(p.year, month))
}

/** Конец периода не раньше начала. 'present' всегда подходит. */
export function isRangeOrdered(start: string, end: string): boolean {
  if (end === PRESENT) return true
  return periodEnd(end) >= periodStart(start)
}
