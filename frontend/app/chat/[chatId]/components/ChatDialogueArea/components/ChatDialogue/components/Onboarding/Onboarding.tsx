import { Step1 } from "./components";
import { Step2 } from "./components/Step2";
import { Step3 } from "./components/Step3";

export const Onboarding = (): JSX.Element => {
  return (
    <div className="flex flex-col gap-2 mb-3">
      <Step1 />
      <Step2 />
      <Step3 />
    </div>
  );
};
