import logging
import os.path
import sys
import traceback
import uuid
from asyncio import Lock

from fastapi import FastAPI, Query, Request, Depends
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from imaginairy.http_app.stablestudio import routes
from imaginairy.http_app.utils import generate_image
from imaginairy.schema import ImaginePrompt
from imaginairy.http_app.database import init_db, SessionLocal, Generation

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GenerateUIRequest(BaseModel):
    prompt: str
    model: str = "Stable Diffusion XL"
    image_size: str = "1024 × 1024"
    steps: int = 40
    controlnet: str = "None"

logger = logging.getLogger(__name__)
static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ui"))


gpu_lock = Lock()


app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api/stablestudio")


@app.post("/api/imagine")
async def imagine_endpoint(prompt: ImaginePrompt):
    async with gpu_lock:
        img_io = await run_in_threadpool(generate_image, prompt)
        return StreamingResponse(img_io, media_type="image/jpg")


@app.get("/api/imagine")
async def imagine_get_endpoint(text: str = Query(...)):
    async with gpu_lock:
        img_io = await run_in_threadpool(generate_image, ImaginePrompt(prompt=text))
        return StreamingResponse(img_io, media_type="image/jpg")


@app.get("/edit")
async def edit_redir():
    return FileResponse(f"{static_folder}/index.html")


@app.get("/generate")
async def generate_redir():
    return FileResponse(f"{static_folder}/index.html")


@app.post("/api/generate_ui")
async def generate_ui_endpoint(req: GenerateUIRequest, db = Depends(get_db)):
    async with gpu_lock:
        size_parts = req.image_size.replace(" ", "").split("×")
        width = int(size_parts[0]) if len(size_parts) == 2 else 256
        height = int(size_parts[1]) if len(size_parts) == 2 else 256
        
        model_name = "sd15" if "1.5" in req.model else "sdxl"
        
        prompt = ImaginePrompt(
            prompt=req.prompt, 
            steps=req.steps,
            size=(width, height),
            model_weights=model_name
        )
        img_io = await run_in_threadpool(generate_image, prompt)
        
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(static_folder, "outputs", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(img_io.getvalue())
            
        try:
            db_gen = Generation(
                prompt=req.prompt,
                model_name=req.model,
                image_path=f"/outputs/{filename}"
            )
            db.add(db_gen)
            db.commit()
            db.refresh(db_gen)
            gen_id = db_gen.id
        except Exception as e:
            print(f"DB Error: {e}")
            gen_id = None
        
        return {"image_url": f"/outputs/{filename}", "id": gen_id}

@app.get("/api/history")
def get_history(db = Depends(get_db)):
    try:
        generations = db.query(Generation).order_by(Generation.created_at.desc()).limit(50).all()
        return [{"id": g.id, "prompt": g.prompt, "model": g.model_name, "image_url": g.image_path} for g in generations]
    except Exception as e:
        print(f"DB Error: {e}")
        return []

app.mount("/", StaticFiles(directory=static_folder, html=True), name="static")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
