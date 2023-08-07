import i18n from 'i18next';
import backend from 'i18next-http-backend';
import { initReactI18next } from 'react-i18next';

i18n.use(backend)
    .use(initReactI18next)
    .init({
        lng: 'en',
        loadPath: '/locales/{{lng}}/{{ns}}.json',
        fallbackLng: 'en', 
        debug: true
    })