import { Chat } from "@/app/chat/types";
import Button from "@/app/components/ui/Button";
import Modal from "@/app/components/ui/Modal";
import { UUID } from "crypto";
import { FC } from "react";
import { FiTrash2 } from "react-icons/fi";

interface DeleteChatProps {
  deleteChat: (chatId: UUID) => void;
  chat: Chat;
}

const DeleteChat: FC<DeleteChatProps> = ({ deleteChat, chat }) => {
  return (
    <Modal
      Trigger={
        <button
          aria-label="Delete chat"
          className="p-2 hover:text-red-500"
          type="button"
          //   onClick={() => deleteChat(chat.chatId)}
        >
          <FiTrash2 />
        </button>
      }
      CloseTrigger={
        <Button
          className="self-end"
          onClick={() => deleteChat(chat.chatId)}
          variant="danger"
        >
          Delete forever
        </Button>
      }
    >
      <h1 className="text-2xl font-bold">Confirm Delete</h1>
      <p className="mb-3">Are you sure you want to delete this chat?</p>
      <p className="text-xs opacity-50">Title: {chat.chatName}</p>
      <p className="text-xs opacity-50 mb-5">Id: {chat.chatId}</p>
    </Modal>
  );
};

export default DeleteChat;
