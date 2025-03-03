
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


from app.database import Base, engine
from app.routers import tags_metadata, mobi_test
from app.logging import logger

app = FastAPI(description=f"Mobi Test API", 
              title="Mobi Test API", 
              version="1.0.0", 
              openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Входящий запрос: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Ответ: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}", exc_info=True)
        raise

Base.metadata.create_all(bind=engine)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

app.include_router(mobi_test)
