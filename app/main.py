# app/main.py

from fastapi import FastAPI
from app.api import routes
from app.api.fields import router as fields_router
from app.api.rules_api import router as rules_api_router
from app.rule_editor import router as rule_editor_router

app = FastAPI(title="Veridex 🧠 Clinical Rule Engine")

# Mount routers
app.include_router(fields_router)
app.include_router(rules_api_router)
app.include_router(rule_editor_router)
app.include_router(routes.router) 

@app.get("/")
def root():
    return {"message": "Welcome to Veridex"}