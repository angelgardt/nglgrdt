import { describe, expect, it } from 'vitest'
import { buildSchemas } from './schemas.ts'

const schemas = buildSchemas({ tagIds: ['stats', 'teaching'], positionIds: ['hse-teacher'] })

/** Пути полей, в которых схема нашла ошибки. */
function errorPaths(schema: { safeParse: (value: unknown) => unknown }, value: unknown): string[] {
  const result = schema.safeParse(value) as {
    success: boolean
    error?: { issues: { path: PropertyKey[] }[] }
  }
  return result.success ? [] : result.error!.issues.map((issue) => issue.path.join('.'))
}

const position = {
  id: 'hse-teacher',
  kind: 'teaching',
  role: { ru: 'преподаватель' },
  organization: { ru: 'НИУ ВШЭ' },
}

describe('служебные поля', () => {
  it('получают значения по умолчанию', () => {
    const parsed = schemas.positions.parse(position)
    expect(parsed).toMatchObject({ tags: [], pinned: false, hidden: false, featured: false })
  })

  it('id должен быть в kebab-case', () => {
    expect(errorPaths(schemas.positions, { ...position, id: 'HSE_Teacher' })).toEqual(['id'])
    expect(errorPaths(schemas.positions, { ...position, id: 'hse--teacher' })).toEqual(['id'])
  })

  it('неизвестное поле — ошибка, чтобы опечатка в названии не прошла молча', () => {
    expect(errorPaths(schemas.positions, { ...position, organisation: { ru: 'x' } })).toEqual([''])
  })
})

describe('текст на нескольких языках', () => {
  it('ru обязателен, en — нет', () => {
    expect(errorPaths(schemas.positions, { ...position, role: { en: 'Teacher' } })).toEqual([
      'role.ru',
    ])
    expect(
      errorPaths(schemas.positions, { ...position, role: { ru: 'x', en: 'Teacher' } }),
    ).toEqual([])
  })

  it('для полей визитки en обязателен, TODO допустим', () => {
    const profile = {
      name: { ru: 'Антон Ангельгардт', en: 'Anton Angelgardt' },
      authorName: 'Ангельгардт',
      positioning: { ru: 'Преподаю статистику', en: 'TODO' },
      location: { ru: 'Москва', en: 'Moscow' },
      photo: 'src/assets/photo.png',
      focusAreas: [
        {
          id: 'stats',
          title: { ru: 'статистика', en: 'TODO' },
          text: { ru: 'TODO', en: 'TODO' },
          tag: 'stats',
        },
      ],
    }
    expect(errorPaths(schemas.profile, profile)).toEqual([])
    expect(errorPaths(schemas.profile, { ...profile, location: { ru: 'Москва' } })).toEqual([
      'location.en',
    ])
  })
})

describe('даты', () => {
  it('даты без кавычек приводятся к строкам', () => {
    const parsed = schemas.positions.parse({
      ...position,
      start: 2021,
      end: new Date('2024-03-14T00:00:00Z'),
    })
    expect(parsed.start).toBe('2021')
    expect(parsed.end).toBe('2024-03-14')
  })

  it('end может быть present, start — нет', () => {
    expect(
      errorPaths(schemas.positions, { ...position, start: '2021-10', end: 'present' }),
    ).toEqual([])
    expect(errorPaths(schemas.positions, { ...position, start: 'present' })).toEqual(['start'])
  })

  it('неверная дата — ошибка в поле даты', () => {
    expect(errorPaths(schemas.positions, { ...position, start: '2021-13' })).toEqual(['start'])
    expect(errorPaths(schemas.positions, { ...position, start: 'октябрь 2021' })).toEqual(['start'])
  })

  it('end раньше start — ошибка в поле end', () => {
    expect(errorPaths(schemas.positions, { ...position, start: '2023', end: '2021' })).toEqual([
      'end',
    ])
  })

  it('порядок дат проверяется и в запусках курса', () => {
    const course = {
      id: 'stats-course',
      position: 'hse-teacher',
      title: { ru: 'Статистика' },
      runs: [{ start: '2024-01', end: '2023-06' }],
    }
    expect(errorPaths(schemas.courses, course)).toEqual(['runs.0.end'])
  })
})

describe('ссылки между коллекциями', () => {
  it('неизвестный тег — ошибка с названием тега', () => {
    const result = schemas.positions.safeParse({ ...position, tags: ['stats', 'statz'] })
    expect(result.success).toBe(false)
    expect(result.error!.issues[0]!.path).toEqual(['tags', 1])
    expect(result.error!.issues[0]!.message).toContain('statz')
  })

  it('курс должен ссылаться на существующую позицию', () => {
    const course = {
      id: 'stats-course',
      position: 'no-such-position',
      title: { ru: 'Статистика' },
      runs: [{ start: '2024-01' }],
    }
    const result = schemas.courses.safeParse(course)
    expect(result.success).toBe(false)
    expect(result.error!.issues[0]!.path).toEqual(['position'])
    expect(result.error!.issues[0]!.message).toContain('no-such-position')
  })

  it('в словаре тегов лишние поля тоже ошибка', () => {
    expect(
      errorPaths(schemas.tags, { id: 'stats', label: { ru: 'статистика' }, extra: 1 }),
    ).toEqual([''])
  })
})

describe('контакты', () => {
  it('по умолчанию контакт невидим — чтобы телефон не попал на сайт по забывчивости', () => {
    const parsed = schemas.contacts.parse({ id: 'phone', kind: 'phone', url: 'tel:+70000000000' })
    expect(parsed.visible).toBe(false)
    expect(parsed.primary).toBe(false)
  })
})

describe('публикации', () => {
  it('год и номер без кавычек приводятся к нужным типам', () => {
    const parsed = schemas.publications.parse({
      id: 'paper',
      authors: ['Ангельгардт А. Н.'],
      title: 'Название',
      venue: 'Журнал',
      year: '2021',
      issue: 2,
    })
    expect(parsed.year).toBe(2021)
    expect(parsed.issue).toBe('2')
    expect(parsed.status).toBe('published')
  })
})
