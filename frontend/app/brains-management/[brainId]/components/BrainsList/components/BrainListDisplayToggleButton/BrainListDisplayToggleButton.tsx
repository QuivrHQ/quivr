import { motion } from "framer-motion";
import { MdChevronRight } from "react-icons/md";

type BrainListDisplayToggleButtonProps = {
  opened: boolean;
  setOpened: (opened: boolean) => void;
};
export const BrainListDisplayToggleButton = ({
  opened,
  setOpened,
}: BrainListDisplayToggleButtonProps): JSX.Element => {
  return (
    <button
      onClick={() => {
        setOpened(!opened);
      }}
      className="absolute left-full top-16 text-3xl bg-black dark:bg-white text-white dark:text-black rounded-r-full p-3 pl-1"
      data-testid="brains-list-toggle"
    >
      <motion.div
        whileTap={{ scale: 0.9 }}
        animate={{ scaleX: opened ? -1 : 1 }}
      >
        <MdChevronRight />
      </motion.div>
    </button>
  );
};
