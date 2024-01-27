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
      <Icon name="brain" color="primary" size="normal" />
      <span>{brainName}</span>
    </div>
  );
};
