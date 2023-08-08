// import all namespaces English
import brain_en from "../../../public/locales/en/brain.json";
import chat_en from "../../../public/locales/en/chat.json";
import config_en from "../../../public/locales/en/config.json";
import delete_brain_en from "../../../public/locales/en/deleteBrain.json";
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
import delete_brain_es from "../../../public/locales/es/deleteBrain.json";
import explore_es from "../../../public/locales/es/explore.json";
import login_es from "../../../public/locales/es/login.json";
import logout_es from "../../../public/locales/es/logout.json";
import signUp_es from "../../../public/locales/es/signUp.json";
import translation_es from "../../../public/locales/es/translation.json";
import updatePassword_es from "../../../public/locales/es/updatePassword.json";
import upload_es from "../../../public/locales/es/upload.json";
import user_es from "../../../public/locales/es/user.json";
// import all namespaces French
import brain_fr from "../../../public/locales/fr/brain.json";
import chat_fr from "../../../public/locales/fr/chat.json";
import config_fr from "../../../public/locales/fr/config.json";
import delete_brain_fr from "../../../public/locales/fr/deleteBrain.json";
import explore_fr from "../../../public/locales/fr/explore.json";
import login_fr from "../../../public/locales/fr/login.json";
import logout_fr from "../../../public/locales/fr/logout.json";
import signUp_fr from "../../../public/locales/fr/signUp.json";
import translation_fr from "../../../public/locales/fr/translation.json";
import updatePassword_fr from "../../../public/locales/fr/updatePassword.json";
import upload_fr from "../../../public/locales/fr/upload.json";
import user_fr from "../../../public/locales/fr/user.json";

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
    delete_brain: delete_brain_en,
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
    user: user_es,
    delete_brain: delete_brain_es,
  },
  fr: {
    brain: brain_fr,
    chat: chat_fr,
    config: config_fr,
    explore: explore_fr,
    login: login_fr,
    logout: logout_fr,
    signUp: signUp_fr,
    translation: translation_fr,
    updatePassword: updatePassword_fr,
    upload: upload_fr,
    user: user_fr,
    delete_brain: delete_brain_fr,
  },
} as const;
