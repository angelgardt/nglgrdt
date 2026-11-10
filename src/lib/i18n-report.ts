// Отчёт о переводе: какие текстовые поля данных ещё без английского варианта.
// Запускается командой npm run i18n:report (скрипт scripts/i18n-report.ts).

export type TextStatus = 'ok' | 'missing' | 'todo'

const TODO = 'TODO'

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Текст на нескольких языках — объект, в котором есть ru и нет ничего, кроме ru и en. */
function isText(value: unknown): value is { ru: string; en?: string } {
  return (
    isRecord(value) &&
    typeof value.ru === 'string' &&
    Object.keys(value).every((key) => key === 'ru' || key === 'en')
  )
}

/** Все текстовые поля записи с путём к каждому и состоянием перевода. */
export function collectTextFields(
  value: unknown,
  path: string[] = [],
): { field: string; status: TextStatus }[] {
  if (isText(value)) {
    const todo = value.en === TODO || value.ru === TODO
    const status: TextStatus = todo ? 'todo' : value.en ? 'ok' : 'missing'
    return [{ field: path.join('.'), status }]
  }
  if (Array.isArray(value)) {
    return value.flatMap((item, index) => collectTextFields(item, [...path, String(index)]))
  }
  if (isRecord(value)) {
    return Object.entries(value).flatMap(([key, item]) => collectTextFields(item, [...path, key]))
  }
  return []
}

export type I18nReport = {
  /** Поля со строкой TODO: их нужно заполнить в первую очередь. */
  todo: { file: string; id: string; field: string }[]
  /** Поля без en, по записям. */
  missing: { file: string; id: string; fields: string[] }[]
  total: number
  translated: number
  /** Процент переведённых полей среди видимых записей, с одним знаком после запятой. */
  coverage: number
}

/** Собирает отчёт. Ключ data — имя файла без расширения, значение — записи. */
export function buildReport(data: Record<string, unknown[]>): I18nReport {
  const report: I18nReport = { todo: [], missing: [], total: 0, translated: 0, coverage: 100 }
  for (const [file, entries] of Object.entries(data)) {
    for (const entry of entries) {
      if (!isRecord(entry) || entry.hidden === true) continue
      const id = typeof entry.id === 'string' ? entry.id : file
      const fields = collectTextFields(entry)
      report.total += fields.length
      report.translated += fields.filter((f) => f.status === 'ok').length
      for (const f of fields.filter((f) => f.status === 'todo')) {
        report.todo.push({ file, id, field: f.field })
      }
      const missing = fields.filter((f) => f.status === 'missing').map((f) => f.field)
      if (missing.length > 0) report.missing.push({ file, id, fields: missing })
    }
  }
  if (report.total > 0) {
    report.coverage = Math.round((report.translated / report.total) * 1000) / 10
  }
  return report
}

export function formatReport(report: I18nReport): string {
  const lines: string[] = []
  lines.push(`Поля с TODO — заполнить в первую очередь (${report.todo.length}):`)
  for (const item of report.todo) {
    lines.push(`  src/data/${item.file}.yaml → ${item.id} → ${item.field}`)
  }
  const missingCount = report.missing.reduce((sum, item) => sum + item.fields.length, 0)
  lines.push('', `Поля без перевода (${missingCount}):`)
  let currentFile = ''
  for (const item of report.missing) {
    if (item.file !== currentFile) {
      currentFile = item.file
      lines.push(`  src/data/${item.file}.yaml`)
    }
    lines.push(`    ${item.id}: ${item.fields.join(', ')}`)
  }
  lines.push(
    '',
    `Покрытие переводом по видимым записям: ${report.translated} из ${report.total} полей — ${report.coverage}%`,
  )
  return lines.join('\n')
}
