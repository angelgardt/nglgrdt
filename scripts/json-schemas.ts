// npm run schemas — обновляет JSON Schema в src/data/schemas.
// Обычно запускать не нужно: схемы обновляются сами при npm run dev, check и build.

import { loadData } from '../src/lib/data-files.ts'
import { writeJsonSchemas } from '../src/lib/json-schemas.ts'

// Списки тегов и позиций берём из данных, даже если в них есть другие ошибки.
const { data } = loadData()
const changed = writeJsonSchemas({
  tagIds: data.tags.map((tag) => String(tag.id)),
  positionIds: data.positions.map((position) => String(position.id)),
})

console.log(changed.length > 0 ? `Обновлено:\n${changed.join('\n')}` : 'Схемы уже актуальны')
