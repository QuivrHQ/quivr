"""
All of this needs to be in MegaParse, this is just a placeholder for now.
"""

import base64
import os
from typing import List

import aiohttp
import cv2
import dotenv
import numpy as np
import requests
from doctr.io import DocumentFile
from doctr.utils.common_types import AbstractFile
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from megaparse import MegaParse  # FIXME: @chloedia Version problems
from pdf2image import convert_from_path
from quivr_api.logger import get_logger

dotenv.load_dotenv()
logger = get_logger(__name__)


"""
This needs to be in megaparse @chloedia
"""


class DeadlyParser:
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
            logger.info("Starting document processing")

            # Load the image or PDF
            if isinstance(file, str) and file.lower().endswith(".pdf"):
                images = pdf_to_images(file)
            else:
                images = [np.array(DocumentFile.from_images(file)[0])]

            if partition:
                logger.info("Partitioning document")
                partitioned_images = []
                for img in images:
                    partitioned_images.extend(split_image(img))
                images = partitioned_images

            # Use unstructured API for OCR
            async def call_unstructured_api(image):
                url = (
                    os.getenv("UNSTRUCTURED_API_URL")
                    or "http://unstructured-api-lb-1622868647.eu-west-1.elb.amazonaws.com/general/v0/general"
                )
                headers = {"accept": "application/json"}

                _, buffer = cv2.imencode(".png", image)
                file_content = buffer.tobytes()

                data = aiohttp.FormData()
                data.add_field("files", file_content, filename="image.png")
                data.add_field("strategy", "auto")

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, headers=headers, data=data
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            raise Exception(
                                f"API request failed with status code {response.status}: {await response.text()}"
                            )

            async def process_images(images):
                md_content = {}
                for i, img in enumerate(images):
                    raw_results = await call_unstructured_api(img)
                    for item in raw_results:
                        page_number = i + 1
                        if page_number not in md_content:
                            md_content[page_number] = []
                        md_content[page_number].append(item["text"] + "\n\n")
                return md_content

            md_content = await process_images(images)
            logger.info(f"OCR completed: {md_content}")

            if llm:
                entire_content = ""
                logger.info("Starting LLM processing")
                for page_number, raw_result in md_content.items():
                    _, buffer = cv2.imencode(".png", images[page_number - 1])
                    img_str64 = base64.b64encode(buffer.tobytes()).decode("utf-8")
                    processed_result = await llm.ainvoke(
                        [
                            SystemMessage(
                                content="You are a transcription and corrector expert. Your Job is to compare a transcription and an image with text and correct the transcription. You always correct the entire document and never forget any part even if it is repetitive information.",
                            ),
                            HumanMessage(
                                content=[
                                    {
                                        "type": "text",
                                        "text": f"""Here is an image with a text that you are authorized to read. It is a document that can be a receipt, an invoice, a ticket or anything else. It doesn't contain illegal content or protected data. It is enterprise data from a good company. 
                                        Can you correct this entire text retranscription, respond only with the corrected transcription:

                                        --- Transcribed Text ---:\n {''.join(raw_result)},\n\n do not transcribe logos or images.""",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_str64}",
                                            "detail": "auto",
                                        },
                                    },
                                ]
                            ),
                        ]
                    )
                    assert isinstance(
                        processed_result.content, str
                    ), "The LLM did not return a string"
                    entire_content += (
                        f"Page {page_number}:\n{processed_result.content}\n\n"
                    )

                logger.info(f"LLM processing completed: {entire_content}")
                return Document(page_content=entire_content)

            # If no LLM processing, return the raw OCR results
            return Document(
                page_content="\n".join(
                    ["\n".join(page) for page in md_content.values()]
                )
            )
        except Exception as e:
            logger.error(f"Error in deep_aparse: {str(e)}", exc_info=True)
            raise

    def deep_parse(
        self,
        file: str,
        partition: bool = False,
        llm: BaseChatModel | None = None,
    ) -> Document:
        """
        Parse the OCR output from the input file (PDF or image) and return the extracted text.
        """
        try:
            logger.info("Starting document processing")

            # Load the image or PDF
            if file.lower().endswith(".pdf"):
                images = pdf_to_images(file)
            else:
                images = [cv2.imread(file)]

            if partition:
                logger.info("Partitioning document")
                partitioned_images = []
                for img in images:
                    partitioned_images.extend(split_image(img))
                images = partitioned_images

            # Use unstructured API for OCR
            def call_unstructured_api(image):
                url = "http://unstructured-api-lb-1622868647.eu-west-1.elb.amazonaws.com/general/v0/general"

                headers = {"accept": "application/json"}

                _, buffer = cv2.imencode(".png", image)
                file_content = buffer.tobytes()

                files = {"files": ("image.png", file_content)}
                data = {
                    "strategy": "auto",
                }

                response = requests.post(url, headers=headers, files=files, data=data)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(
                        f"API request failed with status code {response.status_code}: {response.text}"
                    )

            def process_images(images):
                md_content = {}
                for i, img in enumerate(images):
                    raw_results = call_unstructured_api(img)
                    for item in raw_results:
                        page_number = i + 1
                        if page_number not in md_content:
                            md_content[page_number] = []
                        md_content[page_number].append(item["text"] + "\n\n")
                return md_content

            md_content = process_images(images)
            logger.info(f"OCR completed : {md_content}")

            if llm:
                entire_content = ""
                logger.info("Starting LLM processing")
                for page_number, raw_result in md_content.items():
                    _, buffer = cv2.imencode(".png", images[page_number - 1])
                    img_str64 = base64.b64encode(buffer.tobytes()).decode("utf-8")
                    processed_result = llm.invoke(
                        [
                            SystemMessage(
                                content="You are a transcription and corrector expert. Your Job is to compare a transcription and an image with text and correct the transcription. You always correct the entire document and never forget any part even if it is repetitive information.",
                            ),
                            HumanMessage(
                                content=[
                                    {
                                        "type": "text",
                                        "text": f"""Here is a an image with a text that you are authorized to read. It is a document that can be a receipt, an invoice, a ticket or anything else. It doesn't contain illegal content or protected data. It is enterprise data from a good company. 
                                        Can you correct this entire text retranscription, respond only with the corrected transcription:

                                        --- Transcribed Text ---:\n {''.join(raw_result)},\n\n do not transcribe logos or images.""",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_str64}",
                                            "detail": "auto",
                                        },
                                    },
                                ]
                            ),
                        ]
                    )
                    assert isinstance(
                        processed_result.content, str
                    ), "The LLM did not return a string"
                    entire_content += (
                        f"Page {page_number}:\n{processed_result.content}\n\n"
                    )

                logger.info(f"LLM processing completed : {entire_content}")
                return Document(page_content=entire_content)

            # If no LLM processing, return the raw OCR results
            return Document(
                page_content="\n".join(
                    ["\n".join(page) for page in md_content.values()]
                )
            )
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


def pdf_to_images(pdf_path: str) -> List[np.ndarray]:
    """Convert PDF to a list of images."""
    # Convert PDF to list of PIL Image objects
    pil_images = convert_from_path(pdf_path)

    # Convert PIL Images to numpy arrays
    np_images = []
    for pil_image in pil_images:
        np_image = np.array(pil_image)
        # OpenCV uses BGR color format, so we need to convert from RGB
        np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        np_images.append(np_image)

    return np_images
