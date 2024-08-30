"use client";
import { Dispatch, forwardRef, SetStateAction } from "react";

import Button, { ButtonProps } from "@/lib/components/ui/Button";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { iconList } from "@/lib/helpers/iconList";
import { cn } from "@/lib/utils";

import styles from "./ToolbarButton.module.scss";

type ToolbarButtonProps = {
  active?: boolean;
  setActive?: Dispatch<SetStateAction<boolean>>;
  iconName: keyof typeof iconList;
} & Omit<ButtonProps, "variant">;

export const ToolbarButton = forwardRef(
  (
    {
      className,
      iconName,
      active = false,
      setActive,
      onClick,
      ...props
    }: ToolbarButtonProps,
    ref
  ): JSX.Element => {
    return (
      <Button
        ref={ref}
        variant={"primary"}
        className={cn(
          styles.toolbar_button,
          active ? styles.active : "",
          className
        )}
        onClick={(e) => {
          console.log("HELLO");
          setActive?.((t) => !t);
          // Run the onClick callback from the prop
          onClick?.(e);
        }}
        {...props}
      >
        <Icon
          name={iconName}
          color={active ? "primary" : "black"}
          size={"normal"}
        />
      </Button>
    );
  }
);

ToolbarButton.displayName = "ToolbarButton";
