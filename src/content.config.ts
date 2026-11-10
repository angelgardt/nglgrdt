// Подключение файлов из src/data как коллекций Astro.
// Сами схемы — в src/lib/schemas.ts, проверка данных — в src/lib/data-files.ts.

import { defineCollection } from 'astro:content'
import { file } from 'astro/loaders'
import { parse } from 'yaml'
import { dataFilePath, formatProblems, loadData } from './lib/data-files.ts'
import { writeJsonSchemas } from './lib/json-schemas.ts'
import { DATA_FILES, buildSchemas, type DataFileName, type DataFileShape } from './lib/schemas.ts'

// Сначала проверяем все данные сами. Astro тоже проверяет записи по схеме, но не останавливает
// сборку при ошибке разметки YAML и не видит ошибок на уровне файла (повтор id, основной контакт).
const { data, problems } = loadData()
if (problems.length > 0) {
  throw new Error(
    `Ошибки в данных (${problems.length}). Подсказки — в docs/content.md.\n${formatProblems(problems)}`,
  )
}

const context = {
  tagIds: data.tags.map((tag) => String(tag.id)),
  positionIds: data.positions.map((position) => String(position.id)),
}
const schemas = buildSchemas(context)

// Подсказки редактора зависят от списка тегов и позиций, поэтому обновляются вместе с данными.
writeJsonSchemas(context)

type Entry = Record<string, unknown>

/** Приводит содержимое файла к виду, который понимает загрузчик file(). */
function parser(name: DataFileName, shape: DataFileShape) {
  return (text: string): Entry[] | Record<string, Entry> => {
    const parsed: unknown = parse(text)
    // Один объект становится коллекцией из одной записи с id, равным имени файла.
    if (shape === 'single') return { [name]: parsed as Entry }
    if (shape === 'groups') return (parsed as { groups?: Entry[] } | null)?.groups ?? []
    return (parsed as Entry[] | null) ?? []
  }
}

function loader(name: DataFileName) {
  const shape = DATA_FILES.find((item) => item.name === name)!.shape
  return file(dataFilePath(name), { parser: parser(name, shape) })
}

// Каждая коллекция записана отдельно, чтобы Astro вывел точные типы данных для страниц.
export const collections = {
  profile: defineCollection({ loader: loader('profile'), schema: schemas.profile }),
  contacts: defineCollection({ loader: loader('contacts'), schema: schemas.contacts }),
  tags: defineCollection({ loader: loader('tags'), schema: schemas.tags }),
  positions: defineCollection({ loader: loader('positions'), schema: schemas.positions }),
  courses: defineCollection({ loader: loader('courses'), schema: schemas.courses }),
  education: defineCollection({ loader: loader('education'), schema: schemas.education }),
  'extra-education': defineCollection({
    loader: loader('extra-education'),
    schema: schemas['extra-education'],
  }),
  achievements: defineCollection({ loader: loader('achievements'), schema: schemas.achievements }),
  languages: defineCollection({ loader: loader('languages'), schema: schemas.languages }),
  skills: defineCollection({ loader: loader('skills'), schema: schemas.skills }),
  interests: defineCollection({ loader: loader('interests'), schema: schemas.interests }),
  projects: defineCollection({ loader: loader('projects'), schema: schemas.projects }),
  grants: defineCollection({ loader: loader('grants'), schema: schemas.grants }),
  conferences: defineCollection({ loader: loader('conferences'), schema: schemas.conferences }),
  publications: defineCollection({ loader: loader('publications'), schema: schemas.publications }),
  materials: defineCollection({ loader: loader('materials'), schema: schemas.materials }),
}
