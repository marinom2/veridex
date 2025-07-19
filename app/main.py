from fastapi import FastAPI
from app.api import routes
from app.rule_editor import router as rule_editor_router
from app.api.rules_api import router as rules_api_router 
app = FastAPI(title="Veridex 🧠 Clinical Rule Engine")

app.include_router(routes.router)
app.include_router(rule_editor_router)
app.include_router(rules_api_router)  

@app.get("/")
def root():
    return {"message": "Welcome to Veridex"}