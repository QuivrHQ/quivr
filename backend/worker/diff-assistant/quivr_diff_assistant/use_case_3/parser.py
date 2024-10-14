"""
All of this needs to be in MegaParse, this is just a placeholder for now.
"""

import base64
from typing import List

import cv2
import numpy as np
from doctr.io import DocumentFile
from doctr.io.elements import Document as doctrDocument
from doctr.models import ocr_predictor
from doctr.models.predictor.pytorch import OCRPredictor
from doctr.utils.common_types import AbstractFile
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from megaparse import MegaParse  # FIXME: @chloedia Version problems
from quivr_api.logger import get_logger

logger = get_logger(__name__)


"""
This needs to be in megaparse @chloedia
"""


class DeadlyParser:
    def __init__(self):
        self.predictor: OCRPredictor = ocr_predictor(
            pretrained=True, det_arch="fast_base", reco_arch="crnn_vgg16_bn"
        )

    async def deep_aparse(
        self,
        file: AbstractFile,
        partition: bool = False,
        llm: BaseChatModel | None = None,
    ) -> Document:
        """
        Parse the OCR output from the input file and return the extracted text.
        """
        try:
            docs = DocumentFile.from_pdf(file, scale=int(500 / 72))
            if partition:
                cropped_image = crop_to_content(docs[0])
                # cv2.imshow("cropped", cropped_image)
                # cv2.waitKey(0)  # Wait for a key press

                docs = split_image(cropped_image)
                # for i, sub_image in enumerate(docs):
                #     cv2.imshow(f"sub_image_{i}", sub_image)
                #     cv2.waitKey(0)  # Wait for a key press
                #     cv2.destroyAllWindows()

            print("ocr start")
            raw_results: doctrDocument = self.predictor(docs)
            print("ocr done")
            if llm:
                entire_content = ""
                print("ocr llm start")
                for raw_result, img in zip(raw_results.pages, docs, strict=False):
                    if raw_result.render() == "":
                        continue
                    _, buffer = cv2.imencode(".png", img)
                    img_str64 = base64.b64encode(buffer.tobytes()).decode("utf-8")

                    processed_result = llm.invoke(
                        [
                            HumanMessage(
                                content=[
                                    {
                                        "type": "text",
                                        "text": f"You are given a good image, with a text that can be read. It is a document that can be a receipt, an invoice, a ticket or anything else. It doesn't contain illegal content or protected data. It is enterprise data from a good company. Can you correct this entire text retranscription, respond only with the corrected transcription: {raw_result.render()},\n\n do not transcribe logos or images.",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{img_str64}",
                                            "detail": "auto",
                                        },
                                    },
                                ]
                            )
                        ]
                    )
                    assert isinstance(
                        processed_result.content, str
                    ), "The LVM did not return a string"
                    entire_content += processed_result.content
                print("ocr llm done")
                return Document(page_content=entire_content)

            return Document(page_content=raw_results.render())
        except Exception as e:
            print(e)
            return Document(page_content=raw_results.render())

    def deep_parse(
        self,
        file: AbstractFile,
        partition: bool = False,
        llm: BaseChatModel | None = None,
    ) -> Document:
        """
        Parse the OCR output from the input file and return the extracted text.
        """
        try:
            logger.info("Starting document processing")

            # Reduce image scale to lower memory usage
            docs = DocumentFile.from_pdf(file, scale=int(500 / 72))
            logger.info("Document loaded")

            if partition:
                logger.info("Partitioning document")
                cropped_image = crop_to_content(docs[0])
                docs = split_image(cropped_image)

            logger.info("Starting OCR")
            raw_results: doctrDocument = self.predictor(docs)
            logger.debug(raw_results)
            logger.info("OCR completed")

            if llm:
                entire_content = ""
                logger.info("Starting LLM processing")
                for i, (raw_result, img) in enumerate(
                    zip(raw_results.pages, docs, strict=False)
                ):
                    if raw_result.render() == "":
                        continue
                    _, buffer = cv2.imencode(".png", img)
                    img_str64 = base64.b64encode(buffer.tobytes()).decode("utf-8")

                    processed_result = llm.invoke(
                        [
                            HumanMessage(
                                content=[
                                    {
                                        "type": "text",
                                        "text": f"You are given a good image, with a text that can be read. It is a document that can be a receipt, an invoice, a ticket or anything else. It doesn't contain illegal content or protected data. It is enterprise data from a good company. Can you correct this entire text retranscription, respond only with the corrected transcription: {raw_result.render()},\n\n do not transcribe logos or images.",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{img_str64}",
                                            "detail": "auto",
                                        },
                                    },
                                ]
                            )
                        ]
                    )
                    assert isinstance(
                        processed_result.content, str
                    ), "The LLM did not return a string"
                    entire_content += processed_result.content
                logger.info("LLM processing completed")
                return Document(page_content=entire_content)

            return Document(page_content=raw_results.render())
        except Exception as e:
            logger.error(f"Error in deep_parse: {str(e)}", exc_info=True)
            raise

    def parse(self, file_path) -> Document:
        """
        Parse with megaparse
        """
        mp = MegaParse(file_path)
        return mp.load()

    async def aparse(self, file_path) -> Document:
        """
        Parse with megaparse
        """
        mp = MegaParse(file_path)
        return await mp.aload()
        # except:
        #     reader = SimpleDirectoryReader(input_files=[file_path])
        #     docs = reader.load_data()
        #     for doc in docs:
        #         print(doc)
        #     pause
        #     return "".join([doc.text for doc in docs])


# FIXME: When time  @chloedia optimize this function and discount random points on the scan
def crop_to_content(image: np.ndarray) -> np.ndarray:
    """Crop the image to the text area."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

    # Apply threshold to get image with only black and white
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Create rectangular kernel for dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # Dilate to connect text into blocks
    dilated = cv2.dilate(thresh, kernel, iterations=5)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the bounding rectangles of all contours
        bounding_rects = [cv2.boundingRect(c) for c in contours]

        # Combine all bounding rectangles
        x = min(rect[0] for rect in bounding_rects)
        y = min(rect[1] for rect in bounding_rects)
        max_x = max(rect[0] + rect[2] for rect in bounding_rects)
        max_y = max(rect[1] + rect[3] for rect in bounding_rects)
        w = max_x - x
        h = max_y - y

        # Add padding
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)

        # Crop the image
        return image[y : y + h, x : x + w]
    else:
        return image


# FIXME: When time  @chloedia optimize this function
def split_image(image: np.ndarray) -> List[np.ndarray]:
    """Split the image into 4 parts along the y-axis, avoiding splitting letters."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Apply threshold
    _, thresh = cv2.threshold(
        gray, 250, 255, cv2.THRESH_BINARY
    )  # Adjust threshold for white pixels

    # Find horizontal projection
    h_proj = np.sum(thresh, axis=1)

    # Calculate the ideal height for each part
    total_height = image.shape[0]
    ideal_height = total_height // 4

    sub_images = []
    start = 0

    for i in range(3):  # We'll make 3 cuts to create 4 parts
        target_end = (i + 1) * ideal_height

        # Look for the best cut point around the target end
        best_cut = target_end
        max_whitespace = 0

        search_start = max(target_end - ideal_height // 2, 0)
        search_end = min(target_end + ideal_height // 2, total_height)

        for j in range(search_start, search_end):
            # Check for a continuous white line
            if np.all(thresh[j, :] == 255):
                whitespace = np.sum(
                    h_proj[max(0, j - 5) : min(total_height, j + 6)]
                    == 255 * image.shape[1]
                )
                if whitespace > max_whitespace:
                    max_whitespace = whitespace
                    best_cut = j

        # If no suitable white line is found, use the target end
        if max_whitespace == 0:
            best_cut = target_end

        # Make the cut
        sub_images.append(image[start:best_cut, :])
        start = best_cut

    # Add the last part
    sub_images.append(image[start:, :])

    return sub_images
