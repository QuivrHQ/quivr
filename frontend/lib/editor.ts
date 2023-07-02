import { EditorView } from "@tiptap/pm/view";
import { BlobResult } from "@vercel/blob";
import { toast } from "sonner";

export const handleImageUpload = (
  file: File,
  view: EditorView,
  event: ClipboardEvent | DragEvent | Event,
) => {
  // check if the file is an image
  if (!file.type.includes("image/")) {
    toast.error("File type not supported.");

    // check if the file size is less than 50MB
  } else if (file.size / 1024 / 1024 > 50) {
    toast.error("File size too big (max 50MB).");
  } else {
    // reading locally
    // const reader = new FileReader();
    // reader.onload = (e) => {
    //   const { schema } = view.state;
    //   const node = schema.nodes.image.create({
    //     src: e.target?.result,
    //     alt: file,
    //     title: file.name,
    //   }); // creates the image element
    //   const transaction = view.state.tr.replaceSelectionWith(node);
    //   view.dispatch(transaction);
    // };
    // reader.readAsDataURL(file);

    // upload to Vercel Blob
    toast.promise(
      fetch("/api/upload", {
        method: "POST",
        headers: {
          "content-type": file?.type || "application/octet-stream",
          "x-vercel-filename": file?.name || "image.png",
        },
        body: file,
      }).then(async (res) => {
        // Successfully uploaded image
        if (res.status === 200) {
          const { url } = (await res.json()) as BlobResult;
          // preload the image
          let image = new Image();
          image.src = url;
          image.onload = () => {
            insertImage(url);
          };

          // No blob store configured
        } else if (res.status === 401) {
          const reader = new FileReader();
          reader.onload = (e) => {
            insertImage(e.target?.result as string);
          };
          reader.readAsDataURL(file);
          throw new Error(
            "`BLOB_READ_WRITE_TOKEN` environment variable not found, reading image locally instead.",
          );

          // Unknown error
        } else {
          throw new Error(`Error uploading image. Please try again.`);
        }
      }),
      {
        loading: "Uploading image...",
        success: "Image uploaded successfully.",
        error: (e) => e.message,
      },
    );
  }

  const insertImage = (url: string) => {
    // for paste events
    if (event instanceof ClipboardEvent) {
      return view.dispatch(
        view.state.tr.replaceSelectionWith(
          view.state.schema.nodes.image.create({
            src: url,
            alt: file.name,
            title: file.name,
          }),
        ),
      );

      // for drag and drop events
    } else if (event instanceof DragEvent) {
      const { schema } = view.state;
      const coordinates = view.posAtCoords({
        left: event.clientX,
        top: event.clientY,
      });
      const node = schema.nodes.image.create({
        src: url,
        alt: file.name,
        title: file.name,
      }); // creates the image element
      const transaction = view.state.tr.insert(coordinates?.pos || 0, node); // places it in the correct position
      return view.dispatch(transaction);

      // for input upload events
    } else if (event instanceof Event) {
      return view.dispatch(
        view.state.tr.replaceSelectionWith(
          view.state.schema.nodes.image.create({
            src: url,
            alt: file.name,
            title: file.name,
          }),
        ),
      );
    }
  };
};
