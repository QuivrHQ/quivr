import { ChatInput, Feed } from "./components";
import { useActionBar } from "./hooks/useActionBar";

export const ActionsBar = (): JSX.Element => {
  const { isUploading, setIsUploading } = useActionBar();

  return (
    <div className={isUploading ? "h-full" : ""}>
      {isUploading && (
        <div className="shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
          <Feed onClose={() => setIsUploading(false)} />
        </div>
      )}
      <div className="flex mt-1 flex-col w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
        <ChatInput isUploading={isUploading} setIsUploading={setIsUploading} />
      </div>
    </div>
  );
};
