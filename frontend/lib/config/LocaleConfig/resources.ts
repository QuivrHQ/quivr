/* eslint-disable max-lines */
// import all namespaces English
import brain_en from '../../../public/locales/en/brain.json';
import chat_en from '../../../public/locales/en/chat.json';
import config_en from '../../../public/locales/en/config.json';
import contact_en from '../../../public/locales/en/contact.json';
import delete_brain_en from '../../../public/locales/en/deleteOrUnsubscribeFromBrain.json';
import explore_en from '../../../public/locales/en/explore.json';
import external_api_definition_en from '../../../public/locales/en/external_api_definition.json';
import home_en from '../../../public/locales/en/home.json';
import invitation_en from '../../../public/locales/en/invitation.json';
import knowlegde_en from '../../../public/locales/en/knowledge.json';
import login_en from '../../../public/locales/en/login.json';
import logout_en from '../../../public/locales/en/logout.json';
import monetization_en from '../../../public/locales/en/monetization.json';
import translation_en from '../../../public/locales/en/translation.json';
import upload_en from '../../../public/locales/en/upload.json';
import user_en from '../../../public/locales/en/user.json';
import vaccineTruth_en from '../../../public/locales/en/vaccineTruth.json';
// import all namespaces Spanish
// import all namespaces French
// import all namespaces Portuguese
// import all namespaces Russian
// import all namespaces Simplified Chinese
import brain_zh_cn from '../../../public/locales/zh-cn/brain.json';
import chat_zh_cn from '../../../public/locales/zh-cn/chat.json';
import config_zh_cn from '../../../public/locales/zh-cn/config.json';
import contact_zh_cn from '../../../public/locales/zh-cn/contact.json';
import delete_brain_zh_cn from '../../../public/locales/zh-cn/deleteOrUnsubscribeFromBrain.json';
import explore_zh_cn from '../../../public/locales/zh-cn/explore.json';
import external_api_definition_zh_cn from '../../../public/locales/zh-cn/external_api_definition.json';
import home_zh_cn from '../../../public/locales/zh-cn/home.json';
import invitation_zh_cn from '../../../public/locales/zh-cn/invitation.json';
import knowlegde_zh_cn from '../../../public/locales/zh-cn/knowledge.json';
import login_zh_cn from '../../../public/locales/zh-cn/login.json';
import logout_zh_cn from '../../../public/locales/zh-cn/logout.json';
import monetization_zh_cn from '../../../public/locales/zh-cn/monetization.json';
import translation_zh_cn from '../../../public/locales/zh-cn/translation.json';
import upload_zh_cn from '../../../public/locales/zh-cn/upload.json';
import user_zh_cn from '../../../public/locales/zh-cn/user.json';
import vaccineTruth_zh_cn from '../../../public/locales/zh-cn/vaccineTruth.json';

//type all translations
export type Translations = {
  brain: typeof import('../../../public/locales/en/brain.json');
  chat: typeof import('../../../public/locales/en/chat.json');
  config: typeof import('../../../public/locales/en/config.json');
  contact: typeof import('../../../public/locales/en/contact.json');
  delete_or_unsubscribe_from_brain: typeof import('../../../public/locales/en/deleteOrUnsubscribeFromBrain.json');
  explore: typeof import('../../../public/locales/en/explore.json');
  home: typeof import('../../../public/locales/en/home.json');
  invitation: typeof import('../../../public/locales/en/invitation.json');
  login: typeof import('../../../public/locales/en/login.json');
  logout: typeof import('../../../public/locales/en/logout.json');
  monetization: typeof import('../../../public/locales/en/monetization.json');
  translation: typeof import('../../../public/locales/en/translation.json');
  upload: typeof import('../../../public/locales/en/upload.json');
  user: typeof import('../../../public/locales/en/user.json');
  knowledge: typeof import('../../../public/locales/en/knowledge.json');
  vaccineTruth: typeof import('../../../public/locales/en/vaccineTruth.json');
  external_api_definition: typeof import('../../../public/locales/en/external_api_definition.json');
};

enum SupportedLanguages {
  en = 'en',
  // es = "es",
  // fr = "fr",
  // ptbr = "ptbr",
  // ru = "ru",
  zh_cn = 'zh_cn',
}

export const defaultNS = 'translation';
export const resources: Record<SupportedLanguages, Translations> = {
  en: {
    brain: brain_en,
    chat: chat_en,
    config: config_en,
    contact: contact_en,
    explore: explore_en,
    home: home_en,
    invitation: invitation_en,
    login: login_en,
    logout: logout_en,
    monetization: monetization_en,
    translation: translation_en,
    upload: upload_en,
    user: user_en,
    delete_or_unsubscribe_from_brain: delete_brain_en,
    knowledge: knowlegde_en,
    vaccineTruth: vaccineTruth_en,
    external_api_definition: external_api_definition_en,
  },
  // es: {
  //   brain: brain_es,
  //   chat: chat_es,
  //   config: config_es,
  //   contact: contact_es,
  //   explore: explore_es,
  //   home: home_es,
  //   invitation: invitation_es,
  //   login: login_es,
  //   logout: logout_es,
  //   monetization: monetization_es,
  //   translation: translation_es,
  //   upload: upload_es,
  //   user: user_es,
  //   delete_or_unsubscribe_from_brain: delete_brain_es,
  //   knowledge: knowlegde_es,
  //   vaccineTruth: vaccineTruth_es,
  //   external_api_definition: external_api_definition_es,
  // },
  // fr: {
  //   brain: brain_fr,
  //   chat: chat_fr,
  //   config: config_fr,
  //   contact: contact_fr,
  //   explore: explore_fr,
  //   home: home_fr,
  //   invitation: invitation_fr,
  //   login: login_fr,
  //   logout: logout_fr,
  //   monetization: monetization_fr,
  //   translation: translation_fr,
  //   upload: upload_fr,
  //   user: user_fr,
  //   delete_or_unsubscribe_from_brain: delete_brain_fr,
  //   knowledge: knowlegde_fr,
  //   vaccineTruth: vaccineTruth_fr,
  //   external_api_definition: external_api_definition_fr,
  // },
  // ptbr: {
  //   brain: brain_ptbr,
  //   chat: chat_ptbr,
  //   config: config_ptbr,
  //   contact: contact_ptbr,
  //   explore: explore_ptbr,
  //   home: home_ptbr,
  //   invitation: invitation_ptbr,
  //   login: login_ptbr,
  //   logout: logout_ptbr,
  //   monetization: monetization_ptbr,
  //   translation: translation_ptbr,
  //   upload: upload_ptbr,
  //   user: user_ptbr,
  //   delete_or_unsubscribe_from_brain: delete_brain_ptbr,
  //   knowledge: knowlegde_ptbr,
  //   vaccineTruth: vaccineTruth_ptbr,
  //   external_api_definition: external_api_definition_ptbr,
  // },
  // ru: {
  //   brain: brain_ru,
  //   chat: chat_ru,
  //   config: config_ru,
  //   contact: contact_ru,
  //   explore: explore_ru,
  //   home: home_ru,
  //   invitation: invitation_ru,
  //   login: login_ru,
  //   logout: logout_ru,
  //   monetization: monetization_ru,
  //   translation: translation_ru,
  //   upload: upload_ru,
  //   user: user_ru,
  //   delete_or_unsubscribe_from_brain: delete_brain_ru,
  //   knowledge: knowlegde_ru,
  //   vaccineTruth: vaccineTruth_ru,
  //   external_api_definition: external_api_definition_ru,
  // },
  zh_cn: {
    brain: brain_zh_cn,
    chat: chat_zh_cn,
    config: config_zh_cn,
    contact: contact_zh_cn,
    explore: explore_zh_cn,
    home: home_zh_cn,
    invitation: invitation_zh_cn,
    login: login_zh_cn,
    logout: logout_zh_cn,
    monetization: monetization_zh_cn,
    translation: translation_zh_cn,
    upload: upload_zh_cn,
    user: user_zh_cn,
    delete_or_unsubscribe_from_brain: delete_brain_zh_cn,
    knowledge: knowlegde_zh_cn,
    vaccineTruth: vaccineTruth_zh_cn,
    external_api_definition: external_api_definition_zh_cn,
  },
} as const;
