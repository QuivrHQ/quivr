export const IntroSection = (): JSX.Element => {
  return (
    <>
      <div className="flex flex-col lg:flex-row items-center justify-center md:justify-start gap-10 h-[calc(100vh-300px)] mb-[calc(50vw*tan(6deg))] md:mb-0">
        <div className="w-[80vw] lg:w-[60%] lg:shrink-0 flex flex-col justify-center gap-20">
          <div>
            <h1 className="text-6xl leading-[5rem] sm:text-7xl sm:leading-[6rem] font-bold text-black block max-w-2xl">
              Get a second Brain with{" "}
              <span className="text-primary">Quivr</span>
            </h1>
            <br />
            <p className="text-xl">
              Upload all your files and start talking with them.
            </p>
          </div>
          <div>
            <button className="text-white bg-black rounded-full px-4 py-2 mx-2">
              Try free demo
            </button>
            <button className="font-semibold px-4 py-2 mx-2">
              Contact sales team
            </button>
          </div>
        </div>
        <div className="w-[80vw] lg:w-[calc(50vw-10%-4rem)] lg:shrink-0 h-[80vw] lg:h-[400px] bg-slate-200 rounded flex flex-col items-center justify-center">
          <p>💻 📱 Laptop / mobile image</p>
          <div className="mx-auto my-5 p-5 w-min-content bg-yellow-100 rounded-lg">
            🚧 New homepage in progress 🚧
          </div>
        </div>
      </div>
    </>
  );
};
