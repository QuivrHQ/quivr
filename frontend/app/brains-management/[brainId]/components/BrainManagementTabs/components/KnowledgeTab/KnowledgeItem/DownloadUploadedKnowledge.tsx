import axios from "axios";
import { BsFillCloudArrowDownFill } from "react-icons/bs";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { Knowledge } from "@/lib/types/Knowledge";

export const DownloadUploadedKnowledge = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const { generateSignedUrlKnowledge } = useKnowledgeApi();

  const downloadFile = async () => {
    const download_url = await generateSignedUrlKnowledge({
      knowledgeId: knowledge.id,
    });

    try {
      const response = await axios.get(download_url, {
        responseType: "blob",
      });

      console.log("MU URL", download_url);
      const blobUrl = window.URL.createObjectURL(new Blob([response.data]));

      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = knowledge.file_name ?? "toto.pdf";
      document.body.appendChild(a);
      a.click();

      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("Error downloading the file:", error);
    }
  };

  return (
    <a onClick={() => void downloadFile()}>
      <BsFillCloudArrowDownFill fontSize="large" />
    </a>
  );
};
