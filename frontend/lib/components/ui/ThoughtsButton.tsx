
import Icon from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { IconSize } from "@/lib/types/Icons";


type ThoughtsButtonProps = {
  text: string;
  size: IconSize;
};

export const ThoughtsButton = ({ text, size }: ThoughtsButtonProps): JSX.Element => {

  return (
      <Tooltip tooltip={text}>
        <div>
          <Icon name="question" size={size} color="black" handleHover={true}/>
        </div>
      </Tooltip>
  );
};