import { useState } from "react";

const colors: string[] = [
  "#FF5733",
  "#33FF57",
  "#3357FF",
  "#F5F5F5",
  "#C70039",
  "#900C3F",
  "#581845",
  "#FFBD33",
  "#33FFBD",
  "#BD33FF",
  "#FF33A8",
  "#33A8FF",
  "#A833FF",
  "#33FF5D",
  // Ajoute ici les autres couleurs pour un total d'environ 140 couleurs
];

const ColorPicker = (): JSX.Element => {
  const [selectedColor, setSelectedColor] = useState<string>("#FFFFFF");

  return (
    <div>
      <div>
        {colors.map((color) => (
          <div
            key={color}
            onClick={() => setSelectedColor(color)}
            style={{
              backgroundColor: color,
              width: "50px",
              height: "50px",
              borderRadius: "8px",
              cursor: "pointer",
              border: selectedColor === color ? "2px solid black" : "none",
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default ColorPicker;
