/* eslint-disable max-lines */
// import all namespaces English
import brain_en from "../../../public/locales/en/brain.json";
import chat_en from "../../../public/locales/en/chat.json";
import config_en from "../../../public/locales/en/config.json";
import contact_en from "../../../public/locales/en/contact.json";
import delete_brain_en from "../../../public/locales/en/deleteOrUnsubscribeFromBrain.json";
import explore_en from "../../../public/locales/en/explore.json";
import external_api_definition_en from "../../../public/locales/en/external_api_definition.json";
import home_en from "../../../public/locales/en/home.json";
import invitation_en from "../../../public/locales/en/invitation.json";
import knowlegde_en from "../../../public/locales/en/knowledge.json";
import login_en from "../../../public/locales/en/login.json";
import logout_en from "../../../public/locales/en/logout.json";
import monetization_en from "../../../public/locales/en/monetization.json";
import translation_en from "../../../public/locales/en/translation.json";
import upload_en from "../../../public/locales/en/upload.json";
import user_en from "../../../public/locales/en/user.json";
// import all namespaces Vietnamese
import brain_vi from "../../../public/locales/vi/brain.json";
import chat_vi from "../../../public/locales/vi/chat.json";
import config_vi from "../../../public/locales/vi/config.json";
import contact_vi from "../../../public/locales/vi/contact.json";
import delete_brain_vi from "../../../public/locales/vi/deleteOrUnsubscribeFromBrain.json";
import explore_vi from "../../../public/locales/vi/explore.json";
import external_api_definition_vi from "../../../public/locales/vi/external_api_definition.json";
import home_vi from "../../../public/locales/vi/home.json";
import invitation_vi from "../../../public/locales/vi/invitation.json";
import knowlegde_vi from "../../../public/locales/vi/knowledge.json";
import login_vi from "../../../public/locales/vi/login.json";
import logout_vi from "../../../public/locales/vi/logout.json";
import monetization_vi from "../../../public/locales/vi/monetization.json";
import translation_vi from "../../../public/locales/vi/translation.json";
import upload_vi from "../../../public/locales/vi/upload.json";
import user_vi from "../../../public/locales/vi/user.json";
//type all translations
export type Translations = {
  brain: typeof import("../../../public/locales/vi/brain.json");
  chat: typeof import("../../../public/locales/vi/chat.json");
  config: typeof import("../../../public/locales/vi/config.json");
  contact: typeof import("../../../public/locales/vi/contact.json");
  delete_or_unsubscribe_from_brain: typeof import("../../../public/locales/vi/deleteOrUnsubscribeFromBrain.json");
  explore: typeof import("../../../public/locales/vi/explore.json");
  home: typeof import("../../../public/locales/vi/home.json");
  invitation: typeof import("../../../public/locales/vi/invitation.json");
  login: typeof import("../../../public/locales/vi/login.json");
  logout: typeof import("../../../public/locales/vi/logout.json");
  monetization: typeof import("../../../public/locales/vi/monetization.json");
  translation: typeof import("../../../public/locales/vi/translation.json");
  upload: typeof import("../../../public/locales/vi/upload.json");
  user: typeof import("../../../public/locales/vi/user.json");
  knowledge: typeof import("../../../public/locales/vi/knowledge.json");
  external_api_definition: typeof import("../../../public/locales/vi/external_api_definition.json");
};

enum SupportedLanguages {
  en = "en",
	vi = "vi",
}

export const defaultNS = "translation";
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
    external_api_definition: external_api_definition_en,
  },
	vi : {
		brain: brain_vi,
    chat: chat_vi,
    config: config_vi,
    contact: contact_vi,
    explore: explore_vi,
    home: home_vi,
    invitation: invitation_vi,
    login: login_vi,
    logout: logout_vi,
    monetization: monetization_vi,
    translation: translation_vi,
    upload: upload_vi,
    user: user_vi,
    delete_or_unsubscribe_from_brain: delete_brain_vi,
    knowledge: knowlegde_vi,
    external_api_definition: external_api_definition_vi,
	},

} as const;
