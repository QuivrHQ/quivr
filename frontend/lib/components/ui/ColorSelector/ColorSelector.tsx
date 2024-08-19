import { useState } from "react";
import { HexColorPicker } from "react-colorful";

export const ColorSelector = (): JSX.Element => {
  const [color, setColor] = useState("#aabbcc");

  return <HexColorPicker color={color} onChange={setColor} />;
};
