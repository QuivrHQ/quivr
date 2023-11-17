export const getBrowserLang = (): string => {
  const browserLang: string = navigator.language;

  let defaultBrowserLang = "";
  if (
    browserLang.toLowerCase() === "us" ||
    browserLang.toLowerCase() === "en" ||
    browserLang.toLowerCase() === "en_us"
  ) {
    defaultBrowserLang = "en";
  } else {
    defaultBrowserLang = "zh_cn";
  }

  return defaultBrowserLang;
};
