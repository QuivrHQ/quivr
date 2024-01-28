export interface ButtonProps {
  onClick?: () => void;
  label: string;
  iconName: string;
  type: "add" | "open";
  isSelected: boolean;
}

export const MenuButton = (props: ButtonProps): JSX.Element => {
  console.info(props);

  return (
    // <CoreButton
    //   className={cn("p-2 sm:px-3 text-primary focus:ring-0", className)}
    //   variant={"tertiary"}
    //   data-testid="config-button"
    //   ref={forwardedRef}
    //   onClick={onClick}
    //   {...props}
    // >
    //   <div className="flex flex-row justify-between w-full items-center">
    //     <div className="flex flex-row gap-2 items-center">
    //       {startIcon}
    //       <span>{label}</span>
    //     </div>
    //     {endIcon}
    //   </div>
    // </CoreButton>
    <div>Hey</div>
  );
};
