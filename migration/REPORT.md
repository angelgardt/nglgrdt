# Отчёт миграции (итерация 1)

Старое CV перенесено в `src/data/*.yaml`. Этот отчёт — список того, что нужно проверить и утвердить владельцу (задача #11). Пока он не просмотрен, итерация 2 не начинается.

Посмотреть данные в браузере: `npm run dev` → <http://localhost:4321/nglgrdt/ru/data/>. В режиме разработки там видны и скрытые записи, и заметки. На опубликованном сайте та же страница показывает только видимое.

## 1. Что нужно решить

- [ ] Группировка курсов по позициям — раздел «Группировка курсов по позициям».
- [ ] Теги каждой записи и словарь тегов в `tags.yaml` — раздел «Предложенные теги». Теги уже стоят в YAML, их можно править прямо там.
- [ ] Кандидаты в `featured` — раздел «Кандидаты в featured». В YAML флаг не выставлен ни у одной записи.
- [ ] Пять записей «по настоящее время» — раздел «Записи „по настоящее время“». На старом сайте (июль 2024) они открыты; поставьте даты окончания там, где работа закончилась.
- [ ] Опечатки — раздел 5. В данных они оставлены как в источнике.
- [ ] GPA магистратуры: 8.44 или 8.66 (задача #12).
- [ ] Вопросы из раздела 4.

## 2. Источники

| Источник                                   | Что взято                                    |
| ------------------------------------------ | -------------------------------------------- |
| `a/ru/angelgardt.html`                     | весь русский текст                           |
| `a/ru/index.html`                          | список материалов                            |
| `a/en/angelgardt.html`                     | только поля `en`                             |
| `migration/sources/{ru,en}/education.json` | `department` и `qualification` в образовании |
| `a/imgs/photo.png`                         | фото → `src/assets/photo.png`                |

Старый сайт взят из ветки `master` репозитория angelgardt/angelgardt.github.io, коммит `a6baa59`. Копии трёх HTML-файлов лежат в `migration/sources/old-site/`, чтобы любое значение можно было сверить. Перенос выполнен скриптом `migration/migrate.py`: он копирует тексты из HTML без изменений.

## 3. Как старые разделы легли в файлы

- **Организация и подразделение.** Строка «департамент психологии, Национальный исследовательский университет „Высшая школа экономики“» разделена на `unit` и `organization`. Так сделано для ВШЭ и РАНХиГС; остальные организации записаны целиком в `organization`.
- **Преподавание.** Запись старого сайта — это один запуск курса. Запуски собраны в курсы, курсы — в позиции по паре «роль + подразделение». Слово «курс» перед названием убрано, кавычки оставлены. Обязанности лежат в `runs[].duties`.
- **Поле `context` у позиций.** У 11 записей на старом сайте, кроме организации, указано мероприятие или курс («Весенняя Психологическая Школа», «Семинар по когнитивным исследованиям»). В модели данных из ТЗ для этого нет поля, поэтому я добавил необязательное `context`. Это отступление от ТЗ, см. раздел 4.
- **Образование.** Тексты взяты со старого сайта вместе с подписями: «образовательная программа … (магистратура)», «специальность 45.04.03 …». В прототипе те же поля записаны короче («„Психология“», «37.03.01 „Психология“») — выберите, какой вид оставить.
- **Дополнительное образование.** Вторая строка записи пошла в `organizer`, у MOOC — в `platform`, у EdCrunch («трек …») — в `track`.
- **Достижения.** Верхняя подпись пошла в `context`, нижняя — в `organization`. У олимпиад единственная подпись («участник», «призёр», «победитель») записана в `context`.
- **Публикации.** Строка разобрана на авторов, название, издание, год, номер и страницы.
- **Конференции.** «доклад» и «постерный доклад» стали `talkType`, город — `location`.
- **Материалы.** Две записи из «Авторских прав» и 12 ссылок со старой главной: одна ссылка — одна запись. Заголовок блока главной записан в `context`, строка под ним — в `description`. Ссылки сделаны полными (`https://angelgardt.github.io/...`). Все 14 записей скрыты.
- **Контакты.** Видимы почта, Telegram и LinkedIn. Ссылки на GitHub на старом сайте нет — контакт не создан.
- **Профиль.** Имя и город — со старого сайта. Позиционирование и названия направлений — временные, из раздела 13 ТЗ. Тексты карточек и английские варианты — `TODO`.

**Не перенесено:**

- дата рождения и возраст;
- пустые ссылки TikTok и YouTube в шапке;
- закомментированные блоки «текущая должность» в шапке;
- четыре интереса, скрытые на старом сайте;
- описание позиции онлайн-тьютора: на старом сайте оно скрыто, поэтому лежит в `notes`, а не в `description`;
- ссылки на шрифт в подвале.

## 4. Расхождения и вопросы

1. **GPA магистратуры.** На старом сайте 8.44 (и значение там скрыто), в прототипе 8.66. В YAML записано 8.44, пометка — в `notes` записи `hse-ling`.
2. **«Специалитет [не окончен]».** Так записан уровень третьего образования в прототипе; на старом сайте пометки нет. В YAML — `level: specialist` без пометки, текст вынесен в `notes`. Если это нужно показывать, скажите как.
3. **Поле `context` у позиций** добавлено сверх ТЗ. Альтернатива — дописывать мероприятие в `unit`.
4. **Записи без дат.** У двух позиций «приглашённый преподаватель» вместо дат стоит «по запросу организаторов». Дат в YAML нет, исходная строка — в `notes`. Как показывать такие записи и куда их сортировать, нужно решить до итерации 3.
5. **«осень 2017 — осень 2019».** Формат дат не знает сезонов. Записано `2017`–`2019`, исходная строка — в `notes`.
6. **«25 декабря — 12 февраля 2018»** (курс «Основы веб-дизайна»). Год начала на сайте не указан; записано `2017-12-25`, потому что иначе начало позже конца. Проверьте.
7. **Материалы дублируются.** «Анализ данных + R: мир линейных моделей» есть и в «Авторских правах», и блоком на старой главной (книга, лекции, практика). Записи не объединял.
8. **Курс и координация курса — разные записи.** Например, `uxlab-wlm` (преподавание) и `wlm-2021-coordinator` (менеджмент). Так было на старом сайте.
9. **Автор в публикациях.** `authorName` — «Ангельгардт», но в англоязычной публикации автор записан как «Angelgardt A.». Правило выделения автора понадобится в итерации 3.
10. **Английский файл прототипа не переведён:** в `migration/sources/en/education.json` русский текст. Из него ничего не взято.

## 5. Опечатки и неровности — только предложения

В данных всё оставлено как в источнике.

**Русский текст**

| Где                                                                 | Сейчас                                             | Предложение                            |
| ------------------------------------------------------------------- | -------------------------------------------------- | -------------------------------------- |
| positions → `hse-uxlab-research-intern` → description               | в регулярных рабочих собрания                      | собраниях                              |
| courses → `uxlab-wlm` → runs.0.duties                               | проверка домашних работы слушателей                | домашних работ                         |
| achievements → `hse-psy-academic-council` → title                   | образовательной прогаммы                           | программы                              |
| materials → `andan-logit-transformation` → title                    | с помощю                                           | с помощью                              |
| materials → `psyhse-ggplot2-2021`, `appcogsci-ggplot2-2022` → title | ggplo2                                             | ggplot2                                |
| extra-education, три записи «Летней школы» → organizer              | школа семинар                                      | школа-семинар (как в четвёртой записи) |
| courses → `hse-human-digital-interaction` → title                   | человек-цифрового взаимодействия                   | человеко-цифрового (как в интересах)   |
| conferences → `duncker-2019` → event                                | молодых ученых                                     | учёных (как в остальных записях)       |
| conferences → `bruner-2021` → event                                 | Дж.С. Брунера                                      | Дж. С. Брунера                         |
| positions → `profilum-product-researcher` → description             | отчетов                                            | отчётов                                |
| publications → `hybrid-search-category-2021` → pages                | 148-158                                            | 148–158 (тире)                         |
| education → оценки                                                  | “отлично” в четырёх местах, «отлично» в двух       | единые кавычки                         |
| education → thesis.title                                            | у магистерской без кавычек, у бакалаврской в «»    | единый вид                             |
| extra-education → `ipras-network-analysis-2020`                     | название и организация по-английски в русском поле | перевести или оставить                 |

**Английский текст** (поля `en`)

| Где                                                      | Сейчас                  | Предложение           |
| -------------------------------------------------------- | ----------------------- | --------------------- |
| positions → `profilum-product-researcher` → organization | Profulim                | Profilum              |
| positions → `uxlab-cogsem-coordinator` → role            | Event Administator      | Administrator         |
| positions → `wlm-2021-coordinator` → description         | comunicating            | communicating         |
| positions → `sps-2020-program-head` → description        | develompent, theachers  | development, teachers |
| positions → `uxlab-designer` → description               | reccurent               | recurrent             |
| positions → `hse-lyceum-guest-lecturer` → unit           | HSE Liceum              | HSE Lyceum            |
| positions → `appcogsci-2021-program-head` → context      | Summer school ”Applied… | открывающая кавычка “ |
| extra-education → `hse-nlp-webinar-2020` → organizer     | Continuning             | Continuing            |
| languages → `ukrainian` → name                           | Ukranian                | Ukrainian             |
| conferences → `psychology-xxi-2021` → talkTitle          | calegory                | category              |
| achievements → три олимпиады → context                   | Prizer                  | Prize winner          |

Английское описание продуктового исследователя («Профилум») заметно короче русского — это не полный перевод.

## 6. Перевод

`npm run i18n:report` на момент миграции: **переведено 369 из 434 текстовых полей видимых записей — 85%**. Семь обязательных полей визитки заполнены строкой `TODO`: позиционирование, три названия и три текста направлений.

Английский текст переносился только к записям, которые однозначно совпали с русскими: в том же разделе, с теми же датами. Что не совпало — в разделах «Английские записи без пары» и «Английские тексты, пропущенные намеренно» ниже. Две английские публикации не перенесены: поля публикаций одноязычные, и одна из них — перевод уже перенесённой статьи, а второй («Perceptual characteristics…», на рецензии) в русском CV нет.

## 7. Как сверять числа

В таблице «Число записей» правая колонка совпадает со счётчиками «Показано записей: N из M» на странице `/ru/data/` в режиме разработки. На опубликованной странице счётчики меньше у контактов (3 из 9) и материалов (0 из 14): остальное скрыто.

---

Дальше — таблицы, собранные скриптом миграции.

## Число записей

| Раздел старого сайта                                       | Записей там         | В YAML                               | Пояснение                                                                            |
| ---------------------------------------------------------- | ------------------- | ------------------------------------ | ------------------------------------------------------------------------------------ |
| Опыт работы → Преподавательская деятельность               | 18                  | позиций: 6, курсов: 12, запусков: 17 | 18 записей старого сайта = 17 запусков курсов + 1 позиция без курсов (онлайн-тьютор) |
| Опыт работы → Исследовательская деятельность               | 1                   | позиций: 1                           |                                                                                      |
| Опыт работы → Академическая деятельность                   | 1                   | позиций: 1                           |                                                                                      |
| Опыт работы → Административная и менеджерская деятельность | 13                  | позиций: 13                          |                                                                                      |
| Опыт работы → Другое                                       | 6                   | позиций: 6                           |                                                                                      |
| Образование                                                | 3                   | записей: 3                           |                                                                                      |
| Дополнительное образование → Повышение квалификации        | 4                   | записей: 4                           |                                                                                      |
| Дополнительное образование → Школы / Вебинары / Курсы      | 16                  | записей: 16                          |                                                                                      |
| Дополнительное образование → MOOCs                         | 11                  | записей: 11                          |                                                                                      |
| Достижения                                                 | 15                  | записей: 15                          |                                                                                      |
| Владение языками                                           | 8                   | записей: 8                           |                                                                                      |
| Навыки                                                     | 50 пунктов          | 6 групп, 4 подгруппы, 50 пунктов     |                                                                                      |
| Интересы                                                   | 33 пунктов          | 2 группы, 29 пунктов                 | 4 пункта скрыты на старом сайте и не перенесены (список — в разделе 7)               |
| Исследования → Публикации                                  | 3                   | записей: 3                           |                                                                                      |
| Исследования → Конференции                                 | 4                   | записей: 4                           |                                                                                      |
| Исследования → Гранты                                      | 1                   | записей: 1                           |                                                                                      |
| Проекты                                                    | 0                   | 0 записей                            | раздел на старом сайте скрыт и пуст                                                  |
| Авторские права                                            | 2                   | 2 записи в materials                 | все с hidden: true                                                                   |
| Старая главная: список материалов                          | 6 блоков, 12 ссылок | 12 записей в materials               | одна ссылка = одна запись; все с hidden: true                                        |
| Шапка: контакты                                            | 11                  | записей: 9                           | не перенесены пустые ссылки: tiktok, youtube                                         |

## Группировка курсов по позициям

- **`hse-psy-teacher`** — преподаватель, департамент психологии, Национальный исследовательский университет «Высшая школа экономики»
  - `hse-nis-applied-data-analysis` — «Научно-исследовательский семинар: Прикладной анализ данных в психологии»: 2024-01—2024-06; 2023-01—2023-06; 2022-01—2022-06
  - `hse-nis-diagnostic-tools` — «Научно-исследовательский семинар: Разработка, адаптация и валидизация диагностических инструментов в психологии»: 2023-10—2024-03; 2022-10—2023-03
  - `hse-statistics-for-data-analysis` — «Статистика для анализа данных»: 2023-09—2023-12; 2022-09—2022-12
  - `hse-human-digital-interaction` — «Психология человек-цифрового взаимодействия»: 2023-09—2023-10
- **`ranepa-teacher`** — преподаватель, Институт общественных наук, РАНХиГС
  - `ranepa-modern-data-analysis` — «Современные методы анализа данных»: 2023-09—2024-01
- **`middlebury-tutor`** — онлайн-тьютор, Middlebury Institute of International Studies at Monterey, CA
  - без курсов: позиция перенесена одной записью
- **`hse-psy-teaching-assistant`** — учебный ассистент, департамент психологии, Национальный исследовательский университет «Высшая школа экономики»
  - `hse-psychodiagnostics-practicum` — «Психологический практикум: Психодиагностика и основы психометрики»: 2021-01—2021-06
  - `hse-intro-psychology` — «Введение в психологию»: 2020-09—2020-12; 2019-09—2019-10
  - `hse-nis-data-visualization` — «Научно-исследовательский семинар: Анализ и визуализация данных в психологии»: 2020-01—2020-06
- **`hse-uxlab-teacher`** — преподаватель, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики»
  - `uxlab-wlm` — «Анализ данных + R: мир линейных моделей»: 2021-01—2021-05 (роль: автор курса, преподаватель)
  - `uxlab-andan` — «Анализ данных + R: от t-теста до моделей со смешанными эффектами»: 2020-01—2020-04
  - `uxlab-psychopy` — «Основы построения экспериментов в PsychoPy»: 2019-04—2019-05
- **`hse-math-teaching-assistant`** — учебный ассистент, кафедра высшей математики, Национальный исследовательский университет «Высшая школа экономики»
  - `hse-math-stat-methods` — «Математические и статистические методы в психологии»: 2019-01—2019-06

## Предложенные теги

| Файл            | id                                   | Теги                                      |
| --------------- | ------------------------------------ | ----------------------------------------- |
| positions       | `hse-psy-teacher`                    | teaching                                  |
| positions       | `ranepa-teacher`                     | teaching                                  |
| positions       | `middlebury-tutor`                   | teaching, linguistics                     |
| positions       | `hse-psy-teaching-assistant`         | teaching                                  |
| positions       | `hse-uxlab-teacher`                  | teaching                                  |
| positions       | `hse-math-teaching-assistant`        | teaching                                  |
| positions       | `profilum-product-researcher`        | ux-research, research-design, stats       |
| positions       | `hse-uxlab-research-intern`          | cognitive, psychometrics, research-design |
| positions       | `uxlab-brand-manager`                | management                                |
| positions       | `uxlab-cogsem-coordinator`           | management                                |
| positions       | `uxlab-junior-manager`               | management                                |
| positions       | `uxlab-smm-head`                     | management                                |
| positions       | `appcogsci-2021-program-head`        | management, teaching                      |
| positions       | `wlm-2021-coordinator`               | management                                |
| positions       | `sps-2021-program-deputy-head`       | management, teaching                      |
| positions       | `psyhse-2019-organizer`              | management                                |
| positions       | `appcogsci-2020-program-head`        | management, teaching                      |
| positions       | `andan-2020-coordinator`             | management                                |
| positions       | `sps-2020-program-head`              | management, teaching                      |
| positions       | `psychopy-2019-coordinator`          | management                                |
| positions       | `sps-2019-extracurricular-head`      | management                                |
| positions       | `uxlab-designer`                     | —                                         |
| positions       | `uxlab-site-editor`                  | —                                         |
| positions       | `sps-guest-lecturer`                 | teaching                                  |
| positions       | `hse-lyceum-guest-lecturer`          | teaching                                  |
| positions       | `student-org-committee-head`         | management                                |
| positions       | `thevyshka-proofreader`              | —                                         |
| courses         | `hse-nis-applied-data-analysis`      | stats, teaching                           |
| courses         | `hse-nis-diagnostic-tools`           | psychometrics, teaching                   |
| courses         | `hse-statistics-for-data-analysis`   | stats, teaching                           |
| courses         | `hse-human-digital-interaction`      | cognitive, ux-research, teaching          |
| courses         | `ranepa-modern-data-analysis`        | stats, teaching                           |
| courses         | `hse-psychodiagnostics-practicum`    | psychometrics, teaching                   |
| courses         | `uxlab-wlm`                          | stats, teaching                           |
| courses         | `hse-intro-psychology`               | teaching                                  |
| courses         | `hse-nis-data-visualization`         | stats, teaching                           |
| courses         | `uxlab-andan`                        | stats, teaching                           |
| courses         | `hse-math-stat-methods`              | stats, teaching                           |
| courses         | `uxlab-psychopy`                     | research-design, teaching                 |
| education       | `hse-ling`                           | linguistics                               |
| education       | `hse-psy`                            | —                                         |
| education       | `pspbgmu-med`                        | —                                         |
| extra-education | `focus-groups-2024`                  | ux-research, research-design              |
| extra-education | `teach-for-hse-group-work-2021`      | teaching                                  |
| extra-education | `hse-digital-communications-2021`    | —                                         |
| extra-education | `teach-for-hse-presentations-2020`   | teaching                                  |
| extra-education | `letnyaya-shkola-education-2023`     | teaching                                  |
| extra-education | `appcogsci-2023`                     | cognitive                                 |
| extra-education | `spbu-winter-school-2023`            | cognitive                                 |
| extra-education | `appcogsci-2022`                     | cognitive                                 |
| extra-education | `edcrunch-2021`                      | teaching                                  |
| extra-education | `letnyaya-shkola-education-2021`     | teaching                                  |
| extra-education | `appcogsci-2021`                     | cognitive                                 |
| extra-education | `hse-nlp-webinar-2020`               | linguistics                               |
| extra-education | `appcogsci-2020`                     | cognitive                                 |
| extra-education | `ipras-network-analysis-2020`        | cognitive, linguistics                    |
| extra-education | `letnyaya-shkola-testing-2020`       | psychometrics                             |
| extra-education | `duncker-school-2019`                | cognitive                                 |
| extra-education | `letnyaya-shkola-andan-2019`         | stats                                     |
| extra-education | `appcogsci-2019`                     | cognitive                                 |
| extra-education | `highlights-web-design-2018`         | —                                         |
| extra-education | `hse-management-psychology-2018`     | management                                |
| extra-education | `udemy-machine-learning`             | stats                                     |
| extra-education | `udemy-python-developer`             | —                                         |
| extra-education | `stepik-git`                         | —                                         |
| extra-education | `fructcode-php-mysql`                | —                                         |
| extra-education | `fructcode-javascript-jquery`        | —                                         |
| extra-education | `fructcode-html-css`                 | —                                         |
| extra-education | `stepik-javascript`                  | —                                         |
| extra-education | `stepik-r-data-analysis-2`           | stats                                     |
| extra-education | `stepik-r-data-analysis`             | stats                                     |
| extra-education | `stepik-r-programming`               | stats                                     |
| extra-education | `coursera-latex`                     | —                                         |
| achievements    | `hse-psy-academic-council`           | teaching                                  |
| achievements    | `hse-psy-gratitude-2022`             | teaching                                  |
| achievements    | `hse-talent-pool-2022`               | —                                         |
| achievements    | `hse-best-research-paper-2021`       | psychometrics                             |
| achievements    | `hse-psy-gratitude-2021`             | —                                         |
| achievements    | `psyhse-ggplot2-gratitude-2021`      | stats, teaching                           |
| achievements    | `hse-student-council-gratitude-2018` | —                                         |
| achievements    | `olympiad-chemistry-final-2014`      | —                                         |
| achievements    | `olympiad-chemistry-regional-2014`   | —                                         |
| achievements    | `olympiad-biology-regional-2014`     | —                                         |
| achievements    | `olympiad-biology-final-2013`        | —                                         |
| achievements    | `olympiad-biology-regional-2013`     | —                                         |
| achievements    | `olympiad-chemistry-regional-2013`   | —                                         |
| achievements    | `olympiad-biology-regional-2012`     | —                                         |
| achievements    | `olympiad-chemistry-regional-2012`   | —                                         |
| conferences     | `bruner-2021`                        | cognitive                                 |
| conferences     | `psychology-xxi-2021`                | cognitive                                 |
| conferences     | `psyhse-2019`                        | cognitive, ux-research                    |
| conferences     | `duncker-2019`                       | cognitive, ux-research                    |
| grants          | `rsf-20-78-10055`                    | cognitive                                 |
| publications    | `visual-search-erp-2023`             | cognitive                                 |
| publications    | `trust-assessment-tool-2021`         | psychometrics                             |
| publications    | `hybrid-search-category-2021`        | cognitive                                 |
| materials       | `wlm-2023-course`                    | stats, teaching                           |
| materials       | `wlm-2021-course`                    | stats, teaching                           |
| materials       | `ggplot2-master-class-2020`          | stats, teaching                           |
| materials       | `andan-matrices`                     | stats, teaching                           |
| materials       | `andan-glm-binomial`                 | stats, teaching                           |
| materials       | `andan-logit-transformation`         | stats, teaching                           |
| materials       | `andan-mixed-models`                 | stats, teaching                           |
| materials       | `andan-pca-fa`                       | stats, teaching                           |
| materials       | `wlm-2021-book`                      | stats, teaching                           |
| materials       | `wlm-2021-lectures`                  | stats, teaching                           |
| materials       | `wlm-2021-practice`                  | stats, teaching                           |
| materials       | `psyhse-ggplot2-2021`                | stats, teaching                           |
| materials       | `appcogsci-ggplot2-2022`             | stats, teaching                           |
| materials       | `duncker-rmarkdown-2022`             | teaching                                  |

## Кандидаты в featured

- `positions` / `hse-psy-teacher` — преподаватель
- `positions` / `ranepa-teacher` — преподаватель
- `positions` / `profilum-product-researcher` — продуктовый исследователь
- `positions` / `hse-uxlab-research-intern` — стажёр-исследователь
- `education` / `hse-ling` — образовательная программа «Русский язык как иностранный во взаимодействии языков и культур» (магистратура)
- `education` / `hse-psy` — образовательная программа «Психология» (бакалавриат)

## Записи «по настоящее время»

- онлайн-тьютор, Middlebury Institute of International Studies at Monterey, CA (октябрь 2021 — наст. вр.) — «октябрь 2021 — наст. вр.»
- бренд-менеджер, редактор-корректор, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (август 2021 — наст. вр.) — «август 2021 — наст. вр.»
- координатор мероприятия, Семинар по когнитивным исследованиям (сентябрь 2018 — наст. вр.) — «сентябрь 2018 — наст. вр.»
- дизайнер, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (июнь 2018 — наст. вр.) — «июнь 2018 — наст. вр.»
- редактор сайта подразделения, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (сентябрь 2019 — наст. вр) — «сентябрь 2019 — наст. вр»

## Записи, помеченные на старом сайте как текущие (класс current_item)

- преподаватель, курс «Научно-исследовательский семинар: Прикладной анализ данных в психологии» (январь — июнь 2024)
- преподаватель, курс «Научно-исследовательский семинар: Разработка, адаптация и валидизация диагностических инструментов в психологии» (октябрь 2023 — март 2024)
- преподаватель, курс «Статистика для анализа данных» (сентябрь — декабрь 2023)
- преподаватель, курс «Психология человек-цифрового взаимодействия» (сентябрь — октябрь 2023)
- преподаватель, курс «Современные методы анализа данных» (сентябрь 2023 — январь 2024)
- продуктовый исследователь, Профилум (октябрь 2023 — май 2024)
- стажёр-исследователь, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (июнь 2018 — октябрь 2023)
- бренд-менеджер, редактор-корректор, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (август 2021 — наст. вр.)
- координатор мероприятия, Семинар по когнитивным исследованиям (сентябрь 2018 — наст. вр.)
- дизайнер, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (июнь 2018 — наст. вр.)
- редактор сайта подразделения, лаборатория когнитивной психологии пользователя цифровых интерфейсов, Национальный исследовательский университет «Высшая школа экономики» (сентябрь 2019 — наст. вр)

## Нестандартные даты

- без дат («по запросу организаторов»): приглашённый преподаватель, Весенняя Психологическая Школа (по запросу организаторов)
- без дат («по запросу организаторов»): приглашённый преподаватель, Лицей НИУ ВШЭ, Национальный исследовательский университет «Высшая школа экономики» (по запросу организаторов)
- сезон вместо месяца, оставлены годы: глава подразделения организационного комитета мероприятия, независимая студенческая организация (осень 2017 — осень 2019)
- год начала выведен из дат: курс «Основы веб-дизайна» (25 декабря — 12 февраля 2018)

## Расхождения со старым прототипом (education.json)

- `hse-ling`: GPA на старом сайте 8.44 / 10, в прототипе 8.66/10
- `pspbgmu-med`: в прототипе уровень «специалитет [не окончен]», на старом сайте пометки нет

## Скрытое на старом сайте

- описание позиции «онлайн-тьютор» (Middlebury Institute of International Studies at Monterey, CA)
- интерес «компьютерная лингвистика»
- интерес «обработка естественного языка»
- интерес «психология человеко-машинного взаимодействия»
- интерес «доверие к техническим интеллектуальным системам»
- закомментированный блок: «стажёр-исследователь бренд-менеджер дизайнер лаборатория когнитивной психологии пользователя цифровых интерфейсов, НИУ ВШЭ»
- закомментированный блок: «приглашенный преподаватель Институт общественных наук, РАНХиГС»

## Английские тексты: что перенесено

| Раздел                                                | Записей с парой в английском CV | Всего |
| ----------------------------------------------------- | ------------------------------- | ----- |
| Преподавательская деятельность (записи старого сайта) | 13                              | 18    |
| Исследовательская деятельность                        | 1                               | 1     |
| Академическая деятельность                            | 1                               | 1     |
| Административная и менеджерская деятельность          | 13                              | 13    |
| Другое                                                | 6                               | 6     |
| Образование                                           | 3                               | 3     |
| Дополнительное образование → Повышение квалификации   | 2                               | 4     |
| Дополнительное образование → Школы / Вебинары / Курсы | 11                              | 16    |
| Дополнительное образование → MOOCs                    | 10                              | 11    |
| Достижения                                            | 13                              | 15    |
| Владение языками                                      | 8                               | 8     |
| Навыки (пункты)                                       | 50                              | 50    |
| Интересы (пункты)                                     | 28                              | 29    |
| Конференции                                           | 3                               | 4     |
| Гранты                                                | 1                               | 1     |
| Авторские права                                       | 1                               | 2     |

## Английские записи без пары (не перенесены)

- Publications: Angelgardt, A. N., Makarov I. M., Gorbunova E. S. (2021). Role of calegory level in visual search. Psychology Issues (Russia), 2, 148–158.
- Publications: Angelgardt, A. N., Gorbunova E. S. Perceptual characteristics and familiarity factor of stimulus in interface elements visual search. Experimental Psychology (Russia) [the article is under review]

## Английские тексты, пропущенные намеренно

- Online Tutor: описание «Russian grammar training, Rissian pronunciation training» — русское описание скрыто; поле «course “????????”» — заглушка
- Достижение «Gratitude for Master Class “ggplot2: from basic layer to publishable visualization”»: строки «HSE UX LAB & School of Psychology» и «HSE University» не соответствуют русским («Пси-Вышка: международная конференция молодых учёных» и название подразделений)
- Интерес «психология человеко-цифрового взаимодействия»: в английском списке пары нет

## Блоки старой главной

- Научно-исследовательский семинар: Анализ и визуализация данных в психологии — Департамент психологии, НИУ ВШЭ, 2020: ссылок 1
- Курс «Анализ данных + R: от t-теста до моделей со смешанными эффектами» — HSE UX LAB, НИУ ВШЭ, 2020: ссылок 5
- Курс «Анализ данных + R: мир линейных моделей» — HSE UX LAB, НИУ ВШЭ, 2021: ссылок 3
- Пси-Вышка: Актуальные проблемы психологической науки — Международная конференция молодых учёных, HSE UX LAB & Департамент психологии, НИУ ВШЭ, 2021: ссылок 1
- Летняя школа «Прикладная когнитивная наука» — Летняя школа, HSE UX LAB, НИУ ВШЭ, 2022: ссылок 1
- Летняя когнитивная школа памяти Карла Дункера — ИОН РАНХиГС, 2022: ссылок 1
