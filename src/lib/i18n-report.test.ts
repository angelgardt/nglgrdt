import { describe, expect, it } from 'vitest'
import { buildReport, collectTextFields, formatReport } from './i18n-report.ts'

describe('collectTextFields', () => {
  it('находит текстовые поля на любой глубине и называет путь к ним', () => {
    const entry = {
      id: 'hse-psy',
      level: 'bachelor',
      university: { ru: 'НИУ ВШЭ', en: 'HSE University' },
      thesis: { title: { ru: 'Название' }, supervisor: { name: { ru: 'Имя', en: 'Name' } } },
      items: [{ ru: 'R', en: 'R' }, { ru: 'анализ данных' }],
    }
    expect(collectTextFields(entry)).toEqual([
      { field: 'university', status: 'ok' },
      { field: 'thesis.title', status: 'missing' },
      { field: 'thesis.supervisor.name', status: 'ok' },
      { field: 'items.0', status: 'ok' },
      { field: 'items.1', status: 'missing' },
    ])
  })

  it('TODO в en или ru — отдельный статус', () => {
    const entry = { positioning: { ru: 'Преподаю', en: 'TODO' }, text: { ru: 'TODO', en: 'TODO' } }
    expect(collectTextFields(entry).map((f) => f.status)).toEqual(['todo', 'todo'])
  })

  it('обычные строки и служебные поля не считаются текстом', () => {
    expect(
      collectTextFields({ id: 'x', notes: 'заметка', tags: ['stats'], url: 'https://x' }),
    ).toEqual([])
  })
})

describe('buildReport', () => {
  const data = {
    profile: [{ name: { ru: 'Антон', en: 'Anton' }, positioning: { ru: 'Преподаю', en: 'TODO' } }],
    positions: [
      { id: 'a', hidden: false, role: { ru: 'преподаватель', en: 'Teacher' } },
      { id: 'b', hidden: false, role: { ru: 'ассистент' }, unit: { ru: 'кафедра' } },
    ],
    materials: [{ id: 'm', hidden: true, title: { ru: 'Курс' } }],
  }

  it('считает покрытие только по видимым записям', () => {
    const report = buildReport(data)
    // 5 полей у видимых записей, перевод есть у двух: name и role записи a
    expect(report.total).toBe(5)
    expect(report.translated).toBe(2)
    expect(report.coverage).toBe(40)
  })

  it('TODO идут отдельным списком, пропуски сгруппированы по файлам и записям', () => {
    const report = buildReport(data)
    expect(report.todo).toEqual([{ file: 'profile', id: 'profile', field: 'positioning' }])
    expect(report.missing).toEqual([{ file: 'positions', id: 'b', fields: ['role', 'unit'] }])
  })

  it('formatReport выводит TODO раньше пропусков и процент в конце', () => {
    const text = formatReport(buildReport(data))
    expect(text.indexOf('positioning')).toBeLessThan(text.indexOf('role, unit'))
    expect(text).toContain('src/data/positions.yaml')
    expect(text.trimEnd().split('\n').at(-1)).toContain('40%')
  })

  it('пустые данные дают 100%', () => {
    expect(buildReport({}).coverage).toBe(100)
  })
})
