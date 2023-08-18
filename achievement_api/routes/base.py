from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware

from achievement_api import __version__
from achievement_api.settings import get_settings

from .achievement import router as achievement_router
from .reciever import router as reciever_router
from .user import router as user_router


settings = get_settings()
app = FastAPI(
    title='АПИ достижений',
    description='Программный интерфейс ачивок для Твой ФФ!',
    version=__version__,
    # Отключаем нелокальную документацию
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '/',
    docs_url=None if __version__ != 'dev' else '/docs',
    redoc_url=None,
)


app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(achievement_router)
app.include_router(reciever_router)
app.include_router(user_router)
app.mount('/static', StaticFiles(directory=settings.STATIC_FOLDER))
