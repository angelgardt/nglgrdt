// Проверки целого файла данных — то, что нельзя проверить схемой одной записи.

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Список id, которые встречаются в файле больше одного раза. */
export function findDuplicateIds(entries: unknown[]): string[] {
  const seen = new Set<string>()
  const duplicates = new Set<string>()
  for (const entry of entries) {
    if (!isRecord(entry) || typeof entry.id !== 'string') continue
    if (seen.has(entry.id)) duplicates.add(entry.id)
    seen.add(entry.id)
  }
  return [...duplicates]
}

/**
 * Кнопка «Написать» ведёт на основной контакт, поэтому он должен быть ровно один и видимый.
 * Возвращает текст ошибки или null.
 */
export function checkPrimaryContact(contacts: unknown[]): string | null {
  const primary = contacts.filter(isRecord).filter((contact) => contact.primary === true)
  if (primary.length === 0) {
    return 'нет основного контакта: у одной записи должно быть primary: true'
  }
  if (primary.length > 1) {
    const ids = primary.map((contact) => String(contact.id)).join(', ')
    return `основной контакт должен быть один, а primary: true стоит у нескольких: ${ids}`
  }
  const [contact] = primary
  if (contact?.hidden === true) {
    return `основной контакт ${String(contact.id)} скрыт: уберите hidden: true`
  }
  if (contact?.visible !== true) {
    return `основной контакт ${String(contact?.id)} должен быть видимым: поставьте visible: true`
  }
  return null
}
