# app/main.py

from fastapi import FastAPI
from app.api import routes
from app.api.fields import router as fields_router
from app.api.rules_api import router as rules_api_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Veridex 🧠 Clinical Rule Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(fields_router)
app.include_router(rules_api_router)
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Veridex"}