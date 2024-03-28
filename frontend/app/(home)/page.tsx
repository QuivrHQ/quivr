"use client";
import { Suspense } from "react";

import Login from "../(auth)/login/page";

const Main = (): JSX.Element => {
  return <Login />;
};

const Home = (): JSX.Element => {
  return (
    <Suspense fallback="Loading...">
      <Main />
    </Suspense>
  );
};

export default Home;
