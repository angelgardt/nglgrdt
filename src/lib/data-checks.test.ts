import { describe, expect, it } from 'vitest'
import { checkPrimaryContact, findDuplicateIds } from './data-checks.ts'

describe('findDuplicateIds', () => {
  it('возвращает пустой список, если повторов нет', () => {
    expect(findDuplicateIds([{ id: 'a' }, { id: 'b' }])).toEqual([])
  })

  it('называет каждый повторяющийся id один раз', () => {
    expect(findDuplicateIds([{ id: 'a' }, { id: 'b' }, { id: 'a' }, { id: 'a' }])).toEqual(['a'])
  })

  it('пропускает записи без id — на них укажет схема', () => {
    expect(findDuplicateIds([{}, {}, null, 'x'])).toEqual([])
  })
})

describe('checkPrimaryContact', () => {
  it('принимает ровно один основной видимый контакт', () => {
    const contacts = [
      { id: 'email', primary: true, visible: true },
      { id: 'phone', visible: false },
    ]
    expect(checkPrimaryContact(contacts)).toBeNull()
  })

  it('сообщает, если основного контакта нет', () => {
    expect(checkPrimaryContact([{ id: 'email', visible: true }])).toMatch(/нет основного/)
  })

  it('сообщает, если основных контактов несколько', () => {
    const contacts = [
      { id: 'email', primary: true, visible: true },
      { id: 'telegram', primary: true, visible: true },
    ]
    expect(checkPrimaryContact(contacts)).toMatch(/email, telegram/)
  })

  it('сообщает, если основной контакт скрыт', () => {
    expect(checkPrimaryContact([{ id: 'email', primary: true, visible: false }])).toMatch(
      /email.*visible/,
    )
    expect(checkPrimaryContact([{ id: 'email', primary: true }])).toMatch(/email.*visible/)
    expect(
      checkPrimaryContact([{ id: 'email', primary: true, visible: true, hidden: true }]),
    ).toMatch(/email.*hidden/)
  })
})
