import { describe, expect, it } from 'vitest'
import { formatProblems, loadData, validateTexts } from './data-files.ts'

// Минимальный набор файлов, который проходит проверку.
function validTexts(): Record<string, string> {
  return {
    profile: `
name: { ru: "Антон Ангельгардт", en: "Anton Angelgardt" }
authorName: "Ангельгардт"
positioning: { ru: "Преподаю статистику", en: "TODO" }
location: { ru: "Москва", en: "Moscow" }
photo: "src/assets/photo.png"
focusAreas: []
`,
    contacts: `
- id: email
  kind: email
  url: "mailto:someone@example.com"
  visible: true
  primary: true
`,
    tags: `
- id: stats
  label: { ru: "статистика" }
`,
    positions: `
- id: hse-teacher
  kind: teaching
  role: { ru: "преподаватель" }
  organization: { ru: "НИУ ВШЭ" }
  tags: [stats]
`,
    courses: `
- id: stats-course
  position: hse-teacher
  title: { ru: "Статистика" }
  runs:
    - { start: "2023-09", end: "2023-12" }
`,
    skills: `
groups:
  - id: programming
    title: { ru: "Программирование" }
    items:
      - { ru: "R" }
`,
    interests: 'groups: []',
  }
}

function problemsOf(texts: Record<string, string>): string[] {
  return validateTexts(texts).problems.map((p) => [p.file, p.id, p.field].join(' | '))
}

describe('validateTexts', () => {
  it('правильные данные проходят без замечаний, пустые файлы допустимы', () => {
    const { problems, data } = validateTexts(validTexts())
    expect(problems).toEqual([])
    expect(data.positions).toHaveLength(1)
    expect(data.projects).toEqual([])
    expect(data.skills[0]).toMatchObject({ id: 'programming', hidden: false })
  })

  it('неверная дата: названы файл, id записи и поле', () => {
    const texts = validTexts()
    texts.courses = texts.courses!.replace('"2023-12"', '"2023-13"')
    expect(problemsOf(texts)).toEqual(['src/data/courses.yaml | stats-course | runs.0.end'])
  })

  it('неизвестный тег', () => {
    const texts = validTexts()
    texts.positions = texts.positions!.replace('[stats]', '[statz]')
    const { problems } = validateTexts(texts)
    expect(problemsOf(texts)).toEqual(['src/data/positions.yaml | hse-teacher | tags.0'])
    expect(problems[0]!.message).toContain('statz')
  })

  it('ссылка на несуществующую позицию', () => {
    const texts = validTexts()
    texts.courses = texts.courses!.replace('position: hse-teacher', 'position: msu-teacher')
    const { problems } = validateTexts(texts)
    expect(problemsOf(texts)).toEqual(['src/data/courses.yaml | stats-course | position'])
    expect(problems[0]!.message).toContain('msu-teacher')
  })

  it('дата без кавычек не ошибка', () => {
    const texts = validTexts()
    texts.courses = texts.courses!.replace('start: "2023-09", end: "2023-12"', 'start: 2023')
    const { problems, data } = validateTexts(texts)
    expect(problems).toEqual([])
    expect(data.courses[0]).toMatchObject({ runs: [{ start: '2023' }] })
  })

  it('повтор id', () => {
    const texts = validTexts()
    texts.tags += '\n- id: stats\n  label: { ru: "ещё раз" }\n'
    expect(problemsOf(texts)).toEqual(['src/data/tags.yaml | stats | id'])
  })

  it('нет основного контакта', () => {
    const texts = validTexts()
    texts.contacts = texts.contacts!.replace('primary: true', 'primary: false')
    const { problems } = validateTexts(texts)
    expect(problems).toHaveLength(1)
    expect(problems[0]).toMatchObject({ file: 'src/data/contacts.yaml' })
    expect(problems[0]!.message).toContain('нет основного')
  })

  it('синтаксическая ошибка YAML: назван файл и строка', () => {
    const texts = validTexts()
    texts.tags = '- id: stats\n  label: { ru: "статистика"\n'
    const { problems } = validateTexts(texts)
    // одна ошибка, без каскада «тег не найден» по всем остальным файлам
    expect(problems).toHaveLength(1)
    expect(problems[0]).toMatchObject({ file: 'src/data/tags.yaml' })
    expect(problems[0]!.message).toMatch(/строка \d+/)
  })

  it('файл не того вида', () => {
    const texts = validTexts()
    texts.tags = 'id: stats'
    texts.positions = '[]'
    texts.courses = '[]'
    expect(validateTexts(texts).problems[0]!.message).toContain('список записей')
  })

  it('formatProblems собирает понятное сообщение', () => {
    const message = formatProblems([
      { file: 'src/data/courses.yaml', id: 'stats-course', field: 'runs.0.end', message: 'Плохо' },
      { file: 'src/data/contacts.yaml', message: 'нет основного контакта' },
    ])
    expect(message).toContain('src/data/courses.yaml → stats-course → runs.0.end: Плохо')
    expect(message).toContain('src/data/contacts.yaml: нет основного контакта')
  })
})

describe('данные сайта', () => {
  it('все файлы из src/data проходят проверку', () => {
    const { problems } = loadData()
    expect(formatProblems(problems)).toBe('')
  })
})
