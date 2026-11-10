// npm run i18n:report — какие текстовые поля данных ещё не переведены на английский.

import { formatProblems, loadData } from '../src/lib/data-files.ts'
import { buildReport, formatReport } from '../src/lib/i18n-report.ts'

const { data, problems } = loadData()
if (problems.length > 0) {
  console.error(`Сначала исправьте ошибки в данных:\n${formatProblems(problems)}`)
  process.exit(1)
}

console.log(formatReport(buildReport(data)))
