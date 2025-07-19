from fastapi import FastAPI
from rotate_pdf import router as rotate_router
from split_pdf import router as split_router

app = FastAPI()

app.include_router(rotate_router)
app.include_router(split_router)
