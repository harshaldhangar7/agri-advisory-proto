from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routers import farmers, advisory

app = FastAPI(title="Agri Advisory Prototype")

# Allow local frontend origin (Vite default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farmers.router)
app.include_router(advisory.router)

@app.on_event("startup")
def on_startup():
    init_db()