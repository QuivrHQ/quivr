import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { BsArrowRightShort, BsChatLeftText } from "react-icons/bs";
import { CgSoftwareDownload } from "react-icons/cg";
import { CiFlag1 } from "react-icons/ci";
import {
  FaCheck,
  FaCheckCircle,
  FaKey,
  FaRegStar,
  FaRegUserCircle,
  FaUnlock,
} from "react-icons/fa";
import { FaInfo } from "react-icons/fa6";
import { FiUpload } from "react-icons/fi";
import {
  IoIosAdd,
  IoIosHelpCircleOutline,
  IoMdClose,
  IoMdLogOut,
} from "react-icons/io";
import {
  IoArrowUpCircleOutline,
  IoHomeOutline,
  IoSettingsSharp,
} from "react-icons/io5";
import { IconType } from "react-icons/lib";
import {
  LuBrain,
  LuBrainCircuit,
  LuChevronDown,
  LuChevronLeft,
  LuChevronRight,
  LuCopy,
  LuFile,
  LuPlusCircle,
  LuSearch,
} from "react-icons/lu";
import {
  MdAlternateEmail,
  MdDashboardCustomize,
  MdDeleteOutline,
  MdDynamicFeed,
  MdHistory,
  MdOutlineModeEditOutline,
  MdUploadFile,
} from "react-icons/md";
import { RiHashtag } from "react-icons/ri";
import { SlOptions } from "react-icons/sl";
import { TbNetwork } from "react-icons/tb";
import { VscGraph } from "react-icons/vsc";

export const iconList: { [name: string]: IconType } = {
  add: LuPlusCircle,
  addWithoutCircle: IoIosAdd,
  brain: LuBrain,
  brainCircuit: LuBrainCircuit,
  chat: BsChatLeftText,
  check: FaCheck,
  checkCircle: FaCheckCircle,
  chevronDown: LuChevronDown,
  chevronLeft: LuChevronLeft,
  chevronRight: LuChevronRight,
  close: IoMdClose,
  copy: LuCopy,
  custom: MdDashboardCustomize,
  delete: MdDeleteOutline,
  edit: MdOutlineModeEditOutline,
  email: MdAlternateEmail,
  feed: MdDynamicFeed,
  file: LuFile,
  flag: CiFlag1,
  followUp: IoArrowUpCircleOutline,
  graph: VscGraph,
  hastag: RiHashtag,
  help: IoIosHelpCircleOutline,
  history: MdHistory,
  home: IoHomeOutline,
  info: FaInfo,
  key: FaKey,
  loader: AiOutlineLoading3Quarters,
  logout: IoMdLogOut,
  options: SlOptions,
  redirection: BsArrowRightShort,
  search: LuSearch,
  settings: IoSettingsSharp,
  software: CgSoftwareDownload,
  star: FaRegStar,
  unlock: FaUnlock,
  upload: FiUpload,
  uploadFile: MdUploadFile,
  user: FaRegUserCircle,
  website: TbNetwork,
};
