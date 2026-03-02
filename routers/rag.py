from fastapi import APIRouter, HTTPException
from models import AddDocumentRequest, GetDocumentRequest, UpdateDocumentRequest
from initialize import init_logger
from database import DBManager


router = APIRouter(prefix="/document")
logger = init_logger()

@router.post("/insert", status_code=201)
def insert_document(document: AddDocumentRequest):
    logger.info(f"request_body = {document}")
    db_manager = DBManager(document.collection_name)
    result = db_manager.add_document(document.document, document.metadata)
    return result

@router.post("/search")
def search_documents(document: GetDocumentRequest):
    logger.info(f"request_body = {document}")
    db_manager = DBManager(document.collection_name)
    results = db_manager.get_documents(document.query, document.limit, document.metadata)
    return results

@router.put("/update")
def update_document(document: UpdateDocumentRequest):
    logger.info(f"request_body = {document}")
    db_manager = DBManager(document.collection_name)
    result = db_manager.update_document(document.id, document.document, document.metadata)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"No document found with id = {document.id}")

@router.delete("/delete")
def delete_document(id: str, collection_name: str):
    logger.info(f"request_params = {id}, collection_name = {collection_name}")
    db_manager = DBManager(collection_name)
    result = db_manager.delete_document(id)
    if result:
        return {"message" : f"{result} document deleted"}
    raise HTTPException(status_code=404, detail=f"No document found with id = {id}")

@router.get("/find")
def find_by_id(id: str, collection_name: str):
    logger.info(f"request_params = {id}, collection_name = {collection_name}")
    db_manager = DBManager(collection_name)
    result = db_manager.find_by_ids([id])
    return result
