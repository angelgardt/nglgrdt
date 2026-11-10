// JSON Schema для редактора: по ним VS Code (расширение YAML) подсказывает поля
// и подсвечивает ошибки в src/data/*.yaml. Файлы создаются из тех же схем, что проверяют сборку.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { z } from 'astro/zod'
import { DATA_DIR } from './data-files.ts'
import {
  DATA_FILES,
  buildSchemas,
  dateSchema,
  endDateSchema,
  fileSchema,
  type DataContext,
} from './schemas.ts'

export const SCHEMAS_DIR = `${DATA_DIR}/schemas`

const DATE_PATTERN = '^\\d{4}(-\\d{2}(-\\d{2})?)?$'

/** JSON Schema для каждого файла данных: имя файла -> схема. */
export function buildJsonSchemas(context: DataContext): Record<string, unknown> {
  const schemas = buildSchemas(context)
  const result: Record<string, unknown> = {}
  for (const { name, shape } of DATA_FILES) {
    result[name] = z.toJSONSchema(fileSchema(shape, schemas[name]), {
      // Схема описывает то, что пишет владелец, а не результат после значений по умолчанию.
      io: 'input',
      unrepresentable: 'any',
      override: ({ zodSchema, jsonSchema }) => {
        // Даты проверяются функцией, которую JSON Schema выразить не может, — подставляем шаблон.
        if (zodSchema === dateSchema) {
          Object.assign(jsonSchema, {
            type: ['string', 'integer'],
            pattern: DATE_PATTERN,
            description: 'Дата в кавычках: "YYYY", "YYYY-MM" или "YYYY-MM-DD"',
          })
        }
        if (zodSchema === endDateSchema) {
          Object.assign(jsonSchema, {
            type: ['string', 'integer'],
            pattern: `${DATE_PATTERN}|^present$`,
            description: 'Дата в кавычках ("YYYY", "YYYY-MM", "YYYY-MM-DD") или present',
          })
        }
      },
    })
  }
  return result
}

/** Записывает схемы в src/data/schemas. Файл переписывается, только если изменился. */
export function writeJsonSchemas(context: DataContext): string[] {
  mkdirSync(SCHEMAS_DIR, { recursive: true })
  const changed: string[] = []
  for (const [name, schema] of Object.entries(buildJsonSchemas(context))) {
    const path = `${SCHEMAS_DIR}/${name}.schema.json`
    const text = `${JSON.stringify(schema, null, 2)}\n`
    if (!existsSync(path) || readFileSync(path, 'utf-8') !== text) {
      writeFileSync(path, text)
      changed.push(path)
    }
  }
  return changed
}
