import Image from "next/image";
import { Fragment, useEffect, useState } from "react";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./QuestionBrain.module.scss";

type QuestionBrainProps = {
  brainName?: string | null;
  brainId?: string;
};
export const QuestionBrain = ({
  brainName,
  brainId,
}: QuestionBrainProps): JSX.Element => {
  const [brainLogoUrl, setBrainLogoUrl] = useState<string | undefined>(
    undefined
  );

  const { getBrain } = useBrainApi();

  const getBrainLogoUrl = async () => {
    if (brainId) {
      try {
        const brain = await getBrain(brainId.toString());
        setBrainLogoUrl(brain?.integration_description?.integration_logo_url);
      } catch (error) {
        console.error(error);
      }
    }
  };

  useEffect(() => {
    void getBrainLogoUrl();
  }, [brainId]);

  if (brainName === undefined || brainName === null) {
    return <Fragment />;
  }

  return (
    <div data-testid="brain-tags" className={styles.brain_name_wrapper}>
      {brainLogoUrl ? (
        <Image src={brainLogoUrl} alt="brainLogo" width={18} height={18} />
      ) : (
        <Icon name="brain" color="primary" size="normal" />
      )}
      <span className={styles.brain_name}>{brainName}</span>
    </div>
  );
};
