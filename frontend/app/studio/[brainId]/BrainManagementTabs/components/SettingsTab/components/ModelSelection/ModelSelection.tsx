import { UUID } from "crypto";

import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { Model } from "@/lib/types/BrainConfig";
import { SaveButton } from "@/shared/SaveButton";

import styles from "./ModelSelection.module.scss";

import { useBrainFormState } from "../../hooks/useBrainFormState";

type ModelSelectionProps = {
  brainId: UUID;
  handleSubmit: (checkDirty: boolean) => Promise<void>;
  hasEditRights: boolean;
  accessibleModels: string[];
};

export const ModelSelection = (props: ModelSelectionProps): JSX.Element => {
  const { model, maxTokens, register, setModel } = useBrainFormState();
  const { handleSubmit, hasEditRights, accessibleModels } = props;

  const accessibleModelOptions = accessibleModels.map((accessibleModel) => {
    return { value: accessibleModel, label: accessibleModel };
  });

  console.info(model);

  return (
    <div className={styles.model_selection_wrapper}>
      <fieldset {...register("model")}>
        <FieldHeader label="Model" iconName="robot" />
        <SingleSelector
          options={accessibleModelOptions}
          onChange={(option) => {
            void handleSubmit(false);
            setModel(option as Model);
          }}
          selectedOption={{ value: model, label: model }}
          placeholder="hey"
          iconName="robot"
        />
      </fieldset>
      <fieldset>
        <FieldHeader label="Max tokens" iconName="hashtag" />
        <div className={styles.max_tokens}>
          <input
            className={styles.slider}
            type="range"
            min="10"
            max={defineMaxTokens(model)}
            value={maxTokens}
            disabled={!hasEditRights}
            {...register("maxTokens")}
          />
          <span>{maxTokens}</span>
        </div>
      </fieldset>
      {hasEditRights && (
        <div>
          <SaveButton handleSubmit={handleSubmit} />
        </div>
      )}
    </div>
  );
};
