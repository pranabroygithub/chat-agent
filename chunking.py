from langchain_text_splitters import HTMLSemanticPreservingSplitter
from initialize import init_logger
import requests
from bs4 import Tag

logger = init_logger()

def html_chunking(url: str):

    headers_to_split_on = [
        ("h1", "Header 1")
    ]

    html_string = ""
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_string = response.text

    except requests.exceptions.RequestException:
        logger.exception("Failed to get html content")

    splitter = HTMLSemanticPreservingSplitter(
        headers_to_split_on=headers_to_split_on,
        separators=["\n\n", "\n", ". ", "! ", "? "],
        max_chunk_size=500,
        preserve_images=True,
        preserve_videos=True,
        elements_to_preserve=["table", "ul", "ol", "code"],
        denylist_tags=["script", "style", "head"],
        custom_handlers={"code": code_handler},
    )

    chunks = splitter.split_text(html_string)
    return chunks

def code_handler(element: Tag) -> str:
    data_lang = element.get("data-lang")
    code_format = f"<code:{data_lang}>{element.get_text()}</code>"
    return code_format

