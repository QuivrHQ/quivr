import { InfoDisplayer } from "@/lib/components/ui/InfoDisplayer/InfoDisplayer";

type InfoDisplayerProps = {
  email: string;
};

export const Settings = ({ email }: InfoDisplayerProps): JSX.Element => {
  return (
    <div>
      <InfoDisplayer label="Email" iconName="email">
        <span>{email}</span>
      </InfoDisplayer>
    </div>
  );
};
