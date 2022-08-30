import os 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import burgers_router, auth_router


load_dotenv()

def get_application():
    app = FastAPI(
        title="Burgueria",
        description="API para criação de burgers.",
        version="1.0.0",
    )

    origins = os.getenv("ORIGINS")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router.router, prefix='/api')
    app.include_router(burgers_router.router, prefix='/api')

    return app


app = get_application()