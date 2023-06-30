export const generateUUID = (): string => {
  const array = new Uint32Array(4);
  window.crypto.getRandomValues(array);
  let idx = -1;

  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    idx++;
    const r = (array[idx >> 3] >> ((idx % 8) * 4)) & 15;
    const v = c === "x" ? r : (r & 0x3) | 0x8;

    return v.toString(16);
  });
};
