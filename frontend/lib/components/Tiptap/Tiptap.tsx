"use client";
import { Dropcursor } from "@tiptap/extension-dropcursor";
import { Gapcursor } from "@tiptap/extension-gapcursor";
import { Link } from "@tiptap/extension-link";
import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";

import styles from "./Tiptap.module.scss";
import { Toolbar } from "./components";

const defaultContent = `
    <h1>
      Hi there,
    </h1>
    <p>
      this is a basic <em>basic</em> example of <strong>Tiptap</strong>. Sure, there are all kind of basic text styles you’d probably expect from a text editor. But wait until you see the lists:
    </p>
    <ul>
      <li>
        That’s a bullet list with one …
      </li>
      <li>
        … or two list items.
      </li>
    </ul>
    <p>
      Isn’t that great? And all of that is editable. But wait, there’s more. Let’s try a code block:
    </p>
<pre><code class="language-css">body {
  display: none;
}</code></pre>
    <p>
      I know, I know, this is impressive. It’s only the tip of the iceberg though. Give it a try and click a little bit around. Don’t forget to check the other examples too.
    </p>
    <blockquote>
      Wow, that’s amazing. Good work, boy! 👏
      <br />
      — Mom
    </blockquote>
`;

export const Tiptap = (): JSX.Element => {
  const editor = useEditor({
    extensions: [StarterKit, Dropcursor, Gapcursor, Link],
    content: defaultContent,
    immediatelyRender: false,
  });

  if (!editor) {
    return <></>;
  }

  return (
    <div className={styles.editor_wrapper}>
      <Toolbar editor={editor} />
      <EditorContent className={styles.content_wrapper} editor={editor} />
    </div>
  );
};
