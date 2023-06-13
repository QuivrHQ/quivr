"use client";
import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";
import PageHeading from "@/lib/components/ui/PageHeading";
import Link from "next/link";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

export default function UploadPage() {
  return (
    <main className="pt-10">
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
