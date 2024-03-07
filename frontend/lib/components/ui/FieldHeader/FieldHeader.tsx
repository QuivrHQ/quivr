import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./FieldHeader.module.scss";

import { Icon } from "../Icon/Icon";

type FieldHeaderProps = {
  iconName: string;
  label: string;
  help?: string;
};

export const FieldHeader = ({
  iconName,
  label,
  help,
}: FieldHeaderProps): JSX.Element => {
  return (
    <div className={styles.field_header_wrapper}>
      <Icon name={iconName} color="black" size="small" />
      <label>{label}</label>
      {help && (
        <Tooltip tooltip={help}>
          <div>
            <Icon name="help" size="normal" color="black" handleHover={true} />
          </div>
        </Tooltip>
      )}
    </div>
  );
};
