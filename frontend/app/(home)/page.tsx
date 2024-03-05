"use client";
import { useEffect } from "react";

const HomePage = (): JSX.Element => {
  useEffect(() => {
    window.location.href = "/search";
  }, []);

  return <></>;
};

export default HomePage;
