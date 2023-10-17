/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        black: "#11243E",
        primary: "#7A27FD",
        "chat-bg-gray": "#D9D9D9",
        "msg-gray": "#9B9B9B",
        "msg-header-gray": "#8F8F8F",
        "msg-purple": "#E0DDFC",
        "onboarding-yellow-bg": "#F6EFDE",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
