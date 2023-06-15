import { createContext } from "react";

import { ToastPublisher } from "./types";

const publish: ToastPublisher = () => void 0;

export const ToastContext = createContext({ publish });
