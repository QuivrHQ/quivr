export const IntroSection = (): JSX.Element => {
  return (
    <>
      <div className="flex flex-col md:flex-row items-center justify-center gap-10 h-[calc(100vh-300px)] mb-[calc(50vw*tan(6deg))] md:mb-0">
        <div>
          <h1 className="text-5xl font-bold">Get a second brain with Quivr</h1>
          <p>Upload all your files and start talking with them.</p>
          <button className="text-white bg-black rounded-full px-4 py-2 mx-2">
            Try free demo
          </button>
          <button className="font-semibold px-4 py-2 mx-2">
            Contact sales team
          </button>
        </div>
        <div className="w-[80vw] md:w-[400px] h-[80vw] md:h-[400px] bg-slate-200 rounded flex flex-col items-center justify-center">
          <p>💻 📱 Laptop / mobile image</p>
          <div className="mx-auto my-5 p-5 w-min-content bg-yellow-100 rounded-lg">
            🚧 New homepage in progress 🚧
          </div>
        </div>
      </div>
    </>
  );
};
