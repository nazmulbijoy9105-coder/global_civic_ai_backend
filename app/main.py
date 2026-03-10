from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, questions # Add assessment here when ready

app = FastAPI(
    title="Global Civic AI",
    description="Backend API for Global Civic AI platform",
    version="1.0.0",
    docs_url=None, 
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        custom_css="""
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; background-color: #f5f5f7; }
        .swagger-ui .topbar { display: none }
        .opblock { border-radius: 14px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important; margin-bottom: 20px !important; }
        .opblock-summary { padding: 15px !important; }
        .swagger-ui .info .title { font-size: 32px; font-weight: 700; color: #1d1d1f; }
        """
    )

app.include_router(auth.router)
app.include_router(questions.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}