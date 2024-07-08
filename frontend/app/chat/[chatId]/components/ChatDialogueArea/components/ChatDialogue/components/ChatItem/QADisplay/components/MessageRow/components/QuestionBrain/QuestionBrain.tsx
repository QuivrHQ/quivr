import { Fragment } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./QuestionBrain.module.scss";

type QuestionBrainProps = {
  brainName?: string | null;
};
export const QuestionBrain = ({
  brainName,
}: QuestionBrainProps): JSX.Element => {
  if (brainName === undefined || brainName === null) {
    return <Fragment />;
  }

  return (
    <div data-testid="brain-tags" className={styles.brain_name_wrapper}>
      <Icon name="brain" size="normal" color="black" />
      <span className={styles.brain_name}>{brainName}</span>
    </div>
  );
};
