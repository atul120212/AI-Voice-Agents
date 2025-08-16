import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Base dir (where app/ lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

# Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Root route -> renders index.html
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Import routes
from routes import llm_routes, chat_routes, tts_routes, upload_routes
app.include_router(llm_routes.router)
app.include_router(chat_routes.router)
app.include_router(tts_routes.router)
app.include_router(upload_routes.router)
