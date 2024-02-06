import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { BsArrowRightShort } from "react-icons/bs";
import { CiChat1, CiFlag1 } from "react-icons/ci";
import {
  FaCheck,
  FaCheckCircle,
  FaKey,
  FaRegStar,
  FaRegUserCircle,
  FaUnlock,
} from "react-icons/fa";
import { FaArrowUpFromBracket } from "react-icons/fa6";
import { IoIosAdd, IoMdClose, IoMdLogOut } from "react-icons/io";
import { IoHomeOutline, IoSettingsSharp } from "react-icons/io5";
import { IconType } from "react-icons/lib";
import {
  LuBrain,
  LuBrainCircuit,
  LuChevronDown,
  LuChevronRight,
  LuCopy,
  LuFile,
  LuPlusCircle,
  LuSearch,
} from "react-icons/lu";
import {
  MdAlternateEmail,
  MdDeleteOutline,
  MdHistory,
  MdOutlineModeEditOutline,
  MdUploadFile,
} from "react-icons/md";
import { RiHashtag } from "react-icons/ri";
import { VscGraph } from "react-icons/vsc";

export const iconList: { [name: string]: IconType } = {
  add: LuPlusCircle,
  addWithoutCircle: IoIosAdd,
  brain: LuBrain,
  brainCircuit: LuBrainCircuit,
  chat: CiChat1,
  check: FaCheck,
  checkCircle: FaCheckCircle,
  chevronDown: LuChevronDown,
  chevronRight: LuChevronRight,
  close: IoMdClose,
  copy: LuCopy,
  delete: MdDeleteOutline,
  edit: MdOutlineModeEditOutline,
  email: MdAlternateEmail,
  file: LuFile,
  flag: CiFlag1,
  followUp: FaArrowUpFromBracket,
  graph: VscGraph,
  hastag: RiHashtag,
  history: MdHistory,
  home: IoHomeOutline,
  key: FaKey,
  loader: AiOutlineLoading3Quarters,
  logout: IoMdLogOut,
  redirection: BsArrowRightShort,
  search: LuSearch,
  settings: IoSettingsSharp,
  star: FaRegStar,
  unlock: FaUnlock,
  upload: MdUploadFile,
  user: FaRegUserCircle,
};
