import styles from "./PublicPrompts.module.scss";
import { PublicPromptsList } from "./PublicPromptsList/PublicPromptsList";
import { usePublicPrompts } from "./hooks/usePublicPrompts";

type PublicPromptsProps = {
  onSelect: ({ title, content }: { title: string; content: string }) => void;
};

export const PublicPrompts = ({
  onSelect,
}: PublicPromptsProps): JSX.Element => {
  const { handleChange, publicPrompts } = usePublicPrompts({
    onSelect,
  });

  return (
    <div className={styles.selector_wrapper}>
      <PublicPromptsList
        options={publicPrompts}
        onChange={handleChange}
        onSelect={onSelect}
      />
    </div>
  );
};
