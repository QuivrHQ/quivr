import { useEffect, useRef } from "react";

interface VideoPlayerProps {
  videoSrc: string;
}

export const VideoPlayer = ({ videoSrc }: VideoPlayerProps): JSX.Element => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const videoElement = videoRef.current;

    const handleScroll = () => {
      if (!videoElement) {
        return;
      }
      const videoRect = videoElement.getBoundingClientRect();
      const isVideoVisible =
        videoRect.top >= 0 &&
        videoRect.bottom <= window.innerHeight &&
        videoElement.checkVisibility();

      if (isVideoVisible && videoElement.paused) {
        void videoElement.play();
      } else if (!isVideoVisible && !videoElement.paused) {
        videoElement.pause();
      }
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <video
      className="rounded-md shadow-lg dark:shadow-white/25 border dark:border-white/25 w-full"
      ref={videoRef}
      src={videoSrc}
      muted
      loop
    />
  );
};
