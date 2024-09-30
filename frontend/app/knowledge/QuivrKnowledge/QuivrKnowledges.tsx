import { Icon } from "@/lib/components/ui/Icon/Icon";

const QuivrKnowledges = (): JSX.Element => {
  return (
    <div>
      <Icon
        name={folded ? "chevronRight" : "chevronDown"}
        size="normal"
        color="dark-grey"
        handleHover={true}
      />
      <Image
        src={providerIconUrls[providerGroup.provider]}
        alt={providerGroup.provider}
        width={18}
        height={18}
      />
      <span className={styles.provider_title}>
        {transformConnectionLabel(providerGroup.provider)}
      </span>
    </div>
  );
};

export default QuivrKnowledges;
