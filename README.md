# nglgrdt

CV-сайт Антона Ангельгардта. Статический сайт на [Astro](https://astro.build), публикуется на <https://angelgardt.github.io/nglgrdt/>.

Сейчас на сайте заглушка и страница просмотра данных без оформления: идёт итерация 1 из [ТЗ](docs/spec.md).

## Быстрый старт

Нужен Node.js 24 (версия записана в `.nvmrc`).

```bash
git clone git@github.com:angelgardt/nglgrdt.git
cd nglgrdt
nvm use
npm install
npm run dev
```

Сайт откроется на <http://localhost:4321/nglgrdt/>.

## Команды

| Команда               | Что делает                                     |
| --------------------- | ---------------------------------------------- |
| `npm run dev`         | локальный сервер с автообновлением             |
| `npm run check`       | проверка типов                                 |
| `npm test`            | unit-тесты                                     |
| `npm run build`       | сборка в папку `dist/`                         |
| `npm run preview`     | просмотр собранного сайта                      |
| `npm run format`      | форматирование кода (Prettier)                 |
| `npm run i18n:report` | какие тексты ещё не переведены на английский   |
| `npm run schemas`     | обновить подсказки редактора для файлов данных |

Перед коммитом: `npm run check && npm test && npm run build`.

## Публикация

Push в ветку `master` запускает GitHub Actions: проверка, тесты, сборка и публикация на GitHub Pages. В pull request выполняются те же проверки, но без публикации. Работа идёт в ветках, в `master` — только через pull request.

## Документы

- [docs/spec.md](docs/spec.md) — ТЗ и план итераций
- [docs/content.md](docs/content.md) — файлы данных и их поля
- [docs/decisions.md](docs/decisions.md) — журнал решений
- [migration/REPORT.md](migration/REPORT.md) — отчёт миграции со старого сайта
- [CLAUDE.md](CLAUDE.md) — правила проекта для Claude Code

Остальная документация появится в итерации 4.
