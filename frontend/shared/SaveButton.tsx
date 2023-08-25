import { ReactElement } from "react";

import Button from "@/lib/components/ui/Button";

interface Props {
  handleSubmit: (checkDirty: boolean) => Promise<void>;
}
export const SaveButton = ({ handleSubmit }: Props): ReactElement => (
  <Button
    variant={"primary"}
    onClick={() => void handleSubmit(true)}
    type="button"
  >
    Save
  </Button>
);
