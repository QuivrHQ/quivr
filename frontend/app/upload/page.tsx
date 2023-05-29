"use client";
import Link from "next/link";
import Button from "../components/ui/Button";
import { Divider } from "../components/ui/Divider";
import PageHeading from "../components/ui/PageHeading";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

export default function UploadPage() {
  return (
    <main className="pt-24">
      <PageHeading
        title="Upload Knowledge"
        subtitle="Text, document, spreadsheet, presentation, audio, video, and URLs supported"
      />
      <FileUploader />
      <Divider text="or" className="m-5" />
      <Crawler />
      <div className="flex flex-col items-center justify-center gap-5 mt-5">
        <Link href={"/chat"}>
          <Button variant={"secondary"} className="py-3">
            Chat
          </Button>
        </Link>
      </div>
    </main>
  );
}
