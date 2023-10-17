import { VideoPlayer } from "./components/VideoPlayer";

export const DemoSection = (): JSX.Element => {
  return (
    <>
      <h2 className="text-center text-3xl font-semibold mb-2">Demo video</h2>
      <div className="max-w-3xl">
        <VideoPlayer videoSrc="https://user-images.githubusercontent.com/19614572/239713902-a6463b73-76c7-4bc0-978d-70562dca71f5.mp4" />
      </div>
    </>
  );
};
