import { createI18n } from 'vue-i18n'

import ruCommon from './locales/ru/common.json'
import ruAbout from './locales/ru/about/common.json'
import ruEducation from './locales/ru/about/education.json'

import enCommon from './locales/en/common.json'
import enAbout from './locales/en/about/common.json'
import enEducation from './locales/en/about/education.json'

const savedLocale = localStorage.getItem('locale') || 'ru'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'ru',
  messages: {
    ru: {
      ...ruCommon,
      about: ruAbout,
      education: ruEducation,
    },
    en: {
      ...enCommon,
      about: enAbout,
      education: enEducation,
    },
  },
})

export default i18n
