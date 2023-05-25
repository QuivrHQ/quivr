"use client";
import { ReactNode, forwardRef, useImperativeHandle, useState } from "react";
import * as ToastPrimitive from "@radix-ui/react-toast";
import Button from "./Button";

interface ToastProps extends ToastPrimitive.ToastProps {
  children?: ReactNode;
}

export const Toast = forwardRef(
  ({ children, ...props }: ToastProps, forwardedRef) => {
    const [count, setCount] = useState(0);

    useImperativeHandle(forwardedRef, () => ({
      publish: () => setCount((count) => count + 1),
    }));

    return (
      <>
        <ToastPrimitive.Provider duration={Infinity}>
          {Array.from({ length: count }).map((_, index) => (
            <ToastPrimitive.Root
              className="bg-white dark:bg-black px-8 max-w-sm w-full py-5 border rounded-xl shadow-xl flex items-center"
              key={index}
              {...props}
            >
              <ToastPrimitive.Description className="flex-1">
                {children}
              </ToastPrimitive.Description>
              <ToastPrimitive.Close asChild>
                <Button variant={"tertiary"}>Dismiss</Button>
              </ToastPrimitive.Close>
            </ToastPrimitive.Root>
          ))}
          <ToastPrimitive.Viewport className="fixed flex-col bottom-0 left-0 right-0 p-5 flex items-end gap-2 outline-none" />
        </ToastPrimitive.Provider>
      </>
    );
  }
);

export default Toast;
