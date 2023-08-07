// import all namespaces English
import brain_en from "../../../public/locales/en/brain.json";
import chat_en from "../../../public/locales/en/chat.json";
import config_en from "../../../public/locales/en/config.json";
import explore_en from "../../../public/locales/en/explore.json";
import login_en from "../../../public/locales/en/login.json";
import logout_en from "../../../public/locales/en/logout.json";
import signUp_en from "../../../public/locales/en/signUp.json";
import translation_en from "../../../public/locales/en/translation.json";
import updatePassword_en from "../../../public/locales/en/updatePassword.json";
import upload_en from "../../../public/locales/en/upload.json";
import user_en from "../../../public/locales/en/user.json";
// import all namespaces Spanish
import brain_es from "../../../public/locales/es/brain.json";
import chat_es from "../../../public/locales/es/chat.json";
import config_es from "../../../public/locales/es/config.json";
import explore_es from "../../../public/locales/es/explore.json";
import login_es from "../../../public/locales/es/login.json";
import logout_es from "../../../public/locales/es/logout.json";
import signUp_es from "../../../public/locales/es/signUp.json";
import translation_es from "../../../public/locales/es/translation.json";
import updatePassword_es from "../../../public/locales/es/updatePassword.json";
import upload_es from "../../../public/locales/es/upload.json";
import user_es from "../../../public/locales/es/user.json";

export const defaultNS = "translation";
export const resources = {
  en: {
    brain: brain_en,
    chat: chat_en,
    config: config_en,
    explore: explore_en,
    login: login_en,
    logout: logout_en,
    signUp: signUp_en,
    translation: translation_en,
    updatePassword: updatePassword_en,
    upload: upload_en,
    user: user_en,
  },
  es: {
    brain: brain_es,
    chat: chat_es,
    config: config_es,
    explore: explore_es,
    login: login_es,
    logout: logout_es,
    signUp: signUp_es,
    translation: translation_es,
    updatePassword: updatePassword_es,
    upload: upload_es,
    user: user_es
  }
} as const;
