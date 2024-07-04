import Button from "@/lib/components/ui/Button";
import Icon from "@/lib/components/ui/Icon/Icon";

import { useGithubLogin } from "./hooks/useGithubLogin";
import styles from "./index.module.scss";

export const GithubLoginButton = (): JSX.Element => {
  const { isPending, signInWithGithub } = useGithubLogin();

  return (
    <Button
      onClick={() => void signInWithGithub()}
      isLoading={isPending}
      type="button"
      className={styles.button}
    >
      <Icon name="github" size="small" color="primary" />
      <span>Continue with Github</span>
    </Button>
  );
};
