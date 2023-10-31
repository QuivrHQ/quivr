import axios from "axios";
import { HiOutlineDownload } from "react-icons/hi";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";

export const DownloadUploadedKnowledge = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const { generateSignedUrlKnowledge } = useKnowledgeApi();

  if (!isUploadedKnowledge(knowledge)) {
    return <div />;
  }

  const downloadFile = async () => {
    const download_url = await generateSignedUrlKnowledge({
      knowledgeId: knowledge.id,
    });

    try {
      const response = await axios.get(download_url, {
        responseType: "blob",
      });

      const blobUrl = window.URL.createObjectURL(new Blob([response.data]));

      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = knowledge.fileName;
      document.body.appendChild(a);
      a.click();

      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("Error downloading the file:", error);
    }
  };

  return (
    <a onClick={() => void downloadFile()} className="cursor-pointer">
      <HiOutlineDownload fontSize="small" size={20} />
    </a>
  );
};
