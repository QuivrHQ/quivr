import { motion } from "framer-motion";

import { useSideBarContext } from "@/lib/context/SidebarProvider/hooks/useSideBarContext";

type AnimatedDivProps = {
  children: React.ReactNode;
};
export const AnimatedDiv = ({ children }: AnimatedDivProps): JSX.Element => {
  const { isOpened } = useSideBarContext();

  return (
    <motion.div
      initial={{
        width: isOpened ? "260px" : "0px",
      }}
      animate={{
        width: isOpened ? "260px" : "0px",
        opacity: isOpened ? 1 : 0.5,
        boxShadow: isOpened
          ? "10px 10px 16px rgba(0, 0, 0, 0)"
          : "10px 10px 16px rgba(0, 0, 0, 0.5)",
      }}
      className={"overflow-hidden flex flex-col flex-1"}
    >
      {children}
    </motion.div>
  );
};
