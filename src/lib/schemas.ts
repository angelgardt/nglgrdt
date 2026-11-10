// Схемы всех файлов из src/data. Описание полей для владельца — в docs/content.md.
//
// Схемы лежат здесь, а не в src/content.config.ts, чтобы ими могли пользоваться тесты,
// скрипты (JSON Schema для редактора, отчёт о переводе) и будущая админка.

import { z } from 'astro/zod'
import { PRESENT, isRangeOrdered, isValidDate, normalizeDate } from './dates.ts'

// Сообщения об ошибках — на русском: их читает владелец, когда сборка падает из-за данных.
z.config(z.locales.ru())

// ---------- Общие типы ----------

/** Текст на нескольких языках: ru обязателен, en — перевод. */
export const textSchema = z.strictObject({
  ru: z.string().min(1),
  en: z.string().min(1).optional(),
})

/** Текст, который показывает английская визитка: en обязателен (до перевода — строка TODO). */
export const requiredEnTextSchema = z.strictObject({
  ru: z.string().min(1),
  en: z.string().min(1),
})

const DATE_MESSAGE = 'Дата пишется в кавычках в формате "YYYY", "YYYY-MM" или "YYYY-MM-DD"'

/** Дата. Принимает и значения без кавычек, приводя их к строке. */
export const dateSchema = z.preprocess(
  normalizeDate,
  z.string({ error: DATE_MESSAGE }).refine(isValidDate, { error: DATE_MESSAGE }),
)

/** Дата окончания: дата или present — «по настоящее время». */
export const endDateSchema = z.preprocess(
  normalizeDate,
  z.string({ error: DATE_MESSAGE }).refine((value) => value === PRESENT || isValidDate(value), {
    error: `${DATE_MESSAGE} либо present`,
  }),
)

const idSchema = z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/, {
  error: 'id пишется строчными латинскими буквами и цифрами через дефис, например hse-teacher',
})

/** Строка, даже если в YAML число без кавычек (номер журнала, страницы). */
const looseString = z.preprocess(
  (value) => (typeof value === 'number' ? String(value) : value),
  z.string().min(1),
)

const yearSchema = z.coerce.number().int().min(1900).max(2100)

/** Проверка, что end не раньше start. Ошибка ставится на поле end. */
function checkRange(
  value: { start?: unknown; end?: unknown },
  ctx: { addIssue: (issue: { code: 'custom'; path: string[]; message: string }) => void },
): void {
  const { start, end } = value
  if (typeof start !== 'string' || typeof end !== 'string') return
  if (!isValidDate(start) || (end !== PRESENT && !isValidDate(end))) return
  if (!isRangeOrdered(start, end)) {
    ctx.addIssue({
      code: 'custom',
      path: ['end'],
      message: `Дата окончания (${end}) раньше даты начала (${start})`,
    })
  }
}

/** Ссылка на id из другого файла. Неизвестный id — ошибка сборки. */
function idRef(ids: string[], notFound: (id: string) => string, file: string) {
  const message = (input: unknown) =>
    `${notFound(String(input))}. Допустимые id перечислены в src/data/${file}`
  if (ids.length === 0) {
    return z.string().refine(() => false, { error: (issue) => message(issue.input) })
  }
  return z.enum(ids as [string, ...string[]], { error: (issue) => message(issue.input) })
}

// ---------- Схемы файлов ----------

export type DataContext = {
  /** id из tags.yaml */
  tagIds: string[]
  /** id из positions.yaml */
  positionIds: string[]
}

export function buildSchemas(context: DataContext) {
  const tagRef = idRef(context.tagIds, (id) => `Тег «${id}» не найден`, 'tags.yaml')
  const positionRef = idRef(
    context.positionIds,
    (id) => `Позиция «${id}» не найдена`,
    'positions.yaml',
  )

  // Служебные поля есть у каждой записи.
  const service = {
    id: idSchema,
    tags: z.array(tagRef).default([]),
    /** Всегда показывать, не сворачивать. */
    pinned: z.boolean().default(false),
    /** Не показывать нигде. */
    hidden: z.boolean().default(false),
    /** Комментарий владельца, на сайт не выводится. */
    notes: z.string().optional(),
  }

  const text = textSchema
  const optionalText = textSchema.optional()

  const profile = z.strictObject({
    name: requiredEnTextSchema,
    /** Фамилия, которая выделяется в списке авторов публикаций. */
    authorName: z.string().min(1),
    positioning: requiredEnTextSchema,
    location: requiredEnTextSchema,
    /** Путь к фото от корня проекта. */
    photo: z.string().min(1),
    focusAreas: z.array(
      z.strictObject({
        id: idSchema,
        title: requiredEnTextSchema,
        text: requiredEnTextSchema,
        tag: tagRef,
      }),
    ),
    notes: z.string().optional(),
  })

  const contacts = z.strictObject({
    ...service,
    kind: z.enum([
      'email',
      'telegram',
      'linkedin',
      'github',
      'whatsapp',
      'skype',
      'twitter',
      'facebook',
      'instagram',
      'phone',
      'other',
    ]),
    label: z.string().min(1).optional(),
    url: z.string().min(1),
    /** Показывать ли контакт на сайте. По умолчанию — нет. */
    visible: z.boolean().default(false),
    /** Основной контакт: на него ведёт кнопка «Написать». */
    primary: z.boolean().default(false),
  })

  const tags = z.strictObject({
    id: idSchema,
    label: text,
    notes: z.string().optional(),
  })

  const positions = z
    .strictObject({
      ...service,
      kind: z.enum(['teaching', 'research', 'academic', 'management', 'other']),
      role: text,
      organization: text,
      /** Подразделение. */
      unit: optionalText,
      /** Мероприятие, курс или проект, в рамках которого была роль. */
      context: optionalText,
      /** Если даты не заданы, они вычисляются по курсам позиции. */
      start: dateSchema.optional(),
      end: endDateSchema.optional(),
      description: optionalText,
      featured: z.boolean().default(false),
    })
    .superRefine(checkRange)

  const courses = z.strictObject({
    ...service,
    position: positionRef,
    title: text,
    /** Запуски курса: каждый раз, когда курс читался. */
    runs: z
      .array(
        z
          .strictObject({
            start: dateSchema,
            end: endDateSchema.optional(),
            /** Роль в этом запуске, если отличается от роли позиции. */
            role: optionalText,
            duties: optionalText,
          })
          .superRefine(checkRange),
      )
      .min(1),
    materialsUrl: z.string().min(1).optional(),
  })

  const person = z.strictObject({ name: text, title: optionalText })

  const education = z
    .strictObject({
      ...service,
      level: z.enum(['bachelor', 'master', 'specialist', 'other']),
      start: dateSchema,
      end: endDateSchema.optional(),
      university: text,
      faculty: optionalText,
      department: optionalText,
      program: optionalText,
      track: optionalText,
      specialty: optionalText,
      qualification: optionalText,
      gpa: optionalText,
      minor: z
        .strictObject({ institute: optionalText, program: optionalText, specialty: optionalText })
        .optional(),
      thesis: z
        .strictObject({
          title: text,
          supervisor: person.optional(),
          advisor: person.optional(),
          reviewer: person.optional(),
          grades: z
            .strictObject({
              supervisor: optionalText,
              reviewer: optionalText,
              commission: optionalText,
            })
            .optional(),
        })
        .optional(),
      featured: z.boolean().default(false),
    })
    .superRefine(checkRange)

  const extraEducation = z
    .strictObject({
      ...service,
      kind: z.enum(['qualification', 'school', 'mooc']),
      title: text,
      track: optionalText,
      organizer: optionalText,
      organization: optionalText,
      platform: optionalText,
      start: dateSchema,
      end: endDateSchema.optional(),
    })
    .superRefine(checkRange)

  const achievements = z
    .strictObject({
      ...service,
      title: text,
      context: optionalText,
      organization: optionalText,
      start: dateSchema,
      end: endDateSchema.optional(),
    })
    .superRefine(checkRange)

  const languages = z.strictObject({
    ...service,
    name: text,
    /** Уровень как есть: «родной», «B2». */
    level: optionalText,
  })

  const skillGroup = {
    id: idSchema,
    title: text,
    items: z.array(text).default([]),
  }

  const skills = z.strictObject({
    ...service,
    ...skillGroup,
    subgroups: z.array(z.strictObject(skillGroup)).default([]),
  })

  const interests = z.strictObject({
    ...service,
    ...skillGroup,
  })

  const projects = z
    .strictObject({
      ...service,
      title: text,
      role: optionalText,
      description: optionalText,
      methods: z.array(text).default([]),
      start: dateSchema.optional(),
      end: endDateSchema.optional(),
      url: z.string().min(1).optional(),
      featured: z.boolean().default(false),
    })
    .superRefine(checkRange)

  const grants = z
    .strictObject({
      ...service,
      funder: text,
      number: looseString.optional(),
      title: text,
      role: optionalText,
      start: dateSchema,
      end: endDateSchema.optional(),
    })
    .superRefine(checkRange)

  const conferences = z
    .strictObject({
      ...service,
      event: text,
      talkTitle: text,
      location: optionalText,
      talkType: z.enum(['talk', 'poster', 'workshop']),
      start: dateSchema,
      end: endDateSchema.optional(),
    })
    .superRefine(checkRange)

  const publications = z.strictObject({
    ...service,
    /** Авторы в порядке авторства, как в выходных данных. */
    authors: z.array(z.string().min(1)).min(1),
    title: z.string().min(1),
    venue: z.string().min(1),
    year: yearSchema,
    volume: looseString.optional(),
    issue: looseString.optional(),
    pages: looseString.optional(),
    status: z.enum(['published', 'in-press', 'submitted']).default('published'),
    doi: z.string().min(1).optional(),
    url: z.string().min(1).optional(),
  })

  const materials = z.strictObject({
    ...service,
    kind: z.enum(['course', 'workshop', 'book', 'other']),
    title: text,
    audience: optionalText,
    description: optionalText,
    context: optionalText,
    year: yearSchema.optional(),
    url: z.string().min(1).optional(),
    copyright: z.string().min(1).optional(),
  })

  return {
    profile,
    contacts,
    tags,
    positions,
    courses,
    education,
    'extra-education': extraEducation,
    achievements,
    languages,
    skills,
    interests,
    projects,
    grants,
    conferences,
    publications,
    materials,
  }
}

export type DataSchemas = ReturnType<typeof buildSchemas>
export type DataFileName = keyof DataSchemas

/**
 * Как устроен файл:
 * - list — список записей;
 * - single — один объект (profile.yaml);
 * - groups — объект с полем groups, в котором список записей (skills.yaml, interests.yaml).
 */
export type DataFileShape = 'list' | 'single' | 'groups'

export const DATA_FILES: { name: DataFileName; shape: DataFileShape }[] = [
  { name: 'profile', shape: 'single' },
  { name: 'contacts', shape: 'list' },
  { name: 'tags', shape: 'list' },
  { name: 'positions', shape: 'list' },
  { name: 'courses', shape: 'list' },
  { name: 'education', shape: 'list' },
  { name: 'extra-education', shape: 'list' },
  { name: 'achievements', shape: 'list' },
  { name: 'languages', shape: 'list' },
  { name: 'skills', shape: 'groups' },
  { name: 'interests', shape: 'groups' },
  { name: 'projects', shape: 'list' },
  { name: 'grants', shape: 'list' },
  { name: 'conferences', shape: 'list' },
  { name: 'publications', shape: 'list' },
  { name: 'materials', shape: 'list' },
]

/** Схема файла целиком — для JSON Schema, по которой редактор подсказывает поля. */
export function fileSchema(shape: DataFileShape, entry: z.ZodType) {
  if (shape === 'single') return entry
  if (shape === 'groups') return z.strictObject({ groups: z.array(entry) })
  return z.array(entry)
}
