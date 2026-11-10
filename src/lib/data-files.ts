// Чтение и проверка файлов из src/data.
//
// Проверка запускается при сборке (из src/content.config.ts), в тестах и в скриптах.
// Любая найденная проблема описывается тремя вещами: файл, id записи и поле.

import { existsSync, readFileSync } from 'node:fs'
import { parse, YAMLParseError } from 'yaml'
import { checkPrimaryContact, findDuplicateIds } from './data-checks.ts'
import { DATA_FILES, buildSchemas, type DataFileName, type DataFileShape } from './schemas.ts'

export const DATA_DIR = 'src/data'

export function dataFilePath(name: string): string {
  return `${DATA_DIR}/${name}.yaml`
}

export type DataProblem = {
  file: string
  id?: string
  field?: string
  message: string
}

type Entry = Record<string, unknown>

/** Проверенные данные: для каждого файла — список записей (у profile запись одна). */
export type SiteData = Record<DataFileName, Entry[]>

function isRecord(value: unknown): value is Entry {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Достаёт из разобранного файла список записей с учётом вида файла. */
function toEntries(shape: DataFileShape, parsed: unknown): Entry[] | string {
  if (shape === 'single') {
    return isRecord(parsed) ? [parsed] : 'в файле должен быть один объект с полями'
  }
  const list = shape === 'groups' && isRecord(parsed) ? parsed.groups : parsed
  if (shape === 'groups' && !isRecord(parsed)) {
    return 'в файле должно быть поле groups со списком групп'
  }
  // Пустой файл или файл из одних комментариев — это пустой список.
  if (list === null || list === undefined) return []
  if (!Array.isArray(list) || !list.every(isRecord)) {
    return 'в файле должен быть список записей: каждая начинается с «- id: ...»'
  }
  return list
}

/**
 * Проверяет тексты файлов данных. Ключ — имя файла без расширения, значение — содержимое.
 * Файл, которого нет, считается пустым.
 */
export function validateTexts(texts: Record<string, string | undefined>): {
  data: SiteData
  problems: DataProblem[]
} {
  const problems: DataProblem[] = []
  const raw = new Map<DataFileName, Entry[]>()

  // 1. Разбор YAML и вид файла.
  for (const { name, shape } of DATA_FILES) {
    const file = dataFilePath(name)
    const text = texts[name]
    if (text === undefined) {
      if (shape === 'single') problems.push({ file, message: 'файл не найден' })
      raw.set(name, [])
      continue
    }
    try {
      const entries = toEntries(shape, parse(text))
      if (typeof entries === 'string') {
        problems.push({ file, message: entries })
        raw.set(name, [])
      } else {
        raw.set(name, entries)
      }
    } catch (error) {
      const line = error instanceof YAMLParseError ? error.linePos?.[0].line : undefined
      const where = line === undefined ? '' : `строка ${line}: `
      const reason = error instanceof Error ? error.message.split('\n')[0] : String(error)
      problems.push({ file, message: `ошибка разметки YAML, ${where}${reason}` })
      raw.set(name, [])
    }
  }

  // Если какой-то файл не разобрался, дальше проверять бессмысленно: ошибки посыплются каскадом.
  if (problems.length > 0) {
    const empty = Object.fromEntries(
      DATA_FILES.map(({ name }) => [name, []]),
    ) as unknown as SiteData
    return { data: empty, problems }
  }

  // 2. Проверки файла целиком.
  for (const { name, shape } of DATA_FILES) {
    if (shape === 'single') continue
    for (const id of findDuplicateIds(raw.get(name) ?? [])) {
      problems.push({ file: dataFilePath(name), id, field: 'id', message: 'id повторяется' })
    }
  }
  const contacts = raw.get('contacts') ?? []
  if (texts.contacts !== undefined) {
    const contactProblem = checkPrimaryContact(contacts)
    if (contactProblem) problems.push({ file: dataFilePath('contacts'), message: contactProblem })
  }

  // 3. Схема каждой записи. Списки тегов и позиций берутся из самих данных.
  const ids = (name: DataFileName) =>
    (raw.get(name) ?? []).map((entry) => entry.id).filter((id) => typeof id === 'string')
  const schemas = buildSchemas({ tagIds: ids('tags'), positionIds: ids('positions') })

  const data = {} as SiteData
  for (const { name } of DATA_FILES) {
    data[name] = []
    for (const entry of raw.get(name) ?? []) {
      const result = schemas[name].safeParse(entry)
      if (result.success) {
        data[name].push(result.data as Entry)
        continue
      }
      for (const issue of result.error.issues) {
        problems.push({
          file: dataFilePath(name),
          id: typeof entry.id === 'string' ? entry.id : undefined,
          field: issue.path.join('.') || undefined,
          message: issue.message,
        })
      }
    }
  }

  return { data, problems }
}

/** Читает и проверяет все файлы из src/data. */
export function loadData(dir: string = DATA_DIR): { data: SiteData; problems: DataProblem[] } {
  const texts: Record<string, string | undefined> = {}
  for (const { name } of DATA_FILES) {
    const path = `${dir}/${name}.yaml`
    texts[name] = existsSync(path) ? readFileSync(path, 'utf-8') : undefined
  }
  return validateTexts(texts)
}

/** Сообщение об ошибках для владельца: по строке на проблему. */
export function formatProblems(problems: DataProblem[]): string {
  return problems
    .map((p) => {
      const where = [p.file, p.id, p.field].filter((part) => part !== undefined).join(' → ')
      return `${where}: ${p.message}`
    })
    .join('\n')
}
