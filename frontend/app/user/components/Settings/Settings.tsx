import { InfoDisplayer } from "@/lib/components/ui/InfoDisplayer/InfoDisplayer";

import LanguageSelect from "../LanguageSelect/LanguageSelect";

type InfoDisplayerProps = {
  email: string;
};

export const Settings = ({ email }: InfoDisplayerProps): JSX.Element => {
  return (
    <div>
      <InfoDisplayer label="Email" iconName="email">
        <span>{email}</span>
      </InfoDisplayer>
      <LanguageSelect />
    </div>
  );
};
