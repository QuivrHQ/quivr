import { FC } from 'react';
import { motion } from 'framer-motion';

interface DocumentProps {
  document: {
    name: string;
    size: string;
  };
  viewDocument: (document: { name: string; size: string }) => void;
}

const DocumentItem: FC<DocumentProps> = ({ document, viewDocument }) => {
  return (
    <motion.div
      initial={{ x: -64, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: 64, opacity: 0 }}
      className="flex items-center justify-between w-1/2 p-4 mb-4 bg-white shadow rounded"
    >
      <p className="text-lg">{document.name}</p>
      <button
        onClick={() => viewDocument(document)}
        className="py-2 px-4 bg-blue-500 text-white rounded mr-2 hover:bg-blue-600 transition duration-200"
      >
        View
      </button>
    </motion.div>
  );
};

DocumentItem.displayName = 'DocumentItem';
export default DocumentItem;