const copyToClipboard = async (text?: string | null): Promise<void> => {
  if (typeof text !== "string") {
    return;
  }

  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error("Failed to copy:", err);
  }
};

export default copyToClipboard;
