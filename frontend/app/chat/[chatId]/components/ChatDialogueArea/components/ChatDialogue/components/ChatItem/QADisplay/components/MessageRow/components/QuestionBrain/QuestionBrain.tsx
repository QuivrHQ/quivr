import Image from "next/image";
import { Fragment } from "react";

import styles from "./QuestionBrain.module.scss";

type QuestionBrainProps = {
  brainName?: string | null;
  imageUrl?: string;
  snippetColor?: string;
  snippetEmoji?: string;
};
export const QuestionBrain = ({
  brainName,
  imageUrl,
  snippetColor,
  snippetEmoji,
}: QuestionBrainProps): JSX.Element => {
  if (brainName === undefined || brainName === null) {
    return <Fragment />;
  }

  return (
    <div data-testid="brain-tags" className={styles.brain_name_wrapper}>
      {imageUrl ? (
        <Image
          className={styles.brain_image}
          src={imageUrl}
          alt=""
          width={24}
          height={24}
        />
      ) : (
        <div
          className={styles.brain_snippet}
          style={{ backgroundColor: snippetColor }}
        >
          <span>{snippetEmoji}</span>
        </div>
      )}
      <span className={styles.brain_name}>{brainName}</span>
    </div>
  );
};
