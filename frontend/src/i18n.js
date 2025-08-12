import { createI18n } from 'vue-i18n'
import en from './languages/en.json';
import ru from './languages/ru.json';

const messages = {
    en,
    ru
};
const i18n = new createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
});
export default i18n;