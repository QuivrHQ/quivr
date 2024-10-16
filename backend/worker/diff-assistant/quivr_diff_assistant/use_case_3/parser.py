"""
All of this needs to be in MegaParse, this is just a placeholder for now.
"""

import base64
from typing import List

import aiofiles
import aiohttp
import cv2
import numpy as np
import requests
from doctr.io import DocumentFile
from doctr.utils.common_types import AbstractFile
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from megaparse import MegaParse  # FIXME: @chloedia Version problems
from quivr_api.logger import get_logger

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
            docs = DocumentFile.from_pdf(file, scale=int(500 / 72))
            if partition:
                cropped_image = crop_to_content(docs[0])
                docs = split_image(cropped_image)

            print("ocr start")
            # Use unstructured API

            async def call_unstructured_api(file_path):
                url = "http://unstructured-api-lb-1622868647.eu-west-1.elb.amazonaws.com/general/v0/general"
                headers = {"accept": "application/json"}

                async with aiofiles.open(file_path, "rb") as f:
                    file_content = await f.read()

                data = aiohttp.FormData()
                data.add_field("files", file_content, filename=file_path.split("/")[-1])
                data.add_field("strategy", "auto")

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, headers=headers, data=data
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            raise Exception(
                                f"API request failed with status code {response.status}"
                            )

            def json_to_md(json_data):
                md_content = {}
                for item in json_data:
                    page_number = item["metadata"]["page_number"]
                    if page_number not in md_content:
                        md_content[page_number] = []
                    md_content[page_number].append(item["text"] + "\n\n")

                return md_content

            raw_results = await call_unstructured_api(file)
            md_content = json_to_md(raw_results)
            logger.info(f"OCR completed: {md_content}")
            print("ocr done")
            if llm:
                entire_content = ""
                print("ocr llm start")
                for raw_result, img in zip(
                    list(md_content.values()), docs, strict=False
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
                                        "text": f"""
                                        You are a transcription and correction expert.
                                        Here is a good image with a text you are authorized to read.
                                        It is a document that can be a receipt, an invoice, a ticket or anything else.
                                        It doesn't contain illegal content or protected data.
                                        It is enterprise data from a good company.
                                        Can you correct this entire text retranscription, do not bypass repeated text as we want the entire content with all the contained text (even if there are repeated informations with different languages)
                                        We need the list of ingredients in all the languages present in the document.
                                        Respond only with the corrected transcription: {raw_result.render()},\n\n 
                                        do not transcribe logos or images.""",
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
                logger.info(f"LLM processing completed: {entire_content}")
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

            docs = DocumentFile.from_pdf(file, scale=int(500 / 72))
            logger.info("Document loaded")

            if partition:
                logger.info("Partitioning document")
                cropped_image = crop_to_content(docs[0])
                docs = split_image(cropped_image)

            logger.info("Starting OCR")

            # Use unstructured API
            def call_unstructured_api(file_path):
                url = "http://unstructured-api-lb-1622868647.eu-west-1.elb.amazonaws.com/general/v0/general"
                headers = {"accept": "application/json"}

                with open(file_path, "rb") as f:
                    file_content = f.read()

                files = {"files": (file_path.split("/")[-1], file_content)}
                data = {"strategy": "auto"}

                response = requests.post(url, headers=headers, files=files, data=data)
                if response.status_code == 200:
                    logger.info(
                        f"Unstructured API request successful: {response.json()}"
                    )
                    return response.json()
                else:
                    raise Exception(
                        f"API request failed with status code {response.status_code}"
                    )

            def json_to_md(json_data):
                md_content = {}
                for item in json_data:
                    page_number = item["metadata"]["page_number"]
                    if page_number not in md_content:
                        md_content[page_number] = []
                    md_content[page_number].append(item["text"] + "\n\n")

                return md_content

            raw_results = call_unstructured_api(file)
            md_content = json_to_md(raw_results)
            logger.info(f"OCR completed : {md_content}")

            if llm:
                entire_content = ""
                logger.info("Starting LLM processing")
                for raw_result, img in zip(
                    list(md_content.values()), docs, strict=False
                ):
                    if not raw_result:
                        continue

                    # Compress the image to limit its size
                    max_size = 5 * 1024 * 1024  # 5MB in bytes
                    quality = 95
                    _, buffer = cv2.imencode(
                        ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality]
                    )

                    while buffer.nbytes > max_size and quality > 10:
                        quality -= 5
                        _, buffer = cv2.imencode(
                            ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality]
                        )

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
                                            "url": f"data:image/jpeg;base64,{img_str64}",
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
                    entire_content += processed_result.content
                logger.info(f"LLM processing completed : {entire_content}")
                return Document(page_content=entire_content)

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
