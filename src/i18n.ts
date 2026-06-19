import { createI18n } from 'vue-i18n'

import ruCommon from './locales/ru/common.json'
import ruAbout from './locales/ru/about/common.json'
import ruEducation from './locales/ru/about/education.json'

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages: {
    ru: {
      ...ruCommon,
      about: ruAbout,
      education: ruEducation,
    },
  },
})

export default i18n
