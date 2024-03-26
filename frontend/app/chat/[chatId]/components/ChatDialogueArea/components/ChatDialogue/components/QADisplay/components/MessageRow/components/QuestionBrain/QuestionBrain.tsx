import Image from "next/image";
import { Fragment, useEffect, useState } from "react";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

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
  const { isDarkMode } = useUserSettingsContext();
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
      <Image
        className={isDarkMode ? styles.dark_image : ""}
        src={brainLogoUrl ? brainLogoUrl : "/default_brain_image.png"}
        alt="logo_image"
        width={18}
        height={18}
      />
      <span className={styles.brain_name}>{brainName}</span>
    </div>
  );
};
