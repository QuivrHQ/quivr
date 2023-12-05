// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainCreationHandler = () => {
  const createBrain = () => {
    console.log("createBrain");
  };

  return {
    createBrain,
  };
};
