from fastapi import APIRouter
from models import AddDocumentRequest, GetDocumentRequest
from initialize import init_logger
from database import DBManager


router = APIRouter(prefix="/document")
logger = init_logger()

@router.post("/insert")
def insert_document(document: AddDocumentRequest):
    db_manager = DBManager(document.collection_name)
    doc_id = db_manager.add_document(document.document, document.metadata)
    return doc_id

@router.post("/search")
def search_documents(document: GetDocumentRequest):
    logger.info(f"request_body = {document}")
    db_manager = DBManager(document.collection_name)
    results = db_manager.get_documents(document.query, document.limit, document.metadata)
    return results

