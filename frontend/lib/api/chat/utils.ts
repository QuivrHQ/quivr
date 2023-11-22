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

export const QUESTION_LIST_ZH_CN = [
  "新冠病毒的起源是哪里?",
  "文贵先生针对新冠病毒疫苗在什么时间点发出过警告?",
  "美国疫苗伤害听证会中, 提到了哪些疫苗伤害?",
  "CDC参与了新冠病毒功能增强实验吗?",
];
export const QUESTION_LIST_EN = [
  "Where is the origin of the Covid-19 virus?",
  "What Miles Guo says about Covid-19 virus and vaccine?",
  "What vaccine injuries were discussed in the US Congress hearing?",
  "Is the CDC involved in the new coronavirus function enhancement experiment?",
];

export const getRandomQuestion = (
  lang: string | undefined,
  count: number
): string[] => {
  const sourceArr =
    lang === "en" ? QUESTION_LIST_EN.slice() : QUESTION_LIST_ZH_CN.slice();
  const res: string[] = [];

  for (let i = 0; i < count; i++) {
    const randomIndex = Math.floor(Math.random() * sourceArr.length);
    res.push(sourceArr[randomIndex]);
    sourceArr.splice(randomIndex, 1);
  }

  return res.slice(0, count);
};

export const updateQuestion = (
  lang: string | undefined,
  questions: string[],
  question: string
): string[] => {
  const sourceArr =
    lang === "en" ? QUESTION_LIST_EN.slice() : QUESTION_LIST_ZH_CN.slice();

  const unAskedQuestions = sourceArr.filter(
    (item: string) => !questions.includes(item)
  );

  const filterExistedQuestions = questions.filter(
    (item: string) => item !== question
  );

  if (unAskedQuestions.length > 0) {
    filterExistedQuestions.unshift(unAskedQuestions[0]);
  }

  return filterExistedQuestions;
};
