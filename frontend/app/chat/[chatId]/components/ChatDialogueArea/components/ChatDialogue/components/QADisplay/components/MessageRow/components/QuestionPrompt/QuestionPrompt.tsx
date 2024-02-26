import { Fragment } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./QuestionPompt.module.scss";

type QuestionProptProps = {
  promptName?: string | null;
};
export const QuestionPrompt = ({
  promptName,
}: QuestionProptProps): JSX.Element => {
  if (promptName === undefined || promptName === null) {
    return <Fragment />;
  }

  return (
    <div data-testid="prompt-tags" className={styles.prompt_name_wrapper}>
      <Icon name="hashtag" color="primary" size="small" />
      <span className={styles.prompt_name}>{promptName}</span>
    </div>
  );
};
