#!/usr/bin/env python3
"""Разовая миграция старого CV в src/data/*.yaml.

Источники (только чтение):
  migration/sources/old-site/a/ru/angelgardt.html  — русское CV
  migration/sources/old-site/a/ru/index.html       — старая главная со списком материалов
  migration/sources/old-site/a/en/angelgardt.html  — английское CV, только для полей en
  migration/sources/{ru,en}/education.json         — данные из прототипа на Vue

Тексты копируются из источников без изменений. Всё, что решено при миграции
(id записей, группировка курсов, предложенные теги), задано таблицами в начале файла.

Запуск: python3 migration/migrate.py --force
Без --force скрипт не перезаписывает существующие файлы: после миграции YAML
правится руками, и повторный запуск сотрёт эти правки.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "migration" / "sources"
OUT = ROOT / "src" / "data"

HSE = "Национальный исследовательский университет «Высшая школа экономики»"

# ---------------------------------------------------------------------------
# Таблицы решений миграции
# ---------------------------------------------------------------------------

# Преподавательские позиции: (признак роли, признак подразделения) -> id, роль позиции
TEACHING_POSITIONS = [
    ("онлайн-тьютор", "", "middlebury-tutor", "онлайн-тьютор"),
    ("учебный ассистент", "департамент психологии", "hse-psy-teaching-assistant", "учебный ассистент"),
    ("учебный ассистент", "кафедра высшей математики", "hse-math-teaching-assistant", "учебный ассистент"),
    ("преподаватель", "департамент психологии", "hse-psy-teacher", "преподаватель"),
    ("преподаватель", "Институт общественных наук", "ranepa-teacher", "преподаватель"),
    ("преподаватель", "лаборатория", "hse-uxlab-teacher", "преподаватель"),
]

# Курсы: характерная часть названия -> id
COURSES = [
    ("Прикладной анализ", "hse-nis-applied-data-analysis"),
    ("валидизация", "hse-nis-diagnostic-tools"),
    ("Статистика для", "hse-statistics-for-data-analysis"),
    ("человек-цифрового", "hse-human-digital-interaction"),
    ("Современные методы", "ranepa-modern-data-analysis"),
    ("Психодиагностика", "hse-psychodiagnostics-practicum"),
    ("мир линейных", "uxlab-wlm"),
    ("Введение в психологию", "hse-intro-psychology"),
    ("визуализация данных", "hse-nis-data-visualization"),
    ("t-теста", "uxlab-andan"),
    ("Математические", "hse-math-stat-methods"),
    ("PsychoPy", "uxlab-psychopy"),
]

# Остальные позиции: id в порядке старого сайта
POSITION_IDS = {
    "research": ["profilum-product-researcher"],
    "academic": ["hse-uxlab-research-intern"],
    "management": [
        "uxlab-brand-manager",
        "uxlab-cogsem-coordinator",
        "uxlab-junior-manager",
        "uxlab-smm-head",
        "appcogsci-2021-program-head",
        "wlm-2021-coordinator",
        "sps-2021-program-deputy-head",
        "psyhse-2019-organizer",
        "appcogsci-2020-program-head",
        "andan-2020-coordinator",
        "sps-2020-program-head",
        "psychopy-2019-coordinator",
        "sps-2019-extracurricular-head",
    ],
    "other": [
        "uxlab-designer",
        "uxlab-site-editor",
        "sps-guest-lecturer",
        "hse-lyceum-guest-lecturer",
        "student-org-committee-head",
        "thevyshka-proofreader",
    ],
}

EXTRA_IDS = {
    "qualification": [
        "focus-groups-2024",
        "teach-for-hse-group-work-2021",
        "hse-digital-communications-2021",
        "teach-for-hse-presentations-2020",
    ],
    "school": [
        "letnyaya-shkola-education-2023",
        "appcogsci-2023",
        "spbu-winter-school-2023",
        "appcogsci-2022",
        "edcrunch-2021",
        "letnyaya-shkola-education-2021",
        "appcogsci-2021",
        "hse-nlp-webinar-2020",
        "appcogsci-2020",
        "ipras-network-analysis-2020",
        "letnyaya-shkola-testing-2020",
        "duncker-school-2019",
        "letnyaya-shkola-andan-2019",
        "appcogsci-2019",
        "highlights-web-design-2018",
        "hse-management-psychology-2018",
    ],
    "mooc": [
        "udemy-machine-learning",
        "udemy-python-developer",
        "stepik-git",
        "fructcode-php-mysql",
        "fructcode-javascript-jquery",
        "fructcode-html-css",
        "stepik-javascript",
        "stepik-r-data-analysis-2",
        "stepik-r-data-analysis",
        "stepik-r-programming",
        "coursera-latex",
    ],
}

ACHIEVEMENT_IDS = [
    "hse-psy-academic-council",
    "hse-psy-gratitude-2022",
    "hse-talent-pool-2022",
    "hse-best-research-paper-2021",
    "hse-psy-gratitude-2021",
    "psyhse-ggplot2-gratitude-2021",
    "hse-student-council-gratitude-2018",
    "olympiad-chemistry-final-2014",
    "olympiad-chemistry-regional-2014",
    "olympiad-biology-regional-2014",
    "olympiad-biology-final-2013",
    "olympiad-biology-regional-2013",
    "olympiad-chemistry-regional-2013",
    "olympiad-biology-regional-2012",
    "olympiad-chemistry-regional-2012",
]

CONFERENCE_IDS = ["bruner-2021", "psychology-xxi-2021", "psyhse-2019", "duncker-2019"]
GRANT_IDS = ["rsf-20-78-10055"]
PUBLICATION_IDS = ["visual-search-erp-2023", "trust-assessment-tool-2021", "hybrid-search-category-2021"]
COPYRIGHT_IDS = ["wlm-2023-course", "wlm-2021-course"]
INDEX_MATERIAL_IDS = [
    "ggplot2-master-class-2020",
    "andan-matrices",
    "andan-glm-binomial",
    "andan-logit-transformation",
    "andan-mixed-models",
    "andan-pca-fa",
    "wlm-2021-book",
    "wlm-2021-lectures",
    "wlm-2021-practice",
    "psyhse-ggplot2-2021",
    "appcogsci-ggplot2-2022",
    "duncker-rmarkdown-2022",
]
LANGUAGE_IDS = ["russian", "english", "french", "ukrainian", "turkish", "russian-as-foreign", "russian-sign", "latin"]
SKILL_GROUP_IDS = ["programming", "data-analysis", "research-methods", "management", "software", "other"]
SKILL_SUBGROUP_IDS = ["basic", "graphics", "audio-video", "special"]
INTEREST_GROUP_IDS = ["science-education", "art-design"]
EDUCATION = [("hse-ling", "master"), ("hse-psy", "bachelor"), ("pspbgmu-med", "specialist")]

# Словарь тегов из ТЗ, раздел 5
TAGS = [
    ("stats", "статистика и анализ данных"),
    ("psychometrics", "психометрика"),
    ("research-design", "дизайн исследований"),
    ("teaching", "преподавание"),
    ("biostat", "биостатистика"),
    ("ux-research", "UX и продуктовые исследования"),
    ("cognitive", "когнитивная психология"),
    ("linguistics", "лингвистика"),
    ("management", "менеджмент"),
]

# Предложенные теги. Владелец утверждает их по отчёту (ТЗ, открытый вопрос 6).
PROPOSED_TAGS = {
    # позиции
    "hse-psy-teacher": ["teaching"],
    "ranepa-teacher": ["teaching"],
    "middlebury-tutor": ["teaching", "linguistics"],
    "hse-psy-teaching-assistant": ["teaching"],
    "hse-uxlab-teacher": ["teaching"],
    "hse-math-teaching-assistant": ["teaching"],
    "profilum-product-researcher": ["ux-research", "research-design", "stats"],
    "hse-uxlab-research-intern": ["cognitive", "psychometrics", "research-design"],
    "uxlab-brand-manager": ["management"],
    "uxlab-cogsem-coordinator": ["management"],
    "uxlab-junior-manager": ["management"],
    "uxlab-smm-head": ["management"],
    "appcogsci-2021-program-head": ["management", "teaching"],
    "wlm-2021-coordinator": ["management"],
    "sps-2021-program-deputy-head": ["management", "teaching"],
    "psyhse-2019-organizer": ["management"],
    "appcogsci-2020-program-head": ["management", "teaching"],
    "andan-2020-coordinator": ["management"],
    "sps-2020-program-head": ["management", "teaching"],
    "psychopy-2019-coordinator": ["management"],
    "sps-2019-extracurricular-head": ["management"],
    "sps-guest-lecturer": ["teaching"],
    "hse-lyceum-guest-lecturer": ["teaching"],
    "student-org-committee-head": ["management"],
    # курсы
    "hse-nis-applied-data-analysis": ["stats", "teaching"],
    "hse-nis-diagnostic-tools": ["psychometrics", "teaching"],
    "hse-statistics-for-data-analysis": ["stats", "teaching"],
    "hse-human-digital-interaction": ["cognitive", "ux-research", "teaching"],
    "ranepa-modern-data-analysis": ["stats", "teaching"],
    "hse-psychodiagnostics-practicum": ["psychometrics", "teaching"],
    "uxlab-wlm": ["stats", "teaching"],
    "hse-intro-psychology": ["teaching"],
    "hse-nis-data-visualization": ["stats", "teaching"],
    "uxlab-andan": ["stats", "teaching"],
    "hse-math-stat-methods": ["stats", "teaching"],
    "uxlab-psychopy": ["research-design", "teaching"],
    # образование
    "hse-ling": ["linguistics"],
    # дополнительное образование
    "focus-groups-2024": ["ux-research", "research-design"],
    "teach-for-hse-group-work-2021": ["teaching"],
    "teach-for-hse-presentations-2020": ["teaching"],
    "letnyaya-shkola-education-2023": ["teaching"],
    "appcogsci-2023": ["cognitive"],
    "spbu-winter-school-2023": ["cognitive"],
    "appcogsci-2022": ["cognitive"],
    "edcrunch-2021": ["teaching"],
    "letnyaya-shkola-education-2021": ["teaching"],
    "appcogsci-2021": ["cognitive"],
    "hse-nlp-webinar-2020": ["linguistics"],
    "appcogsci-2020": ["cognitive"],
    "ipras-network-analysis-2020": ["cognitive", "linguistics"],
    "letnyaya-shkola-testing-2020": ["psychometrics"],
    "duncker-school-2019": ["cognitive"],
    "letnyaya-shkola-andan-2019": ["stats"],
    "appcogsci-2019": ["cognitive"],
    "hse-management-psychology-2018": ["management"],
    "udemy-machine-learning": ["stats"],
    "stepik-r-data-analysis-2": ["stats"],
    "stepik-r-data-analysis": ["stats"],
    "stepik-r-programming": ["stats"],
    # достижения
    "hse-psy-academic-council": ["teaching"],
    "hse-psy-gratitude-2022": ["teaching"],
    "hse-best-research-paper-2021": ["psychometrics"],
    "psyhse-ggplot2-gratitude-2021": ["stats", "teaching"],
    # исследования
    "bruner-2021": ["cognitive"],
    "psychology-xxi-2021": ["cognitive"],
    "psyhse-2019": ["cognitive", "ux-research"],
    "duncker-2019": ["cognitive", "ux-research"],
    "rsf-20-78-10055": ["cognitive"],
    "visual-search-erp-2023": ["cognitive"],
    "trust-assessment-tool-2021": ["psychometrics"],
    "hybrid-search-category-2021": ["cognitive"],
    # материалы
    "wlm-2023-course": ["stats", "teaching"],
    "wlm-2021-course": ["stats", "teaching"],
    "ggplot2-master-class-2020": ["stats", "teaching"],
    "andan-matrices": ["stats", "teaching"],
    "andan-glm-binomial": ["stats", "teaching"],
    "andan-logit-transformation": ["stats", "teaching"],
    "andan-mixed-models": ["stats", "teaching"],
    "andan-pca-fa": ["stats", "teaching"],
    "wlm-2021-book": ["stats", "teaching"],
    "wlm-2021-lectures": ["stats", "teaching"],
    "wlm-2021-practice": ["stats", "teaching"],
    "psyhse-ggplot2-2021": ["stats", "teaching"],
    "appcogsci-ggplot2-2022": ["stats", "teaching"],
    "duncker-rmarkdown-2022": ["teaching"],
}

# Кандидаты в featured — только в отчёт, в данные не записываются
FEATURED_CANDIDATES = [
    ("positions", "hse-psy-teacher"),
    ("positions", "ranepa-teacher"),
    ("positions", "profilum-product-researcher"),
    ("positions", "hse-uxlab-research-intern"),
    ("education", "hse-ling"),
    ("education", "hse-psy"),
]

VISIBLE_CONTACTS = {"email", "telegram", "linkedin"}
CONTACT_KINDS = {"mail": "email"}

# Интерес, у которого нет пары в английском списке
INTEREST_WITHOUT_EN = "психология человеко-цифрового взаимодействия"

# ---------------------------------------------------------------------------
# Разбор HTML
# ---------------------------------------------------------------------------


def clean(fragment):
    text = re.sub(r"<[^>]+>", "", fragment)
    return " ".join(html.unescape(text).split())


def read_html(path):
    text = (SRC / "old-site" / path).read_text(encoding="utf-8")
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    comments = re.findall(r"<!--.*?-->", text, flags=re.S)
    return re.sub(r"<!--.*?-->", "", text, flags=re.S), comments


LEAF = re.compile(r'<(p|div)\s+class="([^"]+)"([^>]*)>((?:(?!<div|<p[\s>]).)*?)</\1>', re.S)


def parse_sections(text):
    """Возвращает список разделов: {level, title, items, loose}.

    items — блоки <div class="item">, каждый — список полей (класс, текст, скрыто, html).
    loose — поля раздела вне блоков item (навыки, интересы, языки).
    """
    body = text[text.index("<h2") :]
    body = body[: body.index("<footer")] if "<footer" in body else body
    parts = re.split(r"(<h[234][^>]*>.*?</h[234]>)", body, flags=re.S)
    sections = []
    for i in range(1, len(parts), 2):
        heading, content = parts[i], parts[i + 1]
        section = {"level": int(heading[2]), "title": clean(heading), "items": [], "loose": []}
        chunks = re.split(r'<div class="item[^"]*"[^>]*>', content)
        flags = re.findall(r'<div class="(item[^"]*)"', content)
        for field in LEAF.finditer(chunks[0]):
            cls, attrs, inner = field.group(2), field.group(3), field.group(4)
            if "menu" in cls:
                continue
            section["loose"].append((cls, clean(inner), "hidden" in attrs, inner))
        for flag, chunk in zip(flags, chunks[1:]):
            fields = [
                (f.group(2), clean(f.group(4)), "hidden" in f.group(3), f.group(4))
                for f in LEAF.finditer(chunk)
            ]
            section["items"].append({"current": "current_item" in flag, "fields": fields})
        sections.append(section)
    return sections


def field(item, cls, index=0):
    values = [text for c, text, _, _ in item["fields"] if c == cls and text]
    return values[index] if len(values) > index else None


def is_hidden(item, cls):
    return any(hidden for c, _, hidden, _ in item["fields"] if c == cls)


# ---------------------------------------------------------------------------
# Даты
# ---------------------------------------------------------------------------

MONTHS = {}
for number, names in enumerate(
    [
        "январь января january",
        "февраль февраля february",
        "март марта march",
        "апрель апреля april",
        "май мая may",
        "июнь июня june",
        "июль июля july",
        "август августа august",
        "сентябрь сентября september",
        "октябрь октября october",
        "ноябрь ноября november",
        "декабрь декабря december",
    ],
    start=1,
):
    for name in names.split():
        MONTHS[name] = number


def parse_point(text):
    year = re.search(r"(?<!\d)(\d{4})(?!\d)", text)
    rest = text.replace(year.group(1), " ") if year else text
    month = next((MONTHS[w] for w in re.findall(r"[a-zа-яё]+", rest) if w in MONTHS), None)
    days = [int(d) for d in re.findall(r"(?<!\d)(\d{1,2})(?!\d)", rest)]
    return (int(year.group(1)) if year else None), month, days


def fmt(year, month=None, day=None):
    if month is None:
        return f"{year:04d}"
    if day is None:
        return f"{year:04d}-{month:02d}"
    return f"{year:04d}-{month:02d}-{day:02d}"


def parse_period(original):
    """Строка с датами -> (start, end, пометка). Пометка объясняет нестандартные случаи."""
    text = original.lower().strip()
    if "запросу" in text or "request" in text:
        return None, None, "nodates"
    if "осень" in text or "autumn" in text:
        years = re.findall(r"\d{4}", text)
        return years[0], years[-1], "season"
    present = bool(re.search(r"наст\. ?вр|since", text))
    text = re.sub(r"\s*—?\s*наст\. ?вр\.?", "", text).replace("since ", "").strip()
    parts = [p.strip() for p in text.split("—")]
    note = None
    if len(parts) == 1:
        year, month, days = parse_point(parts[0])
        years = re.findall(r"\d{4}", parts[0])
        if month is None:
            start, end = years[0], (years[1] if len(years) > 1 else None)
        elif not days:
            start, end = fmt(year, month), None
        elif len(days) == 1:
            start, end = fmt(year, month, days[0]), None
        else:
            start, end = fmt(year, month, days[0]), fmt(year, month, days[1])
    else:
        y1, m1, d1 = parse_point(parts[0])
        y2, m2, d2 = parse_point(parts[1])
        if y1 is None:
            y1 = y2
            if m1 > m2:
                # «25 декабря — 12 февраля 2018»: начало относится к предыдущему году
                y1, note = y2 - 1, "yearwrap"
        start = fmt(y1, m1, d1[0] if d1 else None)
        end = fmt(y2, m2, d2[0] if d2 else None)
    if present:
        end = "present"
    return start, end, note


# ---------------------------------------------------------------------------
# Вспомогательное
# ---------------------------------------------------------------------------

report = {
    "nodates": [],
    "season": [],
    "yearwrap": [],
    "present": [],
    "current": [],
    "en_unmatched": [],
    "en_skipped": [],
    "en_matched": {},
    "hidden": [],
}


def T(ru, en=None):
    """Текст на двух языках. en добавляется, только если он есть."""
    if not ru:
        return None
    value = {"ru": ru}
    if en:
        value["en"] = en
    return value


def split_org(text, known):
    """«подразделение, организация» -> (подразделение, организация)."""
    for org in known:
        if text.endswith(", " + org):
            return text[: -len(org) - 2], org
    return None, text


def put(entry, key, value):
    if value is not None and value != [] and value != "":
        entry[key] = value


def with_dates(entry, original, label):
    start, end, note = parse_period(original)
    put(entry, "start", start)
    put(entry, "end", end)
    if note == "nodates":
        entry["notes"] = f"На старом сайте вместо дат: «{original}»"
        report["nodates"].append(label)
    elif note == "season":
        entry["notes"] = f"На старом сайте даты указаны как «{original}»; в данных оставлены только годы"
        report["season"].append(label)
    elif note == "yearwrap":
        entry["notes"] = f"На старом сайте: «{original}». Год начала ({start[:4]}) выведен из дат, проверить"
        report["yearwrap"].append(label)
    if end == "present":
        report["present"].append(f"{label} — «{original}»")
    return start, end


def tags_for(entry_id):
    return PROPOSED_TAGS.get(entry_id, [])


def count_en(name, matched, total):
    report["en_matched"][name] = (matched, total)


# ---------------------------------------------------------------------------
# Сбор данных
# ---------------------------------------------------------------------------


def section_by_title(sections, title, level=None):
    for s in sections:
        if s["title"] == title and (level is None or s["level"] == level):
            return s
    raise KeyError(title)


def build():
    ru_text, ru_comments = read_html("a/ru/angelgardt.html")
    en_text, _ = read_html("a/en/angelgardt.html")
    index_text, _ = read_html("a/ru/index.html")
    ru = parse_sections(ru_text)
    en = parse_sections(en_text)
    data = {}
    counts = []  # (раздел старого сайта, записей там, записей в YAML, пояснение)

    en_orgs = ["HSE University"]
    ru_orgs = [HSE, "РАНХиГС"]

    # ----- позиции и курсы -----
    positions, courses = [], {}
    position_by_id = {}

    def en_org(text):
        if not text:
            return None, None
        return split_org(text, en_orgs)

    # преподавание
    ru_teach = section_by_title(ru, "Преподавательская деятельность")["items"]
    en_teach = section_by_title(en, "Teaching Experience")["items"]
    en_by_dates = {}
    for item in en_teach:
        start, end, _ = parse_period(field(item, "duration"))
        en_by_dates[(start, end)] = item
    used_en = set()
    grouping = {}
    for item in ru_teach:
        role = field(item, "position")
        org_text = field(item, "organization")
        unit, org = split_org(org_text, ru_orgs)
        duration = field(item, "duration")
        start, end, _ = parse_period(duration)
        pos_id, pos_role = next(
            (pid, prole)
            for r, u, pid, prole in TEACHING_POSITIONS
            if r in role and u in org_text and not (r == "преподаватель" and "автор" not in role and role != r)
        )
        en_item = en_by_dates.get((start, end))
        if en_item is not None:
            used_en.add(id(en_item))
        en_unit, en_organization = en_org(field(en_item, "organization")) if en_item else (None, None)
        if pos_id not in position_by_id:
            entry = {"id": pos_id, "kind": "teaching", "role": T(pos_role), "organization": T(org)}
            put(entry, "unit", T(unit))
            put(entry, "tags", tags_for(pos_id))
            position_by_id[pos_id] = entry
            positions.append(entry)
            grouping[pos_id] = []
        entry = position_by_id[pos_id]
        if en_item is not None:
            if role == pos_role and "en" not in entry["role"]:
                entry["role"]["en"] = field(en_item, "position")
            if en_organization and "en" not in entry["organization"]:
                entry["organization"]["en"] = en_organization
            if en_unit and "unit" in entry and "en" not in entry["unit"]:
                entry["unit"]["en"] = en_unit
        course_text = field(item, "suborganization")
        label = f"{role}, {course_text or org_text} ({duration})"
        if item["current"]:
            report["current"].append(label)
        if course_text is None:
            # позиция без курсов (онлайн-тьютор)
            with_dates(entry, duration, label)
            description = field(item, "description")
            if is_hidden(item, "description"):
                entry["notes"] = f"На старом сайте описание было скрыто: «{description}»"
                report["hidden"].append(f"описание позиции «{role}» ({org_text})")
                if en_item is not None:
                    report["en_skipped"].append(
                        f"Online Tutor: описание «{field(en_item, 'description')}» — русское описание скрыто; "
                        "поле «course “????????”» — заглушка"
                    )
            else:
                put(entry, "description", T(description))
            grouping[pos_id].append("(без курсов)")
            continue
        course_id = next(cid for key, cid in COURSES if key in course_text)
        title = re.sub(r"^курс ", "", course_text)
        if course_id not in courses:
            course = {"id": course_id, "position": pos_id, "title": T(title), "runs": []}
            courses[course_id] = course
            grouping[pos_id].append(course_id)
        course = courses[course_id]
        run = {"start": start}
        put(run, "end", end)
        if role != pos_role:
            run["role"] = T(role, field(en_item, "position") if en_item else None)
        run["duties"] = T(field(item, "description"), field(en_item, "description") if en_item else None)
        course["runs"].append(run)
        if en_item is not None and "en" not in course["title"]:
            course["title"]["en"] = re.sub(r"^course ", "", field(en_item, "suborganization"))
    for course in courses.values():
        put(course, "tags", tags_for(course["id"]))
    for item in en_teach:
        if id(item) not in used_en:
            report["en_unmatched"].append(f"Teaching: {field(item, 'suborganization')} ({field(item, 'duration')})")
    count_en("Преподавательская деятельность (записи старого сайта)", len(used_en), len(ru_teach))
    counts.append(
        (
            "Опыт работы → Преподавательская деятельность",
            len(ru_teach),
            f"позиций: {len(positions)}, курсов: {len(courses)}, "
            f"запусков: {sum(len(c['runs']) for c in courses.values())}",
            "18 записей старого сайта = 17 запусков курсов + 1 позиция без курсов (онлайн-тьютор)",
        )
    )
    teaching_positions = len(positions)

    # остальные позиции — по одной записи на запись старого сайта
    for kind, ru_title, en_title in [
        ("research", "Исследовательская деятельность", "Research Experience"),
        ("academic", "Академическая деятельность", "Academic Experience"),
        ("management", "Административная и менеджерская деятельность", "Administrative and Managerial Experience"),
        ("other", "Другое", "Other"),
    ]:
        ru_items = section_by_title(ru, ru_title, 3)["items"]
        en_items = section_by_title(en, en_title, 3)["items"]
        matched = 0
        for index, item in enumerate(ru_items):
            pos_id = POSITION_IDS[kind][index]
            role, org_text, duration = field(item, "position"), field(item, "organization"), field(item, "duration")
            unit, org = split_org(org_text, ru_orgs)
            en_item = en_items[index] if index < len(en_items) else None
            if en_item is not None and parse_period(field(en_item, "duration")) != parse_period(duration):
                report["en_unmatched"].append(f"{en_title}: {field(en_item, 'position')} — даты не совпали")
                en_item = None
            matched += en_item is not None
            en_unit, en_organization = en_org(field(en_item, "organization")) if en_item else (None, None)
            if unit is None:
                en_organization = field(en_item, "organization") if en_item else None
                en_unit = None
            entry = {"id": pos_id, "kind": kind}
            entry["role"] = T(role, field(en_item, "position") if en_item else None)
            entry["organization"] = T(org, en_organization)
            put(entry, "unit", T(unit, en_unit))
            put(entry, "context", T(field(item, "suborganization"), field(en_item, "suborganization") if en_item else None))
            label = f"{role}, {field(item, 'suborganization') or org_text} ({duration})"
            with_dates(entry, duration, label)
            put(entry, "description", T(field(item, "description"), field(en_item, "description") if en_item else None))
            put(entry, "tags", tags_for(pos_id))
            if "notes" in entry:
                entry["notes"] = entry.pop("notes")
            if item["current"]:
                report["current"].append(label)
            positions.append(entry)
        count_en(ru_title, matched, len(ru_items))
        counts.append((f"Опыт работы → {ru_title}", len(ru_items), f"позиций: {len(ru_items)}", ""))
    data["positions"] = positions
    data["courses"] = list(courses.values())
    report["grouping"] = grouping
    report["teaching_positions"] = teaching_positions

    # ----- образование -----
    ru_edu = section_by_title(ru, "Образование")["items"]
    en_edu = section_by_title(en, "Education")["items"]
    proto_ru = json.loads((SRC / "ru" / "education.json").read_text(encoding="utf-8"))["list"]
    proto_en = json.loads((SRC / "en" / "education.json").read_text(encoding="utf-8"))["list"]
    report["proto"] = []

    def people(item, cls, index=0):
        raw = [inner for c, _, _, inner in item["fields"] if c == cls]
        if len(raw) <= index:
            return None, None
        name = re.search(r'<span class="name">(.*?)</span>', raw[index], re.S)
        if not name:
            return None, None
        rest = clean(raw[index][name.end() :]).lstrip(", ").strip()
        return clean(name.group(1)), rest or None

    def grade(item, index):
        value = field(item, "grade", index)
        return value.split(": ", 1)[1] if value else None

    education = []
    for index, item in enumerate(ru_edu):
        edu_id, level = EDUCATION[index]
        e = en_edu[index]
        p_ru, p_en = proto_ru[index], proto_en[index]
        assert p_ru["id"] == edu_id
        start, end, _ = parse_period(field(item, "duration"))
        entry = {"id": edu_id, "level": level, "start": start, "end": end}
        entry["university"] = T(field(item, "university"), field(e, "university"))
        # у бакалавриата второй faculty/program/field относится к дополнительной специализации
        put(entry, "faculty", T(field(item, "faculty"), field(e, "faculty")))
        # английский файл прототипа не переведён: en берём, только если он отличается от ru
        en_proto = lambda key: p_en.get(key) if p_en.get(key) != p_ru.get(key) else None
        put(entry, "department", T(p_ru.get("department"), en_proto("department")))
        put(entry, "program", T(field(item, "program"), field(e, "program")))
        put(entry, "track", T(field(item, "track"), field(e, "track")))
        put(entry, "specialty", T(field(item, "field"), field(e, "field")))
        put(entry, "qualification", T(p_ru.get("qualification"), en_proto("qualification")))
        gpa = field(item, "gpa")
        gpa_en = field(e, "gpa")
        put(entry, "gpa", T(gpa.split(": ", 1)[1] if gpa else None, gpa_en.split(": ", 1)[1] if gpa_en else None))
        if field(item, "minor"):
            minor = {}
            put(minor, "institute", T(field(item, "faculty", 1), field(e, "faculty", 1)))
            put(minor, "program", T(field(item, "program", 1), field(e, "program", 1)))
            put(minor, "specialty", T(field(item, "field", 1), field(e, "field", 1)))
            entry["minor"] = minor
        title_ru, _ = people(item, "fqw_title")
        if title_ru:
            title_en, _ = people(e, "fqw_title")
            thesis = {"title": T(title_ru, title_en)}
            for key, cls, idx in [("supervisor", "fqw_supervisor", 0), ("advisor", "fqw_advisor", 0), ("reviewer", "fqw_advisor", 1)]:
                name_ru, degree_ru = people(item, cls, idx)
                name_en, degree_en = people(e, cls, idx)
                if name_ru:
                    person = {"name": T(name_ru, name_en)}
                    put(person, "title", T(degree_ru, degree_en))
                    thesis[key] = person
            grades = {}
            for idx, key in enumerate(["supervisor", "reviewer", "commission"]):
                put(grades, key, T(grade(item, idx), grade(e, idx)))
            put(thesis, "grades", grades)
            entry["thesis"] = thesis
        put(entry, "tags", tags_for(edu_id))
        notes = []
        if is_hidden(item, "gpa"):
            notes.append("На старом сайте GPA был скрыт.")
        proto_gpa = p_ru.get("gpa")
        if gpa and proto_gpa and proto_gpa.split("/")[0].strip() != gpa.split(": ", 1)[1].split("/")[0].strip():
            notes.append(
                f"Расхождение источников: на старом сайте GPA {gpa.split(': ', 1)[1]}, "
                f"в прототипе (migration/sources/ru/education.json) — {proto_gpa}. Записано значение со старого сайта."
            )
            report["proto"].append(f"`{edu_id}`: GPA на старом сайте {gpa.split(': ', 1)[1]}, в прототипе {proto_gpa}")
        if "не окончен" in p_ru.get("level", "").replace("\xa0", " "):
            notes.append(f"В прототипе уровень указан как «{p_ru['level']}»; на старом сайте этой пометки нет.")
            report["proto"].append(f"`{edu_id}`: в прототипе уровень «{p_ru['level']}», на старом сайте пометки нет")
        if notes:
            entry["notes"] = " ".join(notes)
        education.append(entry)
    data["education"] = education
    count_en("Образование", len(en_edu), len(ru_edu))
    counts.append(("Образование", len(ru_edu), f"записей: {len(education)}", ""))

    # ----- дополнительное образование -----
    extra = []
    for kind, ru_title, en_title in [
        ("qualification", "Повышение квалификации", "Professional Retraining"),
        ("school", "Школы / Вебинары / Курсы", "Schools / Webinars / Courses"),
        ("mooc", "MOOCs", "MOOCs"),
    ]:
        ru_items = section_by_title(ru, ru_title)["items"]
        en_items = section_by_title(en, en_title)["items"]
        used = set()
        matched = 0
        for index, item in enumerate(ru_items):
            entry_id = EXTRA_IDS[kind][index]
            duration = field(item, "duration") or field(item, "date")
            period = parse_period(duration)
            if kind == "mooc":
                # в английском списке нет первой записи русского; остальные идут в том же порядке
                candidate = en_items[index - 1] if index >= 1 else None
                same = candidate is not None and field(candidate, "suborganization") == field(item, "suborganization")
                en_item = candidate if same and parse_period(field(candidate, "duration"))[0] == period[0] else None
            else:
                en_item = next(
                    (c for c in en_items if id(c) not in used and parse_period(field(c, "duration"))[:2] == period[:2]),
                    None,
                )
            if en_item is not None:
                used.add(id(en_item))
                matched += 1
            g = lambda cls: field(en_item, cls) if en_item is not None else None
            entry = {"id": entry_id, "kind": kind, "title": T(field(item, "title"), g("title"))}
            sub = field(item, "suborganization")
            if kind == "mooc":
                put(entry, "platform", T(sub, g("suborganization")))
            elif sub and sub.startswith("трек "):
                put(entry, "track", T(sub, g("suborganization")))
                put(entry, "organization", T(field(item, "organization"), g("organization")))
            else:
                put(entry, "organizer", T(sub, g("suborganization")))
                put(entry, "organization", T(field(item, "organization"), g("organization")))
            with_dates(entry, duration, f"{field(item, 'title')} ({duration})")
            put(entry, "tags", tags_for(entry_id))
            if "notes" in entry:
                entry["notes"] = entry.pop("notes")
            extra.append(entry)
        for item in en_items:
            if id(item) not in used:
                report["en_unmatched"].append(f"{en_title}: {field(item, 'title')} ({field(item, 'duration')})")
        count_en(f"Дополнительное образование → {ru_title}", matched, len(ru_items))
        counts.append((f"Дополнительное образование → {ru_title}", len(ru_items), f"записей: {len(ru_items)}", ""))
    data["extra-education"] = extra

    # ----- достижения -----
    ru_items = section_by_title(ru, "Достижения")["items"]
    en_items = section_by_title(en, "Achievements")["items"]
    achievements = []
    matched = 0
    for index, item in enumerate(ru_items):
        entry_id = ACHIEVEMENT_IDS[index]
        date = field(item, "date")
        # в английском списке нет двух первых записей русского
        en_item = en_items[index - 2] if index >= 2 else None
        if en_item is not None and parse_period(field(en_item, "date"))[:2] != parse_period(date)[:2]:
            en_item = None
        matched += en_item is not None
        g = lambda cls: field(en_item, cls) if en_item is not None else None
        entry = {"id": entry_id, "title": T(field(item, "title"), g("title"))}
        subsub, sub = field(item, "subsubtitle"), field(item, "subtitle")
        if entry_id == "psyhse-ggplot2-gratitude-2021":
            # английские подписи описывают другое (организаторов, а не конференцию) — не переносим
            put(entry, "context", T(subsub))
            put(entry, "organization", T(sub))
            report["en_skipped"].append(
                f"Достижение «{g('title')}»: строки «{g('subsubtitle')}» и «{g('subtitle')}» "
                "не соответствуют русским («Пси-Вышка: международная конференция молодых учёных» и название подразделений)"
            )
        elif subsub:
            put(entry, "context", T(subsub, g("subsubtitle")))
            put(entry, "organization", T(sub, g("subtitle")))
        else:
            # у олимпиад единственная подпись — результат участия
            put(entry, "context", T(sub, g("subtitle")))
        with_dates(entry, date, f"{field(item, 'title')} ({date})")
        put(entry, "tags", tags_for(entry_id))
        achievements.append(entry)
    data["achievements"] = achievements
    count_en("Достижения", matched, len(ru_items))
    counts.append(("Достижения", len(ru_items), f"записей: {len(achievements)}", ""))

    # ----- языки -----
    ru_langs = [t for c, t, _, _ in section_by_title(ru, "Владение языками")["loose"] if c == "lang"]
    en_langs = [t for c, t, _, _ in section_by_title(en, "Language Profficiency")["loose"] if c == "lang"]

    def lang_parts(text):
        m = re.match(r"^(.*?) \((.*)\)$", text)
        return (m.group(1), m.group(2)) if m else (text, None)

    languages = []
    for index, text in enumerate(ru_langs):
        name, level = lang_parts(text)
        en_name, en_level = lang_parts(en_langs[index])
        entry = {"id": LANGUAGE_IDS[index], "name": T(name, en_name)}
        put(entry, "level", T(level, en_level))
        languages.append(entry)
    data["languages"] = languages
    count_en("Владение языками", len(en_langs), len(ru_langs))
    counts.append(("Владение языками", len(ru_langs), f"записей: {len(languages)}", ""))

    # ----- навыки -----
    def skill_sections(sections, start_title):
        start = next(i for i, s in enumerate(sections) if s["title"] == start_title and s["level"] == 2)
        result = []
        for s in sections[start + 1 :]:
            if s["level"] == 2:
                break
            result.append(s)
        return result

    ru_skills, en_skills = skill_sections(ru, "Навыки"), skill_sections(en, "Skills")
    groups, group_index, sub_index, total_skills = [], 0, 0, 0
    for s_ru, s_en in zip(ru_skills, en_skills):
        items_ru = [t for c, t, _, _ in s_ru["loose"] if c == "skill"]
        items_en = [t for c, t, _, _ in s_en["loose"] if c == "skill"]
        total_skills += len(items_ru)
        items = [T(a, b) for a, b in zip(items_ru, items_en)]
        if s_ru["level"] == 3:
            group = {"id": SKILL_GROUP_IDS[group_index], "title": T(s_ru["title"], s_en["title"])}
            put(group, "items", items)
            groups.append(group)
            group_index += 1
        else:
            sub = {"id": SKILL_SUBGROUP_IDS[sub_index], "title": T(s_ru["title"], s_en["title"]), "items": items}
            groups[-1].setdefault("subgroups", []).append(sub)
            sub_index += 1
    data["skills"] = {"groups": groups}
    count_en("Навыки (пункты)", total_skills, total_skills)
    counts.append(("Навыки", f"{total_skills} пунктов", f"{len(groups)} групп, {sub_index} подгруппы, {total_skills} пунктов", ""))

    # ----- интересы -----
    ru_int, en_int = skill_sections(ru, "Интересы"), skill_sections(en, "Interests")
    en_queue = [t for s in en_int for c, t, _, _ in s["loose"] if c == "interest"]
    groups, shown, hidden_count, with_en = [], 0, 0, 0
    for index, (s_ru, s_en) in enumerate(zip(ru_int, en_int)):
        items = []
        for c, text, hidden, _ in s_ru["loose"]:
            if c != "interest":
                continue
            en_value = None if text == INTEREST_WITHOUT_EN else en_queue.pop(0)
            if hidden:
                hidden_count += 1
                report["hidden"].append(f"интерес «{text}»")
                continue
            if en_value is None:
                report["en_skipped"].append(f"Интерес «{text}»: в английском списке пары нет")
            items.append(T(text, en_value))
            shown += 1
            with_en += en_value is not None
        groups.append({"id": INTEREST_GROUP_IDS[index], "title": T(s_ru["title"], s_en["title"]), "items": items})
    assert not en_queue, en_queue
    data["interests"] = {"groups": groups}
    count_en("Интересы (пункты)", with_en, shown)
    counts.append(
        (
            "Интересы",
            f"{shown + hidden_count} пунктов",
            f"{len(groups)} группы, {shown} пунктов",
            f"{hidden_count} пункта скрыты на старом сайте и не перенесены (список — в разделе 7)",
        )
    )

    # ----- публикации -----
    publications = []
    for index, item in enumerate(section_by_title(ru, "Публикации")["items"]):
        text = field(item, "publication")
        left, right = text.split(" // ")
        m = re.match(r"^((?:\S+ (?:[A-ZА-ЯЁ]\.\s?)+(?:, )?)+)(.*)$", left)
        authors = [a.strip() for a in m.group(1).strip().split(", ")]
        entry = {"id": PUBLICATION_IDS[index], "authors": authors, "title": m.group(2).strip()}
        ym = re.search(r"\. (\d{4})\.?", right)
        entry["venue"] = right[: ym.start()].strip()
        entry["year"] = int(ym.group(1))
        tail = right[ym.end() :]
        issue = re.search(r"№ (\S+?)\.", tail)
        pages = re.search(r"С\. ([\d\-–]+)", tail)
        put(entry, "issue", issue.group(1) if issue else None)
        put(entry, "pages", pages.group(1) if pages else None)
        entry["status"] = "in-press" if field(item, "under_review") else "published"
        put(entry, "tags", tags_for(entry["id"]))
        publications.append(entry)
    data["publications"] = publications
    en_pubs = section_by_title(en, "Publications")["items"]
    for item in en_pubs:
        report["en_unmatched"].append(
            f"Publications: {field(item, 'publication')} {field(item, 'journal') or ''} {field(item, 'under_review') or ''}".strip()
        )
    counts.append(("Исследования → Публикации", len(publications), f"записей: {len(publications)}", ""))

    # ----- конференции -----
    en_conf = section_by_title(en, "Conferences")["items"]
    conferences = []
    matched = 0
    for index, item in enumerate(section_by_title(ru, "Конференции")["items"]):
        location, dates = field(item, "date").split(", ", 1)
        talk = field(item, "report")
        talk_type = "poster" if talk.startswith("постерный") else "talk"
        title = re.sub(r"^(постерный )?доклад ", "", talk)
        # в английском списке нет первой записи русского
        en_item = en_conf[index - 1] if index >= 1 else None
        en_location = en_title = None
        if en_item is not None:
            en_location, en_year = field(en_item, "date").split(", ", 1)
            if en_year != parse_period(dates)[0][:4]:
                en_item = None
        if en_item is not None:
            en_title = re.sub(r"^report ", "", field(en_item, "report"))
            matched += 1
        entry = {
            "id": CONFERENCE_IDS[index],
            "event": T(field(item, "conference"), field(en_item, "conference") if en_item else None),
            "talkTitle": T(title, en_title),
            "location": T(location, en_location if en_item else None),
            "talkType": talk_type,
        }
        with_dates(entry, dates, field(item, "conference"))
        put(entry, "tags", tags_for(entry["id"]))
        conferences.append(entry)
    data["conferences"] = conferences
    count_en("Конференции", matched, len(conferences))
    counts.append(("Исследования → Конференции", len(conferences), f"записей: {len(conferences)}", ""))

    # ----- гранты -----
    grants = []
    en_grants = section_by_title(en, "Grants")["items"]
    for index, item in enumerate(section_by_title(ru, "Гранты")["items"]):
        m = re.match(r"^(.+?): ([\d-]+) (.+)$", field(item, "title"))
        me = re.match(r"^(.+?): ([\d-]+) (.+)$", field(en_grants[index], "title"))
        assert m.group(2) == me.group(2)
        entry = {
            "id": GRANT_IDS[index],
            "funder": T(m.group(1), me.group(1)),
            "number": m.group(2),
            "title": T(m.group(3), me.group(3)),
            "role": T(field(item, "role"), field(en_grants[index], "role")),
        }
        with_dates(entry, field(item, "duration"), field(item, "title"))
        put(entry, "tags", tags_for(entry["id"]))
        grants.append(entry)
    data["grants"] = grants
    count_en("Гранты", len(en_grants), len(grants))
    counts.append(("Исследования → Гранты", len(grants), f"записей: {len(grants)}", ""))

    # ----- проекты -----
    data["projects"] = []
    counts.append(("Проекты", 0, "0 записей", "раздел на старом сайте скрыт и пуст"))

    # ----- материалы -----
    materials = []
    en_copy = section_by_title(en, "Copyrights")["items"]
    ru_copy = section_by_title(ru, "Авторские права")["items"]
    matched = 0
    for index, item in enumerate(ru_copy):
        year = int(field(item, "date"))
        en_item = next((c for c in en_copy if int(field(c, "date")) == year), None)
        matched += en_item is not None
        g = lambda cls: field(en_item, cls) if en_item is not None else None
        entry = {
            "id": COPYRIGHT_IDS[index],
            "kind": "course",
            "title": T(field(item, "title"), g("title")),
            "description": T(field(item, "description"), g("description")),
            "year": year,
            "copyright": field(item, "subtitle"),
            "tags": tags_for(COPYRIGHT_IDS[index]),
            "hidden": True,
        }
        materials.append(entry)
    count_en("Авторские права", matched, len(ru_copy))
    counts.append(("Авторские права", len(ru_copy), f"{len(ru_copy)} записи в materials", "все с hidden: true"))

    blocks = re.findall(
        r'<h2 class="index">(.*?)</h2>\s*<div class="description">(.*?)</div>\s*<div class="block_content">(.*?)</div>',
        index_text,
        flags=re.S,
    )
    links_total = 0
    report["index_blocks"] = []
    for heading, description, content in blocks:
        heading, description = clean(heading), clean(description)
        year = int(re.search(r"(\d{4})$", description).group(1))
        links = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', content, flags=re.S)
        report["index_blocks"].append((heading, description, len(links)))
        for url, text in links:
            text = clean(text)
            if text.startswith(("Мастер-класс", "Воркшоп")):
                kind = "workshop"
            elif text == "Книга":
                kind = "book"
            else:
                kind = "other"
            entry_id = INDEX_MATERIAL_IDS[links_total]
            materials.append(
                {
                    "id": entry_id,
                    "kind": kind,
                    "title": T(text),
                    "description": T(description),
                    "context": T(heading),
                    "year": year,
                    "url": url if url.startswith("http") else "https://angelgardt.github.io" + url,
                    "tags": tags_for(entry_id),
                    "hidden": True,
                }
            )
            links_total += 1
    data["materials"] = materials
    counts.append(
        (
            "Старая главная: список материалов",
            f"{len(blocks)} блоков, {links_total} ссылок",
            f"{links_total} записей в materials",
            "одна ссылка = одна запись; все с hidden: true",
        )
    )

    # ----- контакты -----
    head = ru_text[: ru_text.index("<h2")]
    contacts = []
    skipped_contacts = []
    for href, icon, attrs in re.findall(r'<a class="contact" href="([^"]*)"[^>]*>\s*<img src="[^"]*/(\w+)\.svg"([^>]*)>', head):
        kind = CONTACT_KINDS.get(icon, icon)
        if not href:
            skipped_contacts.append(icon)
            continue
        entry = {"id": kind, "kind": kind}
        if kind == "email":
            entry["label"] = href.replace("mailto:", "")
        entry["url"] = href
        entry["visible"] = kind in VISIBLE_CONTACTS
        if kind == "email":
            entry["primary"] = True
        if "hidden" in attrs:
            entry["notes"] = "На старом сайте значок был скрыт"
        contacts.append(entry)
    data["contacts"] = contacts
    report["skipped_contacts"] = skipped_contacts
    counts.append(
        (
            "Шапка: контакты",
            len(contacts) + len(skipped_contacts),
            f"записей: {len(contacts)}",
            f"не перенесены пустые ссылки: {', '.join(skipped_contacts)}",
        )
    )

    # ----- профиль и теги -----
    en_head = en_text[: en_text.index("<h2")]
    name_ru = clean(re.search(r"<h1>(.*?)</h1>", head, re.S).group(1))
    name_en = clean(re.search(r"<h1>(.*?)</h1>", en_head, re.S).group(1))
    loc_ru = clean(re.search(r'<p class="current_location">(.*?)<', head, re.S).group(1)).rstrip(",")
    loc_en = clean(re.search(r'<p class="current_location">(.*?)<', en_head, re.S).group(1)).rstrip(",")
    data["profile"] = {
        "name": T(name_ru, name_en),
        "authorName": name_ru.split()[-1],
        "positioning": T("Преподаю статистику, анализ данных и психометрику", "TODO"),
        "location": T(loc_ru, loc_en),
        "photo": "src/assets/photo.png",
        "focusAreas": [
            {"id": "stats", "title": T("статистика и анализ данных", "TODO"), "text": T("TODO", "TODO"), "tag": "stats"},
            {
                "id": "psychometrics",
                "title": T("психометрика и дизайн исследований", "TODO"),
                "text": T("TODO", "TODO"),
                "tag": "psychometrics",
            },
            {"id": "teaching", "title": T("преподавание", "TODO"), "text": T("TODO", "TODO"), "tag": "teaching"},
        ],
        "notes": "Позиционирование и названия направлений — временные, из раздела 13 ТЗ. Тексты карточек и переводы пишет владелец.",
    }
    data["tags"] = [{"id": tag_id, "label": T(label)} for tag_id, label in TAGS]

    report["counts"] = counts
    report["comments"] = [clean(c).strip("<!-> ") for c in ru_comments]
    return data


# ---------------------------------------------------------------------------
# Запись YAML
# ---------------------------------------------------------------------------

BARE_KEYS = {"id", "kind", "level", "talkType", "status", "position", "tag"}
HEADERS = {
    "profile": "Кто владелец сайта. Один объект.",
    "contacts": "Каналы связи. На сайте показываются только записи с visible: true.",
    "tags": "Словарь направлений. На эти id ссылается поле tags в остальных файлах.",
    "positions": "Места работы и роли. Курсы позиции лежат в courses.yaml.",
    "courses": "Курсы, которые вёл владелец. Повторные запуски курса — в runs.",
    "education": "Основное образование.",
    "extra-education": "Дополнительное образование: повышение квалификации, школы, MOOC.",
    "achievements": "Награды, статусы, благодарности.",
    "languages": "Языки.",
    "skills": "Навыки по группам.",
    "interests": "Интересы по группам.",
    "projects": "Исследовательские и прикладные проекты. На старом сайте раздел был пуст.",
    "grants": "Гранты.",
    "conferences": "Доклады на конференциях.",
    "publications": "Публикации.",
    "materials": "Авторские учебные материалы. Пока все скрыты (hidden: true) — до пересмотра владельцем.",
}


def q(value):
    return json.dumps(value, ensure_ascii=False)


def scalar(key, value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return value if key in BARE_KEYS else q(value)


def is_text(value):
    return isinstance(value, dict) and set(value) <= {"ru", "en"} and "ru" in value


def inline_text(value):
    return "{ " + ", ".join(f"{k}: {q(v)}" for k, v in value.items()) + " }"


def emit(key, value, indent, lines, dash=False):
    """Пишет пару «ключ: значение» с отступом. dash — первая строка элемента списка."""
    pad = " " * indent
    lead = pad[:-2] + "- " if dash else pad
    if is_text(value):
        line = f"{lead}{key}: {inline_text(value)}"
        if len(line) <= 96:
            lines.append(line)
        else:
            lines.append(f"{lead}{key}:")
            for k, v in value.items():
                lines.append(f"{pad}  {k}: {q(v)}")
    elif isinstance(value, dict):
        lines.append(f"{lead}{key}:")
        for k, v in value.items():
            emit(k, v, indent + 2, lines)
    elif isinstance(value, list):
        if not value:
            lines.append(f"{lead}{key}: []")
        elif all(isinstance(v, str) for v in value):
            rendered = [v if key == "tags" else q(v) for v in value]
            line = f"{lead}{key}: [{', '.join(rendered)}]"
            if len(line) <= 96:
                lines.append(line)
            else:
                lines.append(f"{lead}{key}:")
                lines.extend(f"{pad}  - {r}" for r in rendered)
        else:
            lines.append(f"{lead}{key}:")
            for element in value:
                if is_text(element):
                    line = f"{pad}  - {inline_text(element)}"
                    if len(line) <= 96:
                        lines.append(line)
                    else:
                        first = True
                        for k, v in element.items():
                            lines.append(f"{pad}  {'- ' if first else '  '}{k}: {q(v)}")
                            first = False
                else:
                    first = True
                    for k, v in element.items():
                        emit(k, v, indent + 4, lines, dash=first)
                        first = False
    else:
        lines.append(f"{lead}{key}: {scalar(key, value)}")


def write_yaml(name, value):
    lines = [f"# yaml-language-server: $schema=./schemas/{name}.schema.json", f"# {HEADERS[name]}", ""]
    if isinstance(value, list):
        if not value:
            lines.append("[]")
        for entry in value:
            first = True
            for k, v in entry.items():
                emit(k, v, 2, lines, dash=first)
                first = False
            lines.append("")
    else:
        for k, v in value.items():
            emit(k, v, 0, lines)
    (OUT / f"{name}.yaml").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Сводка для отчёта
# ---------------------------------------------------------------------------


def write_summary(data):
    """Пишет migration/generated.md — таблицы, которые вставлены в REPORT.md."""
    out = ["<!-- Файл создан скриптом migration/migrate.py. Руками не править. -->", ""]
    out += ["## Число записей", "", "| Раздел старого сайта | Записей там | В YAML | Пояснение |", "| --- | --- | --- | --- |"]
    out += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in report["counts"]]

    out += ["", "## Группировка курсов по позициям", ""]
    positions = {p["id"]: p for p in data["positions"]}
    courses = {c["id"]: c for c in data["courses"]}
    for pos_id, course_ids in report["grouping"].items():
        p = positions[pos_id]
        unit = f", {p['unit']['ru']}" if "unit" in p else ""
        out.append(f"- **`{pos_id}`** — {p['role']['ru']}{unit}, {p['organization']['ru']}")
        for cid in course_ids:
            if cid not in courses:
                out.append("  - без курсов: позиция перенесена одной записью")
                continue
            c = courses[cid]
            runs = "; ".join(
                f"{r['start']}—{r.get('end', '')}" + (f" (роль: {r['role']['ru']})" if "role" in r else "") for r in c["runs"]
            )
            out.append(f"  - `{cid}` — {c['title']['ru']}: {runs}")

    out += ["", "## Предложенные теги", "", "| Файл | id | Теги |", "| --- | --- | --- |"]
    for name in ["positions", "courses", "education", "extra-education", "achievements", "conferences", "grants", "publications", "materials"]:
        for entry in data[name]:
            tags = ", ".join(entry.get("tags", [])) or "—"
            out.append(f"| {name} | `{entry['id']}` | {tags} |")

    out += ["", "## Кандидаты в featured", ""]
    for name, entry_id in FEATURED_CANDIDATES:
        entry = next(e for e in data[name] if e["id"] == entry_id)
        title = entry.get("role", entry.get("program", {})).get("ru", "")
        out.append(f"- `{name}` / `{entry_id}` — {title}")

    out += ["", "## Записи «по настоящее время»", ""]
    out += [f"- {line}" for line in report["present"]]
    out += ["", "## Записи, помеченные на старом сайте как текущие (класс current_item)", ""]
    out += [f"- {line}" for line in report["current"]]

    out += ["", "## Нестандартные даты", ""]
    out += [f"- без дат («по запросу организаторов»): {line}" for line in report["nodates"]]
    out += [f"- сезон вместо месяца, оставлены годы: {line}" for line in report["season"]]
    out += [f"- год начала выведен из дат: {line}" for line in report["yearwrap"]]

    out += ["", "## Расхождения со старым прототипом (education.json)", ""]
    out += [f"- {line}" for line in report["proto"]]

    out += ["", "## Скрытое на старом сайте", ""]
    out += [f"- {line}" for line in report["hidden"]]
    out += [f"- закомментированный блок: «{c}»" for c in report["comments"]]

    out += ["", "## Английские тексты: что перенесено", "", "| Раздел | Записей с парой в английском CV | Всего |", "| --- | --- | --- |"]
    out += [f"| {name} | {m} | {t} |" for name, (m, t) in report["en_matched"].items()]
    out += ["", "## Английские записи без пары (не перенесены)", ""]
    out += [f"- {line}" for line in report["en_unmatched"]]
    out += ["", "## Английские тексты, пропущенные намеренно", ""]
    out += [f"- {line}" for line in report["en_skipped"]]
    out += ["", "## Блоки старой главной", ""]
    out += [f"- {h} — {d}: ссылок {n}" for h, d, n in report["index_blocks"]]
    (ROOT / "migration" / "generated.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    data = build()
    existing = [p.name for p in OUT.glob("*.yaml")] if OUT.exists() else []
    if existing and "--force" not in sys.argv:
        sys.exit(
            "В src/data уже есть файлы данных. Повторная миграция сотрёт ручные правки.\n"
            "Если это действительно нужно, запустите с --force."
        )
    OUT.mkdir(parents=True, exist_ok=True)
    for name, value in data.items():
        write_yaml(name, value)
    write_summary(data)
    for name, value in data.items():
        size = len(value["groups"]) if isinstance(value, dict) and "groups" in value else len(value) if isinstance(value, list) else 1
        print(f"{name}: {size}")


if __name__ == "__main__":
    main()
