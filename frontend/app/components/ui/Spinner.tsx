import { FC } from "react";
import { FaSpinner } from "react-icons/fa";

interface SpinnerProps {}

const Spinner: FC<SpinnerProps> = ({}) => {
  return <FaSpinner className="animate-spin m-5" />;
};

export default Spinner;
