import { BeautifulMentionsTheme } from "lexical-beautiful-mentions";

const mentionsStyle =
  "px-1 mx-px align-baseline inline-block rounded break-words cursor-pointer select-none leading-5";
const mentionsStyleFocused =
  "outline-none shadow-md shadow-gray-500 dark:shadow-gray-900";

const beautifulMentionsTheme: BeautifulMentionsTheme = {
  "@": `${mentionsStyle} dark:bg-green-500 bg-green-600 dark:text-gray-950 text-white`,
  "@Focused": mentionsStyleFocused,
  "#": `${mentionsStyle} dark:bg-blue-400 bg-blue-600 dark:text-gray-950 text-white`,
  "#Focused": mentionsStyleFocused,
  "due:": `${mentionsStyle} dark:bg-yellow-400 bg-yellow-600 dark:text-gray-950 text-white`,
  "due:Focused": mentionsStyleFocused,
  // 👇 use a configuration object if you need to apply different styles to trigger and value
  "rec:": {
    trigger: `dark:text-blue-400 text-blue-950`,
    value: `dark:text-orange-400 text-orange-950`,
    container:
      "mx-[2px] px-[4px] rounded ring-1 ring-gray-400 dark:ring-gray-700 cursor-pointer",
    containerFocused:
      "mx-[2px] px-[4px] rounded ring-1 ring-gray-500 dark:ring-gray-400 cursor-pointer",
  },
  "\\w+:": `${mentionsStyle} dark:bg-gray-400 bg-gray-500 dark:text-gray-950 text-white`,
  "\\w+:Focused": mentionsStyleFocused,
};

export const theme = {
  ltr: "text-left",
  rtl: "text-right",
  beautifulMentions: beautifulMentionsTheme,
};
