import { useFeatureIsOn } from "@growthbook/growthbook-react";

import { AddBrainModal as AddBrainModalNew } from "./AddBrainModal";
import { AddBrainModal as AddBrainModalOld } from "../AddBrainModalOld";

type AddBrainModalSelectorProps = {
  triggerClassName?: string;
};

export const AddBrainModalSelector = ({
  triggerClassName,
}: AddBrainModalSelectorProps): JSX.Element => {
  const isNewBrainCreationOn = useFeatureIsOn("new-brain-creation");

  if (isNewBrainCreationOn) {
    return <AddBrainModalNew triggerClassName={triggerClassName} />;
  }

  return <AddBrainModalOld triggerClassName={triggerClassName} />;
};
