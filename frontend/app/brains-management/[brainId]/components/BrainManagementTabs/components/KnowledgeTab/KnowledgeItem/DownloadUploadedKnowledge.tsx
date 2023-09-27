import axios from "axios";
import { BsFillCloudArrowDownFill } from "react-icons/bs";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { getFileIcon } from "@/lib/helpers/getFileIcon";
import { UploadedKnowledge } from "@/lib/types/Knowledge";

export const DownloadUploadedKnowledge = ({
  knowledge,
}: {
  knowledge: UploadedKnowledge;
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
    <a
      onClick={() => void downloadFile()}
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      {getFileIcon(knowledge.fileName)}
      <BsFillCloudArrowDownFill fontSize="small" />
    </a>
  );
};
